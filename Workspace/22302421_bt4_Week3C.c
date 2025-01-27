#include <stdio.h>

int main(){
	int n,dv,chc;
	do{
		printf("Nhap so duong co hai chu so: ");
		scanf("%d",&n);
	}while(100<n || n<10);
	dv=n%10;
	chc=n/10;
	printf("Tong hai so cong lai la %d",dv+chc);
}
