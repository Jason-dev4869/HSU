#include <stdio.h>

int main(){
	printf("BANG CHU HOA XUOI\n");
	for(char i = 'A'; i<='Z';i++){
		printf("%c\t",i);
	}
	printf("\nBANG CHU HOA NGUOC\n");
	for(char i = 'Z'; i>='A';i--){
		printf("%c\t",i);
	}
	printf("\nBANG CHU THUONG XUOI\n");
	for(char i = 'a'; i<='z';i++){
		printf("%c\t",i);
	}
	printf("\nBANG CHU THUONG NGUOC\n");
	for(char i = 'z'; i>='a';i--){
		printf("%c\t",i);
	}
} 
