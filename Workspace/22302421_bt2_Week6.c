#include <stdio.h>

/*22302421 - Nguyen Phuc Minh Chau
Nhap gio,phut,giay; Tinh tong so giay*/

int main(){
	int gio, phut, giay;
	printf("Nhap gio:");
	scanf("%d",&gio);
	
	printf("Nhap phut:");
	scanf("%d",&phut);
	
	printf("Nhap giay:");
	scanf("%d",&giay);
	
	printf("Tong so giay la: %d",gio*3600+phut*60+giay);
} 
