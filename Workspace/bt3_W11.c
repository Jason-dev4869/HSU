#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

bool isPrime(int n) {
    if (n <= 1) {
        return false;
    }
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

int sumOfPrimes(int a[], int N) {
    int sum = 0;
    for (int i = 0; i < N; ++i) {
        if (isPrime(a[i])) {
            sum += a[i];
        }
    }
    return sum;
}

int main() {
    srand((unsigned int)time(NULL));

    int N;
    do{
    	printf("Nhap so phan tu cua mang: ");
		scanf("%d", &N);
	}while(N<=0 || N>1000);

    int a[N];
    for (int i = 0; i < N; ++i) {
        a[i] = rand() % 1000 + 1;
    }

    for (int i = 0; i < N; ++i) {
        printf("%d ", a[i]);
    }
    printf("\n");

    printf("Tong cac phan tu la so nguyen to: %d", sumOfPrimes(a, N));
}

