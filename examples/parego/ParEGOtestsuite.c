/*
A suite of test functions for multiobjective optimization
(C) Joshua Knowles, 2004
Please contact me at j.knowles@man.ac.uk for any queries or corrections
See the technical report for further details: 
J. Knowles (2004) ParEGO: A Hybrid Algorithm with On-line Landscape Approximation 
for Expensive Multiobjective Optimization Problems.
Technical report TR-COMPSYSBIO-2004-01
IMPORTANT NOTICE:
In this file, x[1],...,x[n] refer to the decision variables (i.e. x[0] is NOT used).
Similarly, y[1],...,y[k] refer to the objective values (i.e. y[0] is NOT used). */


#include <math.h>
#define PI 3.141592654


double myabs(double v)
{
  if(v>=0.0)
    return v;
  else if (v < 0.0)
    return -v;
}

void f_dtlz1a(double *x, double *y)
{
  /* There are 2 objectives, 6 decision (x) variables. The x variables are in the range [0,1]. */

  int dim=6;

  double g = 0.0;
  for(int i=2;i<=dim;i++)
    g+= (x[i]-0.5)*(x[i]-0.5) - cos(2*PI*(x[i]-0.5)); // Note this is 20*PI in Deb's DTLZ1
  g += dim-1;
  g *= 100;

  y[1] = 0.5*x[1]*(1 + g);
  y[2] = 0.5*(1-x[1])*(1 + g);
}

void f_dtlz2a(double *x, double *y)
{

  /* There are 3 objectives, 8 decision (x) variables. The x variables are in the range [0,1]. */
  int dim=8;
  double alph=1.0

  double g = 0.0;
  for(int i=3;i<=dim;i++)
    g+=(x[i]-0.5)*(x[i]-0.5);


  y[1] = (1 + g)*cos(pow(x[1],alph)*PI/2)*cos(pow(x[2],alph)*PI/2);
  y[2] = (1 + g)*cos(pow(x[1],alph)*PI/2)*sin(pow(x[2],alph)*PI/2);
  y[3] = (1 + g)*sin(pow(x[1],alph)*PI/2);
}

void f_dtlz4a(double *x, double *y)
{

  /* There are 3 objectives, 8 decision (x) variables. The x variables are in the range [0,1]. */
  int dim=8;
  double alph=100.0

  double g = 0.0;
  for(int i=3;i<=dim;i++)
    g+=(x[i]-0.5)*(x[i]-0.5);


  y[1] = (1 + g)*cos(pow(x[1],alph)*PI/2)*cos(pow(x[2],alph)*PI/2);
  y[2] = (1 + g)*cos(pow(x[1],alph)*PI/2)*sin(pow(x[2],alph)*PI/2);
  y[3] = (1 + g)*sin(pow(x[1],alph)*PI/2);
}


void f_dtlz7a(double *x, double *y)
{

  /* There are 3 objectives, 8 decision (x) variables. The x variables are in the range [0,1]. */
  int dim=8;
  int nobjs=3;


  double g,h,sum;
  y[1]=x[1];
  y[2]=x[2];

  g = 0.0;
  for(int i=3;i<=dim;i++)
    {
      g+=x[i];
    }
  g*=9.0/(dim-nobjs+1);
  g+=1.0;
  
  sum=0.0;
  for(int i=1;i<=nobjs-1;i++)
    sum += ( y[i]/(1.0+g) * (1.0+sin(3*PI*y[i])) );
  h = nobjs - sum;
  
  y[3]=(1 + g)*h;
}

void f_vlmop3(double *x, double *y)
{
  
  /* There are 3 objectives, 2 decision (x) variables. The x variables are in the range [-3,3]. */

  y[1] = 0.5*(x[1]*x[1]+x[2]*x[2]) + sin(x[1]*x[1]+x[2]*x[2]);
  y[2] = pow(3*x[1]-2*x[2]+4.0, 2.0)/8.0 + pow(x[1]-x[2]+1, 2.0)/27.0 + 15.0;
  y[3] = 1.0 / (x[1]*x[1]+x[2]*x[2]+1.0) - 1.1*exp(-(x[1]*x[1]) - (x[2]*x[2]));
}


void f_oka1(double *x, double *y)
{

  /* There are 2 objectives, 2 decision (x) variables. The x variables are in the ranges:
  x[1] in [6*sin(PI/12.0), 6*sin(PI/12.0)+2*PI*cos(PI/12.0)]
  x[2] in [-2*PI*sin(PI/12.0), 6*cos(PI/12.0)]
  */
  
  double x1p = cos(PI/12.0)*x[1] - sin(PI/12.0)*x[2];
  double x2p = sin(PI/12.0)*x[1] + cos(PI/12.0)*x[2];
   
  y[1] = x1p;
  y[2] = sqrt(2*PI) - sqrt(myabs(x1p)) + 2 * pow(myabs(x2p-3*cos(x1p)-3) ,0.33333333);				       
}

void f_oka2(double *x, double *y)
{
  /* There are 2 objectives, 3 decision (x) variables. The x variables are in the ranges:
  x[1] in [-PI, PI]
  x[2] in [-5, 5]
  x[3] in [-5, 5]
  */
  y[1]=x[1];
  y[2]=1 - (1/(4*PI*PI))*pow(x[1]+PI,2) + pow(myabs(x[2]-5*cos(x[1])),0.333333333) + pow(myabs(x[3] - 5*sin(x[1])),0.33333333);

}

void f_vlmop2(double *x, double *y)
{
  /* x variables must be in the range [-2,2] */

  double sum1=0;
  double sum2=0;
  int dim = 2;

  for(int i=1;i<=2;i++)
    {
      sum1+=pow(x[i]-(1/sqrt(2.0)),2);
      sum2+=pow(x[i]+(1/sqrt(2.0)),2);
    }
       
  y[1] = 1 - exp(-sum1);
  y[2] = 1 - exp(-sum2);
}

void f_kno1(double *x, double *y)
{
  /* There are 2 objectives, 2 decision (x) variables. The x variables are in the range [0,3] */

  double f;
  double g;
  double c;

  
  c = x[1]+x[2];

  f = 20-( 11+3*sin((5*c)*(0.5*c)) + 3*sin(4*c) + 5 *sin(2*c+2));

  g = (PI/2.0)*(x[1]-x[2]+3.0)/6.0;

  y[1]= 20-(f*cos(g));
  y[2]= 20-(f*sin(g));

}
