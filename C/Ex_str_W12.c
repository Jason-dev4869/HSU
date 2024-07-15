#include <stdio.h>
#include <ctype.h>
int main(){
	char name[50];
	int len=0;
	int i = 0;
	
	printf("Nhap ten:");
	gets(name);
	printf("In ten: ");
	puts(name);
	len = strlen(name);
	printf("So ki tu co trong ten: %d\n",strlen(name));
	printf("So ki tu co trong ten: %d\n",len);
	
	while(name[i]!=NULL){
		name[i]=toupper(name[i]);
		i++;
	}
	printf("In ten in hoa:%s\n",name);
	
	/*for(i=0;i<len;i++){
		printf("%c\n",name[i]);
	}*/
	int j=0;
	while(name[j]!=NULL){
		printf("%c\n",name[j++]);
	}
	
	int k=0;
	int countabc=0, countnum=0, countother=0;
	while(name[k]!=NULL){
		if(isalpha(name[k])){
			countabc++;
		}
		if(isdigit(name[k])){
			countnum++;
		}
		k++;
	}
	countother = len - (countabc + countnum);
	printf("So ki tu chu: %d\n",countabc);
	printf("So ki tu so: %d\n",countnum);
	printf("So ki tu dac biet: %d",countother);
} 
