#include <stdio.h>
int main() {
    int n;
    do {
    	printf("Nhap n:");
    	scanf("%d",&n);
    	if (n<=0){
    		printf("moi nhap so lon hon 0\n");
		}
    }
    while (n<= 0);
    printf("%d so nguyen to dau tien:\n",n);
    int k=1;
    for (int i = 2;; i++) {
    	if (k>n)
    		break;
    	int t = 0;
       for (int j = 1; j <= i; j++)
       	if ((i % j) == 0)
          	t++;
       if (t == 2)
       	{
          	printf("%d\t", i);
          	k++;
          }
     }
    return 0;
}
