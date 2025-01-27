#include<stdio.h>

void hoanvi(int a, int b){
	int temp;
	temp = a;
	a = b;
	b = temp;
}

void main(){
	int x=1, y = 2;
	hoanvi(x,y);
	printf("x = %d, y = %d",x,y);
}
