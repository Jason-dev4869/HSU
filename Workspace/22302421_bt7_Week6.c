#include <stdio.h>

/*22302421 - Nguyen Phuc Minh Chau
Gia tri lon nhat, gia tri nho nhat*/

int main(){
	int a,b,c,d,max,min;
	printf("Nhap lan luot 4 so a b c d: ");
	scanf("%d %d %d %d",&a,&b,&c,&d);
	max = (a>b) ? a:b;
	max = (max>c) ? max:c;
	max = (max>d) ? max:d;
	
	min = (a<b) ? a:b;
	min = (min<c) ? min:c;
	min = (min<d) ? min:d;
	printf("Max la %d\nMin la: %d", max, min);
}
