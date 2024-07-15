#include <stdio.h>
#include <stdlib.h>
int generateRandom(int a, int b);
void main(){
	int a[100], num;
	float x,f=0;
	
	printf("Nhap so phan tu trong mang:");
	scanf("%d", &num);
	printf("Nhap X:");
	scanf("%f",&x);
	for(int i=0; i<num;i++){
		a[i]=generateRandom(0,20);
	}
	printf("Xuat phan tu mang xuoi");
	for(int i=0; i<num;i++){
		printf("%d\t",a[i]);
	}
	printf("Xuat phan tu mang nguoc");
	for(int i=num-1; i>=0;i--){
		printf("%d\t",a[i]);
	}
}

int generateRandom(int a, int b){
	int n = a+rand()%(b+1-a);
	return n;
}
