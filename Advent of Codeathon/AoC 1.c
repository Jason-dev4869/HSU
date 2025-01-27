#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int length;
} Subsequence;

void findIncreasingSubsequences(int arr[], int n, Subsequence *result, int *resultCount) {
    int start = 0;
    int count = 0;

    for (int i = 0; i < n - 1; i++) {
        if (arr[i] >= arr[i + 1]) {
            if (i - start >= 1) {
                result[count].data = &arr[start];
                result[count].length = i - start + 1;
                count++;
            }
            start = i + 1;
        }
    }

    // Check the last subsequence
    if (n - start >= 2) {
        result[count].data = &arr[start];
        result[count].length = n - start;
        count++;
    }

    *resultCount = count;
}

int main() {
    int n;
    scanf("%d", &n);

    Subsequence *result = (Subsequence *)malloc(n * sizeof(Subsequence));
    int resultCount;

    int batchSize = 1000;
    int *arr = (int *)malloc(batchSize * sizeof(int));

    int totalResults = 0;

    for (int i = 0; i < n; i += batchSize) {
        int readSize = (i + batchSize < n) ? batchSize : (n - i);
        for (int j = 0; j < readSize; j++) {
            scanf("%d", &arr[j]);
        }

        findIncreasingSubsequences(arr, readSize, result + totalResults, &resultCount);
        totalResults += resultCount;
    }

    for (int k = 0; k < totalResults; k++) {
        for (int j = 0; j < result[k].length; j++) {
            printf("%d ", result[k].data[j]);
        }
        printf("\n");
    }

    free(arr);
    free(result);

    printf("Nh?n b?t k? phím ð? thoát...");
    getchar(); // Ð?i ngý?i dùng nh?n phím
    return 0;
}

