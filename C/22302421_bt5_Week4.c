#include <stdio.h>
int main(){
	int n,i;
	float x, T = 1, S = 0;
	printf("Nhap so thuc X:");
	scanf("%f",&x);
	printf("Nhap so nguyen N:");
	scanf("%d",&n);
	for(i = 1; i<=n; i++){
		T *= x;
		S += T;
	}
	printf("S = %.1f",S);
}
