#include <stdio.h>

/*22302421 - Nguyen Phuc Minh Chau
Bang cuu chuong cua N*/

int main(){
	int n,i;
	printf("Nhap so nguyen N:");
	scanf("%d",&n);
	if(n>0 && n<=10){
		for(i=1;i<=10;i++){
			printf("%d * %d = %d\n",n,i,n*i);
		}
	}
	else{
		printf("Chu y: N phai lon hon 0 va be hon hoac bang 10");
	}
}
