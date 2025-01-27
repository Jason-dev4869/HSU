#include <stdio.h>
#define PI 3.14 //dinh dang gia tri PI la 3.14

/*22302421 - Nguyen Phuc Minh Chau
Nhap ban kinh r, tinh va in dien tich hinh tron*/
 
int main(){
	int r;
	printf("Nhap ban kinh r:");
	scanf("%d",&r);
	printf("Dien tich hinh tron la %.2f",(float)r*r*PI);
}
