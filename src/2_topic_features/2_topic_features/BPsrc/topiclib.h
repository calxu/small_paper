#ifndef _TOPICLIB_H_
#define _TOPICLIB_H_
 
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <time.h>

typedef unsigned long uint32;

#define drand() (randomMT()/4294967296.0)

void seedMT(uint32 seed);
inline uint32 randomMT(void);
uint32 reloadMT(void);

int *ivec(int n); //
double *dvec(int n); //
int partition(double *x, int *indx, int left, int right, int pivotIndx); //
void psort(double *x, int *indx, int left, int right, int k); //
void write_dvec (int n, int nrow, int ncol, double *x, char *fname); //
double etime(); //

#endif
