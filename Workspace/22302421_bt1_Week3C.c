#include <stdio.h>
#include <math.h>

int main(){
	int n;
	double x, z=0, k=0, t=0;
	printf("Nhap n:");
	scanf("%d",&n);
	printf("Nhap x:");
	scanf("%lf",&x);
	z = (2*x+sqrt(n))/13;
	t = 0.5*x*n+2.23*(pow(x,3));
	k = pow((pow(x,2)+x+1),n) + pow((pow(x,2)-x+1),n);
	printf("Z = %.2lf\n",z);
	printf("T = %.2lf\n",t);
	printf("K = %.2lf",k);
} 
