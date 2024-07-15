#include <stdio.h>
int max(int a, int b, int c);
int main(){
	int a,b,c;
	max(a, b, c);
}

int max(int a, int b, int c){
	int m;
	printf("Nhap 3 so lan luot a b c:");
	scanf("%d %d %d",&a,&b,&c);	
	m=(a>b)?a:b;
	m=(m>c)?m:c;
	printf("so lon nhat 3 so la: %d",m);
}
