#include<stdio.h>
int main()
{
    /*
    int num1,num2,sum=0;
    printf("Enter number 1:\n");
    scanf("%d",&num1);
    printf("Enter number 2:\n");
    scanf("%d",&num2);
    sum=num1+num2;
    printf("The result of num 1: %d and num2: %d is %d",num1,num2,sum);
    return 0;*/
    float num1,num2,sum=0;
    printf("Enter number 1:\n");
    scanf("%f",&num1);
    printf("Enter number 2:\n");
    scanf("%f",&num2);
    sum=num1+num2;
    printf("The result of num 1: %.1f and num2: %.1f is %.1f",num1,num2,sum);
    return 0;

}