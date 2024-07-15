#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generateRandomArray(float a[], int size, float min, float max) {
    for (int i = 0; i < size; ++i) {
        a[i] = ((float)rand() / RAND_MAX) * (max - min) + min;
    }
}

int isSubarray(float a1[], int size1, float a2[], int size2) {
    for (int i = 0; i <= size1 - size2; ++i) {
        int j;
        for (j = 0; j < size2; ++j) {
            if (a1[i + j] != a2[j]) {
                break;
            }
        }
        if (j == size2) {
            return 1;  
        }
    }
    return 0; 
}

int main() {
    srand((unsigned int)time(NULL));

    const int size1 = 100;
    const int size2 = 10;

    float a1[size1];
    float a2[size2];

    generateRandomArray(a1, size1, 1.0, 5.0);

    printf("Mang goc:\n");
    for (int i = 0; i < size1; ++i) {
        printf("%.2f ", a1[i]);
    }
    printf("\n");

    for (int i = 0; i < size2; ++i) {
        a2[i] = a1[i + 20];  
    }

    if (isSubarray(a1, size1, a2, size2)) {
        printf("Mang con la mang con cua mang goc");
    } else {
        printf("Mang con khong la mang con cua mang goc");
    }
}

