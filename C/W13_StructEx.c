#include <conio.h>
#include <stdio.h>
struct Student
{   char Name[15];
     int Age;
};
void main()
{	
	struct Student sv;
	printf("Nhap ho ten:"); 
	gets(sv.Name);
	printf("Nhap tuoi: "); 
	scanf("%d", &sv.Age);

	printf("%s %d", sv.Name, sv.Age);
	getch();
}

