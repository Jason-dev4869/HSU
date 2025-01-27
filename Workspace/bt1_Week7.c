#include <stdio.h>

int main(){
	int n;
	printf("Nhap so n: ");
	scanf("%d", &n);
	if(n%3==0){
		printf("%d chia het cho 3",n);
	} else{
		printf("%d khong chia het cho 3",n);
	}
}
