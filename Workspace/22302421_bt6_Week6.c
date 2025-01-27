#include <stdio.h>
#include <math.h>

/*22302421 - Nguyen Phuc Minh Chau
Tinh chu vi hinh thang can*/

int main(){
	float a,b,c,h,l;
	printf("Nhap day nho: ");
	scanf("%f",&a);
	printf("Nhap day lon: ");
	scanf("%f",&b);
	printf("Nhap chieu cao:");
	scanf("%f",&h);
	if(b>a){
		l = (b-a)/2;
		c = sqrt(l*l+h*h);
		printf("Chu vi hinh thang can la %.2f",a+b+(2*c));
	}
	else{
		printf("Chu y: Day nho phai be hon day lon");
	}
}
