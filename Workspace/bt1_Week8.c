#include<stdio.h>

int main(){
	int n, count = 0;
	do{
		printf("Nhap so nguyen duong N: ");
		scanf("%d",&n);
	}while(n<=0);
	for(int i=1;i<=n;i+=2){
		printf("\t%d",i);
		count++;
		if(count==5){
			printf("\n");
			count = 0;
		}
	}
} 
