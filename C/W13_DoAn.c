#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct DoB{
	int day;
	int month;
	int year;
};

struct Score{
	float Mth;
	float Phi;
	float Eng;
	float Aveg;
	char Rate[20];
};

struct Students{
	char St_code[10];
	char Class[10];
	char Fullname[100];
	char Address[100];
	struct DoB date;
	struct Score sc;
};

void Input_Info(struct Students st[], int* n){
	printf("Enter the number of students: ");
	scanf("%d", n);
	
	for(int i=0;i< *n;i++){
		fflush(stdin);
		printf("\n=====Student Info=====\n");
		printf("Student code: ");
		gets(st[i].St_code);
		printf("Class: ");
		gets(st[i].Class);
		printf("Full name: ");
		gets(st[i].Fullname);
		printf("Address: ");
		gets(st[i].Address);
		fflush(stdin);
		printf("Date of Birth [dd mm yyyy]: ");
		scanf("%d %d %d",&st[i].date.day, &st[i].date.month, &st[i].date.year);
		
		printf("======Input Score======\n");
		printf("Math: ");
		scanf("%f",&st[i].sc.Mth);
		printf("Philosophy: ");
		scanf("%f",&st[i].sc.Phi);
		printf("English: ");
		scanf("%f",&st[i].sc.Eng);
		
		st[i].sc.Aveg = (st[i].sc.Mth + st[i].sc.Phi + st[i].sc.Eng)/3;
		if(st[i].sc.Aveg >= 8)
			strcpy(st[i].sc.Rate,"Excellent");
		else if(st[i].sc.Aveg >= 7)
			strcpy(st[i].sc.Rate,"Good");
		else if(st[i].sc.Aveg >= 5)
			strcpy(st[i].sc.Rate,"Average");
		else
			strcpy(st[i].sc.Rate,"Poor");
		printf("Average Score: %.2f\n",st[i].sc.Aveg);
		printf("Rate: %s\n",st[i].sc.Rate);
	}
}

void Output_Info(struct Students st[], int n){
	printf("====== Student List ======\n");
	printf("| %25s | %10s | %10s | %15s | %10s | %5s | %10s |\n","Name","Class","Stu Code","Address","Birth Date","Avg Score","Rate");
	
	for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (strcmp(st[j].Fullname, st[j + 1].Fullname) > 0) {
                struct Students temp = st[j];
                st[j] = st[j + 1];
                st[j + 1] = temp;
            }
        }
    }
	
	for(int i=0;i<n;i++){
		printf("| %25s | %10s | %10s | %15s | %2d-%2d-%4d | %.2f\t | %10s |\n",st[i].Fullname,st[i].Class,st[i].St_code,st[i].Address,st[i].date.day,st[i].date.month,st[i].date.year,st[i].sc.Aveg,st[i].sc.Rate);
	}
}

void Find_Stcode(struct Students st[], int n){
	fflush(stdin);
	struct Students arrFound[100];
	int count = 0;
	char fstc[15];
	printf("Enter Student code you want to find: ");
	gets(fstc);
	
	for(int i=0;i<n;i++){
		if(strcmp(st[i].St_code, fstc)==0){
			arrFound[count++] = st[i];
		}
	}
	if(count > 0)
		Output_Info(arrFound,count);
	else
		printf("No students found with student code like %s.\n",fstc);
}

void Find_Class(struct Students st[], int n){
	fflush(stdin);
	struct Students arrFound[100];
	int count = 0;
	char fcls[15];
	printf("Enter class you want to find: ");
	gets(fcls);
	
	for(int i=0;i<n;i++){
		if(strcmp(st[i].Class, fcls)==0){
			arrFound[count++] = st[i];
		}
	}
	if(count > 0)
		Output_Info(arrFound,count);
	else
		printf("No students found with class %s.\n",fcls);
}

void Display_Rate(struct Students st[], int n){
	fflush(stdin);
	struct Students arrFound[100];
	int count = 0;
	char fr[15];
	printf("=====Select Rate=====\n");
	printf("E. Excellent\n");
	printf("G. Good\n");
	printf("A. Average\n");
	printf("P. Poor\n");
	printf("Enter class you want to find: ");
	gets(fr);
	
	if(strcmp(fr, "E") == 0)
		strcpy(fr,"Excellent");
	else if(strcmp(fr, "G") == 0)
		strcpy(fr,"Good");
	else if(strcmp(fr, "A") == 0)
		strcpy(fr,"Average");
	else if(strcmp(fr, "P") == 0)
		strcpy(fr,"Poor");
	else
		printf("Can't find any Rate have letter like %s\n",fr);
	
	for(int i=0;i<n;i++){
		if(strcmp(st[i].sc.Rate, fr)==0){
			arrFound[count++] = st[i];
		}
	}
	if(count > 0)
		Output_Info(arrFound,count);
	else
		printf("No students found with the selected rate.\n");
}

int main(){
	int m=0, choice;
	struct Students sv[100];
	
	do{
		//system("CLS");
		printf("==========CSLT==========\n");
		printf("1. Input Student List\n");
		printf("2. Display Student List\n");
		printf("3. Find Student Info [base on Student Code]\n");
		printf("4. Find Student [base on Class]\n");
		printf("5. Display List [base on Rate]\n");
		printf("6. Exit\n");
		printf("========================\n");
		printf("Select Number: ");
		scanf("%d",&choice);
		
		switch(choice){
			case 1:
				Input_Info(sv,&m); 
				break;
			case 2:
				Output_Info(sv,m);
				break;
			case 3:
				Find_Stcode(sv,m);
				break;
			case 4:
				Find_Class(sv,m);
				break;
			case 5:
				Display_Rate(sv,m);
				break;
			case 6:
				printf("Goodbye and have a nice day !"); 
		}
	}while(choice!=6);
}
