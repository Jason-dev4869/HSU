#include <stdio.h>
#define PI 3.14

int main(){
	//Nhap ban kinh, tinh chu vi, dien tich
	int r;
	float CV,S;
	printf("Nhap ban kinh r: ");
	scanf("%d",&r);
	if(r>0){
		CV = 2*PI*r;
		S = PI*r*r;
		printf("Chu vi hinh tron: %.2f \nDien tich hinh tron: %.2f", CV, S);
	} else{
		printf("Ban kinh be hon 0, khong the tinh duoc");
	}
	return 0;
}
