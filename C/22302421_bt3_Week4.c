#include <stdio.h>
#include <math.h>

int main(){
	//giai 
	int a,b,c;
	float delta,x,x1,x2;
	printf("Nhap a: ");
	scanf("%d",&a);
	printf("Nhap b: ");
	scanf("%d",&b);
	printf("Nhap c: ");
	scanf("%d",&c);
	if(a==0){
		if(b==0){
			if(c==0){
				printf("Phuong trinh vo so nghiem");
			} else{
				printf("Phuong trinh vo nghiem");
			}
		} else{
			x=-c/b;
			printf("x=%.1f",x);
		}
	} else{
		delta=b*b-4*a*c;
		if(delta>0){
			x1=(-b+sqrt(delta))/2*a;
			x2=(-b-sqrt(delta))/2*a;
			printf("phuong trinh co hai nghiem\nx1 = %.2f\nx2 = %2.f",x1,x2);
		}
		if(delta==0){
			x=-b/2*a;
			printf("phuong trinh co nghiem kep\nx1 = x2 = %.2f",x);
		} 
		if(delta<0){
			printf("phuong trinh vo nghiem");
		}
	}
}
