#include <stdio.h>

int main() {
    int n;

    printf("nhap N: ");
    scanf("%d", &n);
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("* ");
        }
        printf("\n");
    }
    printf("-----------------\n");
	for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++) {
            printf("* ");
        }
        printf("\n");
    }
	printf("-----------------\n");
	for (int i = 1; i <= n; i++) {
        for (int j = i; j < n; j++) {
            printf(" ");
        }
		for (int j = 1; j <= (2*i-1); j++) {
            printf("*");
        }
        printf("\n");
    } 
}

