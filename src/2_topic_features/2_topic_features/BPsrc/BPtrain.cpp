#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <math.h>
#include <assert.h>
#include "topiclib.h"
using namespace std;

#define MAXLEN 500000    // maximum length of the line is 50000 characters
#define LEN 10           // the constant memory size

// Belief Propagation (BP) algorithm
void BP(double ALPHA, double BETA, int W, int J, int D, double *pr, int *ir, int *jc, 
	double *phi, double *phitot, int NNZ, double TD, double TK, double TH) 
{
	int wi, di, i, j, k, topic, iter, ii, J2 = (int) (TK*J), D2 = (int) (TD*D);
	int *ind_rk, *ind_rd;
	double mutot, totprob, xi, rsum, xtot = 0.0;
	double JALPHA = (double) (J*ALPHA), WBETA = (double) (W*BETA);
	double *theta, *mu, *rk, *rd, *munew;

	theta = dvec(J*D);
	mu = dvec(J*NNZ);
	ind_rk = ivec(J*D);
	ind_rd = ivec(D);
	munew = dvec(J);
	rk = dvec(J*D);
	rd = dvec(D);

	/* initialize ind_rk and ind_rd */
	for (di=0; di<D; di++) {
		ind_rd[di] = di;
		for (j=0; j<J; j++) {
			ind_rk[di*J + j] = j;
		}
	}


	/* random initialization */
	for (di=0; di<D; di++) {
		for (i=jc[di]; i<jc[di + 1]; i++) {
			wi = (int) ir[i];
			xi = pr[i];
			xtot += xi;
			// pick a random topic 0..J-1
			topic = (int) (J*drand());
			mu[i*J + topic] = 1.0; // assign this word token to this topic
			phi[wi*J + topic] += xi; // increment phi count matrix
			theta[di*J + topic] += xi; // increment theta count matrix
			phitot[topic] += xi; // increment phitot matrix
		}
	}

	for (iter=0; iter<50; iter++) {
		/* passing message mu */
		/* iteration 0 */
		if (iter == 0) {
			for (di=0; di<D; di++) {
				for (i=jc[di]; i<jc[di + 1]; i++) {
					wi = (int) ir[i];
					xi = pr[i];
					mutot = 0;
					for (j=0; j<J; j++) {
						phi[wi*J + j] -= xi*mu[i*J + j];
						phitot[j] -= xi*mu[i*J + j];
						theta[di*J + j] -= xi*mu[i*J + j];	
						munew[j] = (phi[wi*J + j] + BETA)/(phitot[j] + WBETA)*(theta[di*J + j] + ALPHA);
						mutot += munew[j];
					}
					for (j=0; j<J; j++) {
						munew[j] /= mutot;
						rk[di*J + j] += xi*fabs(munew[j] - mu[i*J + j]);
						rd[di] += xi*fabs(munew[j] - mu[i*J + j]);
						mu[i*J + j] = munew[j];
						phi[wi*J + j] += xi*mu[i*J + j];
						phitot[j] += xi*mu[i*J + j];
						theta[di*J + j] += xi*mu[i*J + j];
					}
				}
				psort(rk + di*J, ind_rk + di*J, 0, J - 1, J2);
			}
			psort(rd, ind_rd, 0, D - 1, D2);

		} else { /* iteration > 0 */
			for (ii=0; ii<D2; ii++) {
				di = (int) ind_rd[ii];
				for (j=0; j<J2; j++) {				
					k = (int) ind_rk[di*J + j];
					rd[di] -= rk[di*J + k];
					rk[di*J + k] = 0.0;
				}
				for (i=jc[di]; i<jc[di + 1]; i++) {
					wi = (int) ir[i];
					xi = pr[i];
					for (j=0, mutot=0.0, totprob=0.0; j<J2; j++) {
						k = (int) ind_rk[di*J + j];
						phi[wi*J + k] -= xi*mu[i*J + k];
						phitot[k] -= xi*mu[i*J + k];
						theta[di*J + k] -= xi*mu[i*J + k];	
						totprob += mu[i*J + k];
						munew[k] = (phi[wi*J + k] + BETA)/(phitot[k] + WBETA)*(theta[di*J + k] + ALPHA);
						mutot += munew[k];
					}
					for (j=0; j<J2; j++) {
						k = (int) ind_rk[di*J + j];
						munew[k] /= mutot;
						munew[k] *= totprob;
						rk[di*J + k] += xi*fabs(munew[k] - mu[i*J + k]);
						mu[i*J + k] = munew[k];
						phi[wi*J + k] += xi*mu[i*J + k];
						phitot[k] += xi*mu[i*J + k];
						theta[di*J + k] += xi*mu[i*J + k];
					}
				}
				for (j=0; j<J2; j++) {
					k = (int) ind_rk[di*J + j];
					rd[di] += rk[di*J + k];
				}
				psort(rk + di*J, ind_rk + di*J, 0, J - 1, J2);
			}
			psort(rd, ind_rd, 0, D - 1, D2);
		}
		
		/* check the convergence condition */
		rsum = 0.0;
		for (di=0; di<D; di++) rsum += rd[di];
		if (rsum/xtot < TH) break;
	}
	
	free(theta);
	free(mu);
	free(ind_rk);
	free(ind_rd);
	free(munew);
	free(rk);
	free(rd);
}

/*==========================================
* main
*========================================== */
int main(int argc, char* argv[])
{
	int W, K, D, NNZ, SEED, m, s;
	int *ir, *jc;
	double TD, ALPHA, BETA;
	double TK;
	double TH;
	double *phi, *phitot, *pr;
	char *pch, mystring[MAXLEN];
	FILE *fp;

	K=100;                   //topic number
	//DS=1160362;                //document number

	TD=1;                    // accelerate velocity
	TK=1;                    // accelerate 
	TH=0.001;                // 收敛条件 
	ALPHA=0.01;              // 超参alpha
	BETA=0.01;               // 超参beta
	SEED=3;                  // random seed


	seedMT(SEED);

	// open document file
        
        printf("LDA\n");
	fp = fopen(argv[1], "r");        // file location

	if (fp == NULL) fprintf(stderr, "Text file cannot be found.\n");

	// read the file header
	fgets(mystring, sizeof(mystring), fp);

	// Unix file contains a special space at each line of the file
	pch = strtok(mystring, "	");
	if ((pch != NULL) && (atoi(pch) != 0)){
		D = atoi(pch);                                           // the number of document
		printf("#Document: %d \n", D);
	} else {
		fprintf(stderr, "File header error.\n");
	}

	pch = strtok(NULL, "	");
	if ((pch != NULL) && (atoi(pch) != 0)){
		W = atoi(pch);                                           // the number of word
		printf("#Vocabulary: %d \n", W);
	} else {
		fprintf(stderr, "File header error.\n");
	}

	pch = strtok(NULL, "	");
	if ((pch != NULL) && (atoi(pch) != 0)){
		NNZ = atoi(pch);                                         // the number of nozero 
		printf("#NNZ: %d \n", NNZ);
	} else {
		fprintf(stderr, "File header error.\n");
	}
	if (NNZ == 0) fprintf(stderr, "Empty file.\n");

	/* initializae global parameters */
	phitot  = dvec(K);
	phi     = dvec(K*W);


	// copy each mini-batch in the file to sparse matrix
	// run BP algorithm
	// allocate enough memory for each mini-batch
	// we assume that each fp contains ten times word indices than that on average
	jc     = ivec(D+1);
	ir     = ivec((int) (NNZ*100));         // initialize the space to store the word. 
	pr     = dvec((int) (NNZ*100));         // initialize the space to store the quality of word.

		
        /* read "D" docs from the file */
        NNZ = 0;
	for (s=0; s<D; s++) {			
	    jc[s] = NNZ;
	    if (fgets(mystring, sizeof(mystring), fp) == NULL) break;
	    pch = strtok(mystring, ":");
	    if((pch != NULL) && ( (atoi(pch)+1) != 0)) {    
		ir[NNZ] = atoi(pch);                         // the id of word
		pch = strtok(NULL, "	");
	        pr[NNZ] = atof(pch);                         // the number of word
		NNZ++;			
	     }
	     // Unix file contains a special space at each line of the file
	    while (pch != NULL) {
		pch = strtok(NULL, ":");
		if ((pch != NULL) && ( (atoi(pch)+1) != 0)) {   
		        ir[NNZ] = atoi(pch);                 // the id of word
			printf("doument:%d \t word:%d\n",s,atoi(pch));
			pch = strtok(NULL, "	");
			pr[NNZ] = atof(pch);                 // the number of word
			NNZ++;
		}
	    }
	}
	jc[s] = NNZ;

	/* run the learning algorithm */
	BP(ALPHA, BETA, W, K, s, pr, ir, jc, phi, phitot, NNZ, TD, TK, TH);


	fclose(fp);                                       // close file

	// final output
	// K x W matrix  K_w1 K_w2 ...
	write_dvec(K*W, K, W, phi, argv[2]);    // file storage       topic--word
	free(phi);                                        // free point
	free(phitot);                                     // free point
	free(ir);                                         // free point
	free(jc);                                         // free point
	free(pr);                                         // free point
}
