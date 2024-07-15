#include <stdio.h>

int main(){
	int a,b,tong,hieu,tich,thuong;
	printf("Nhap so a:");
	scanf("%d",&a);
	printf("Nhap so b:");
	scanf("%d",&b);
	tong=a+b;
	printf("\nTong cua hai so %d va %d la %d\n",a,b,tong);
	hieu=a-b;
	printf("Hieu cua hai so %d va %d la %d\n",a,b,hieu);
	tich=a*b;
	printf("Tich cua hai so %d va %d la %d\n",a,b,tich);
	if(a==0 || b==0){
		printf("Khong the chia duoc cho 0");
	} else {
		thuong=a/b;
		printf("Thuong cua hai so %d va %d la %d",a,b,thuong);
	}
	return 0;
}
