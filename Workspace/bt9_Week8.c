#include <stdio.h>
#include <math.h>

int main(){
	int n, count=0;
	do{
		printf("Nhap so nguyen duong N: ");
		scanf("%d",&n);
	}while(n<=0);
	if(n>=2){
		for(int i=2;i<=sqrt(n);i++){
			if(n%i==0)
				count++;
		}
		if(count==0){
			printf("%d la so nguyen to",n);
		}
		else{
			printf("%d khong phai so nguyen to",n);
		}
	}
	else{
		printf("%d khong phai so nguyen to",n);
	}
}
