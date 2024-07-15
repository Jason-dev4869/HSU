#include <stdio.h>

int main(){
	int n,s=0;
	do{
		printf("Nhap so nguyen duong N: ");
		scanf("%d",&n);
	}while(n<=0);
	for(int i=1;i<n;i++){
		if(n%i==0){
			s=s+i;
		}
	}
	if(s==n){
		printf("%d la so hoan thien",n);
	}
	else{
		printf("%d khong phai la so hoan thien",n);
	}
}
