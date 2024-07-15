#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int random(int minN, int maxN) {
    return minN + rand() % (maxN + 1 - minN);
}

int main() {
    srand((unsigned int)time(NULL));

    int N;
    printf("Nhap so phan tu cua mang: ");
    scanf("%d", &N);

    int a[N];
    for (int i = 0; i < N; ++i) {
        a[i] = random(-100, 100);
    }
    for (int i = 0; i < N; ++i) {
        printf("%d ", a[i]);
    }
    printf("\n");

    int minSum = a[0] + a[1];
    int minIndex = 0;

    for (int i = 1; i < N - 1; ++i) {
        int currentSum = a[i] + a[i + 1];
        if (abs(currentSum) < abs(minSum)) {
            minSum = currentSum;
            minIndex = i;
        }
    }

    printf("Vi tri cua 2 phan tu lien nhau co tong gia tri tuyet doi nho nhat la: %d va %d\n", minIndex, minIndex + 1);
    printf("Gia tri cua 2 phan tu do la: %d va %d", a[minIndex], a[minIndex + 1]);
}

