#include <stdio.h>
#include <math.h>

int main(){
	float sl,dg,gg,cvc,kq,tt;
	printf("Nhap so luong: ");
	scanf("%f",&sl);
	printf("Nhap don gia: ");
	scanf("%f",&dg);
	tt = sl*dg;
	gg = tt*0.12;
	cvc = tt*0.05;
	kq = tt-gg+cvc;
	printf("So tien phai tra la %.2f",kq);
}
