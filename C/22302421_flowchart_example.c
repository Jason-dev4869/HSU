#include <stdio.h>

int main(){
	float Diem;
	printf("Nhap Diem mon CSLT cua ban: ");
	scanf("%f",&Diem);
	
	if(Diem>=5){
		printf("Vi diem cua ban la %.1f nen ban Dau", Diem);
	} else{
		printf("Vi diem cua ban la %.1f nen ban Rot", Diem);
	}
	
	return 0;
} 
