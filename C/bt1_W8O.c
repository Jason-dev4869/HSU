#include <stdio.h>
int main(){
	int n;
	do{
		printf("Nhap so N:");
		scanf("%d",&n);
		if(n<0 || n>10){
			printf("0 < N <= 10\n");
		}
	}while(n<0 || n>10);
	for(int i=1;i<=10;i++){
		printf("%d * %d = %d\n",n,i,n*i);
	}
}
