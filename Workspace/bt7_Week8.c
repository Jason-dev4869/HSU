#include<stdio.h>

int main(){
	int x, p=0, temp;
	printf("Nhap so nguyen: ");
	scanf("%d",&x);
	for(int i=1;i<=x;i++){
		p=p*i; 
	} 
	printf("%d! = %d",x,p);
} 
