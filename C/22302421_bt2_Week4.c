#include <stdio.h>

int main(){
	//Giai phuong trinh bac 1, ax+b=0; ==> x=-b/a
	int a,b;
	float x;
	printf("Nhap so nguyen a: ");
	scanf("%d",&a);
	printf("Nhap so nguyen b: ");
	scanf("%d",&b);
	if(a==0){
		if(b==0){
			printf(" Phuong trinh vo so nghiem");
		} else{
			printf("Phuong trinh vo nghiem");
		}
	}else{
		//ep kieu x=(float)-b/a; x=1.0*-b/a
		x=-b/a;
		printf("x = %.1f",x);
	}
}
