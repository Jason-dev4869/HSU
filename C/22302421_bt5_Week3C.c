#include <stdio.h>
#include <math.h>

int main(){
	int n;
	float x;
	printf("Nhap so nguyen n: ");
	scanf("%d",&n);
	printf("Nhap so thuc x: ");
	scanf("%f",&x);
	printf("Can bac n cua x la %.2f",pow(x,1.0/n));
} 
