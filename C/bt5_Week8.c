#include <stdio.h>

int main(){
	printf("------CHUONG TRINH IN BANG CUU CHUONG-----\n");
	for(int i=1;i<10;i++){
		printf("\tBang cuu chuong %d\n",i);
		for(int j = 1;j<10;j++){
			printf("\t%d * %d = %d\n",i,j,i*j);
		}
		printf("\n");
	}
}
