#include <stdio.h>
struct Book{
	char BookName[20];
	int Quantity;
};
struct Book book[100];

void Input(struct Book b[], int n){
	for(int i=0; i<n; i++){
		printf("Nhap sach thu %d\n",i+1);
		printf("Ten sach: ");
		gets(b[i].BookName);
		printf("So luong :");
		scanf("%d",&b[i].Quantity);
		fflush(stdin);
	}
}

void Output(struct Book b[], int n){
	for(int i=0; i<n;i++)
		printf("%20s - %d\n",b[i].BookName,b[i].Quantity);
}

int main(){
	Input(book,5);
	Output(book,5);
}
