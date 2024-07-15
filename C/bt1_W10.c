#include <stdio.h>
#include <stdbool.h>
#define MAX 10

int count_neg(int a[], int n);
int sum(int a[],int n);
bool checkDoiXung(int a[], int n);
int TimX(int a[], int n);
int main(){
	int n;
	int a[MAX];
	printf("Nhap n: ");
	scanf("%d",&n);
	if(n>=1 && n<=MAX){
		for(int i=0;i<n;i++){
			printf("a[%d]:",i);
			scanf("%d",&a[i]);
		}
		printf("Xuat mang:\t");
		for(int i=0;i<n;i++){
			printf("%d\t",a[i]);
		}
	}
	else{
		printf("n khong lon hon %d",MAX);
	}
	printf("\nSo phan tu am trong mang la %d", count_neg(a,n));
	printf("\nTong so phan tu trong mang la %d", sum(a,n));
	if(checkDoiXung(a,n))
		printf("\nMang vua nhap doi xung nhau");
	else
		printf("\nMang vua nhap khong doi xung nhau");
	TimX(a,n);
}

int count_neg(int a[], int n){
	int count=0;
	for(int i=0;i<n;i++){
		if(a[i]<0)
			count+=1;
	}
	return count;
}

int sum(int a[],int n){
	int sum=0;
	for(int i=0;i<n;i++){
		sum+=a[i];
	}
	return sum;
}

bool checkDoiXung(int a[], int n){
    for(int i = 0;i<n/2;i++){
        if(a[i] != a[n-i-1]) 
			return false;
    } 
    return true;
}

int TimX(int a[], int n){
	int x,vitri;
	printf("\nNhap x can tim:");
	scanf("%d",&x);
	
    for(int i=0;i<n;i++){
    	if(a[i]==x){
        	vitri=i;
        	printf("Tim thay %d o vi tri %d\n",x,vitri);
		}
	}
	printf("Khong tim thay X");
	return vitri;
}
