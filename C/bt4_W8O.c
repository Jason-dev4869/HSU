#include <stdio.h>

int main(){
	int n, s=1;
	do{
		printf("Nhap N:");
		scanf("%d",&n);
		if(n<1){
			printf("Vui long nhap lai\n");
		}
	}while(n<1);
	for(int i=1;i<=n;i++){
		s*=i;
	}
	printf("%d! = %d",n,s);
}