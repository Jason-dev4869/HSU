#include <stdio.h>

int main(){
	int n,s;
	do{
		printf("Nhap so nguyen duong N: ");
		scanf("%d",&n);
		s+=n;
	}while(n>0);
	printf("Tong cac so vua nhap la %d",s);
}
