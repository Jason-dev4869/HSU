#include <stdio.h>

int main(){
	int n=10;
	int *p;
	p = &n;
	printf("Gia tri cua bien N: %d\n",n);
	printf("Dia chi cua bien N: %d\n",&n);
	printf("Dia chi cua con tro p: %d\n",&p);
	printf("Gia tri cua con tro p qua N: %d\n",*p);
	*p=100;//thay doi gia tri
	printf("Gia tri cua bien N: %d",n);
} 
