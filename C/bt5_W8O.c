#include <stdio.h>

int main(){
	int n;
	do{
		printf("------------\n");
		printf("1. bai tap 1\n");
		printf("2. bai tap 2\n");
		printf("3. bai tap 3\n");
		printf("4. bai tap 4\n");
		printf("5. bai tap 5\n");
		printf("6. Exit\n");
		printf("------------\n");
		printf("Nhap bai muon chon:");
		scanf("%d",&n);
		switch(n){
			case 1:
				printf("Thuc hien bai tap 1");
				break;
			case 2:
				printf("Thuc hien bai tap 2");
				break;
			case 3:
				printf("Thuc hien bai tap 3");
				break;
			case 4:
				printf("Thuc hien bai tap 4");
				break;
			case 5:
				printf("Thuc hien bai tap 5");
				break;
			default:
				printf("Khong co bai nay. Vui long nhap lai\n");
		}
	} while(n<1 || n>5);
}
