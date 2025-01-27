#include<stdio.h>
int nhan2so(int a, int b);
int cong2so(int a, int b);

void main(){
	int x,y;
	printf("Nhap x,y: ");
	scanf("%d %d",&x,&y);
	printf("%d + %d = %d\n",x,y,cong2so(x,y));
	printf("%d * %d = %d\n",x,y,nhan2so(x,y));
}

int nhan2so(int a, int b){
	return(a*b);
}

int cong2so(int a, int b){
	return(a+b);
}
