#include<stdio.h>

int main(){
	int n, s=0;
	do{
		printf("Nhap so nguyen N: ");
		scanf("%d",&n);
	}while(n<=0);
	for(int i=1;i<=n;i+=2){
		s=s+i;
	}
	printf("Tong cac so nguyen duong le nho hon hoac bang %d: %d",n,s);
} 
