#include <stdio.h>
int max(int a, int b, int c, int d);
int main(){
	int a,b,c,d;
	max(a, b, c, d);
}

int max(int a, int b, int c, int d){
	int m;
	printf("Nhap 4 so lan luot a b c d:");
	scanf("%d %d %d %d",&a,&b,&c,&d);	
	m=(a>b)?a:b;
	m=(m>c)?m:c;
	m=(m>d)?m:d;
	printf("so lon nhat 4 so la: %d",m);
}
