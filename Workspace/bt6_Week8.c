#include <stdio.h>
#include <math.h>
 
int main()
{
    int m, n;
    printf("Nhap co so m: ");
    scanf("%d", &m);
    printf("Nhap so mu n: ");
    scanf("%d", &n);
    int kq = pow(m,n);
    printf("%d ^ %d = %d", m, n, kq);
}
