#include "topiclib.h"
#include "math.h"


// ivec
// dvec

int *ivec(int n) //
{
	int *x = (int*)calloc(n,sizeof(int));
	assert(x);
	return x;
}

double *dvec(int n) //
{
	double *x = (double*)calloc(n,sizeof(double));
	assert(x);
	return x;
}


// sort: call qsort library function
// psort

int partition(double *x, int *indx, int left, int right, int pivotIndx) 
{
	double pivotValue = x[indx[pivotIndx]];
	int i, tmp, storeIndx = left;

	/* move pivot to end */
	tmp = indx[pivotIndx];
	indx[pivotIndx] = indx[right];
	indx[right] = tmp;

	for (i=left; i<right; i++) 
        {
		if (x[indx[i]] > pivotValue) 
                {
			tmp = indx[i];
			indx[i] = indx[storeIndx];
			indx[storeIndx] = tmp;
			storeIndx++;
		}
	}

	/* move pivot to storeIndx */
	tmp = indx[storeIndx];
	indx[storeIndx] = indx[right];
	indx[right] = tmp;

	return storeIndx;
}

/* *index should be in the range [0, length(x)] */
void psort(double *x, int *indx, int left, int right, int k)
{
	int pivotIndx, pivotNewIndx;

	if (right > left) 
        {
		pivotIndx = (int) ((right - left)*drand());
		pivotNewIndx = partition(x, indx, left, right, pivotIndx);
		if (pivotNewIndx > left + k) 
                {
			psort(x, indx, left, pivotNewIndx - 1, k);
		}
		if (pivotNewIndx < left + k) 
                {
			psort(x, indx, pivotNewIndx + 1, right, k + left - pivotNewIndx - 1); 
		}
	}
}


void write_dvec (int n, int nrow, int ncol, double *x, char *fname) //
{
	FILE *fp = fopen(fname,"w");                  // write the file
	assert(fp);                                   // ensure currence of the point fp
	fprintf(fp, "%d %d\n", nrow, ncol);           // print the number of topic and the number of word
        
        for (int i = 0; i < ncol; i++)                // the number of word
        {
            for (int j = 0; j < nrow; j++)            // the number of feature
                if (j == nrow-1)                      // the last
                    fprintf(fp, "%f", x[i*nrow+j]);
                else                                  // not the last
                    fprintf(fp, "%f\t", x[i*nrow+j]); // store a line feature of word
            fprintf(fp, "\n");                        // next word
        }

	fclose(fp);                                   // release the point
}

/*------------------------------------------
* sample_chain_rank
*------------------------------------------ */

double etime() //
{
	static double last_clock = 0;
	static double now_time = 0;
	last_clock = now_time;
	now_time = (double) clock ();
	return (double) (now_time - last_clock) / CLOCKS_PER_SEC;
}

typedef unsigned long uint32;

#define N              (624)                 // length of state vector
#define M              (397)                 // a period parameter
#define K              (0x9908B0DFU)         // a magic constant
#define hiBit(u)       ((u) & 0x80000000U)   // mask all but highest   bit of u
#define loBit(u)       ((u) & 0x00000001U)   // mask all but lowest    bit of u
#define loBits(u)      ((u) & 0x7FFFFFFFU)   // mask     the highest   bit of u
#define mixBits(u, v)  (hiBit(u)|loBits(v))  // move hi bit of u to hi bit of v



static uint32   state[N+1];     // state vector + 1 extra to not violate ANSI C
static uint32   *next;          // next random value is computed from here
static int      left = -1;      // can *next++ this many times before reloading


void seedMT(uint32 seed)
{
    //
    // We initialize state[0..(N-1)] via the generator
    //
    //   x_new = (69069 * x_old) mod 2^32
    //
    // from Line 15 of Table 1, p. 106, Sec. 3.3.4 of Knuth's
    // _The Art of Computer Programming_, Volume 2, 3rd ed.
    //
    // Notes (SJC): I do not know what the initial state requirements
    // of the Mersenne Twister are, but it seems this seeding generator
    // could be better.  It achieves the maximum period for its modulus
    // (2^30) iff x_initial is odd (p. 20-21, Sec. 3.2.1.2, Knuth); if
    // x_initial can be even, you have sequences like 0, 0, 0, ...;
    // 2^31, 2^31, 2^31, ...; 2^30, 2^30, 2^30, ...; 2^29, 2^29 + 2^31,
    // 2^29, 2^29 + 2^31, ..., etc. so I force seed to be odd below.
    //
    // Even if x_initial is odd, if x_initial is 1 mod 4 then
    //
    //   the          lowest bit of x is always 1,
    //   the  next-to-lowest bit of x is always 0,
    //   the 2nd-from-lowest bit of x alternates      ... 0 1 0 1 0 1 0 1 ... ,
    //   the 3rd-from-lowest bit of x 4-cycles        ... 0 1 1 0 0 1 1 0 ... ,
    //   the 4th-from-lowest bit of x has the 8-cycle ... 0 0 0 1 1 1 1 0 ... ,
    //    ...
    //
    // and if x_initial is 3 mod 4 then
    //
    //   the          lowest bit of x is always 1,
    //   the  next-to-lowest bit of x is always 1,
    //   the 2nd-from-lowest bit of x alternates      ... 0 1 0 1 0 1 0 1 ... ,
    //   the 3rd-from-lowest bit of x 4-cycles        ... 0 0 1 1 0 0 1 1 ... ,
    //   the 4th-from-lowest bit of x has the 8-cycle ... 0 0 1 1 1 1 0 0 ... ,
    //    ...
    //
    // The generator's potency (min. s>=0 with (69069-1)^s = 0 mod 2^32) is
    // 16, which seems to be alright by p. 25, Sec. 3.2.1.3 of Knuth.  It
    // also does well in the dimension 2..5 spectral tests, but it could be
    // better in dimension 6 (Line 15, Table 1, p. 106, Sec. 3.3.4, Knuth).
    //
    // Note that the random number user does not see the values generated
    // here directly since reloadMT() will always munge them first, so maybe
    // none of all of this matters.  In fact, the seed values made here could
    // even be extra-special desirable if the Mersenne Twister theory says
    // so-- that's why the only change I made is to restrict to odd seeds.
    //

    register uint32 x = (seed | 1U) & 0xFFFFFFFFU, *s = state;
    register int    j;

    for(left=0, *s++=x, j=N; --j;
        *s++ = (x*=69069U) & 0xFFFFFFFFU);
}


inline uint32 randomMT(void)
{
    uint32 y;

    if(--left < 0)
        return(reloadMT());

    y  = *next++;
    y ^= (y >> 11);
    y ^= (y <<  7) & 0x9D2C5680U;
    y ^= (y << 15) & 0xEFC60000U;
    y ^= (y >> 18);
    return(y);
}


uint32 reloadMT(void)
{
    register uint32 *p0=state, *p2=state+2, *pM=state+M, s0, s1;
    register int    j;

    if(left < -1)
        seedMT(4357U);

    left=N-1, next=state+1;

    for(s0=state[0], s1=state[1], j=N-M+1; --j; s0=s1, s1=*p2++)
        *p0++ = *pM++ ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);

    for(pM=state, j=M; --j; s0=s1, s1=*p2++)
        *p0++ = *pM++ ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);

    s1=state[0], *p0 = *pM ^ (mixBits(s0, s1) >> 1) ^ (loBit(s1) ? K : 0U);
    s1 ^= (s1 >> 11);
    s1 ^= (s1 <<  7) & 0x9D2C5680U;
    s1 ^= (s1 << 15) & 0xEFC60000U;
    return(s1 ^ (s1 >> 18));
}
