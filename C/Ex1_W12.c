#include<stdio.h>

int main(){
	float a[4] = {0.5,1.5,3.5,5.7};
	float *p;
	p = a;
	printf("Gia tri cua a[3]:%.1f\n",a[3]);
	printf("Gia tri cua p[3]:%.1f\n",p[3]);
	printf("Gia tri cua *(a+3):%.1f\n",*(a+3));
	printf("Gia tri cua *(p+3):%.1f\n",*(p+3));
	
	printf("\nDia chi cua a[0]:%d\n",&a[0]);
	printf("Dia chi cua a[1]:%d\n",&a[1]);
	printf("Dia chi cua a[2]:%d\n",&a[2]);
	printf("Dia chi cua a[3]:%d\n",&a[3]);
	printf("Dia chi cua con tro p: %d",&p);
}
