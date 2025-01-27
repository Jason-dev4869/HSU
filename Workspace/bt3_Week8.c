#include<stdio.h>

int main(){
	int n;
	do{
		printf("Nhap so nguyen duong N: ");
		scanf("%d",&n);
	}while(n<=0);
	for(int i=1;i<n;i++){
		if(n%i==0){
			printf("\t%d",i);
		}
	}
}
