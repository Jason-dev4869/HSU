#include <stdio.h>

int main(){
	int a,b,c,d,min;
	printf("Nhap ln lt so a b c d: ");
	scanf("%d %d %d %d",&a,&b,&c,&d);
	min = (a<b) ? a:b;
	min = (min<c) ? min:c;
	min = (min<d) ? min:d;
	printf("So nho nhat la %d",min);
}
