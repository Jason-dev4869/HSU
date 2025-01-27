#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int randomInRange(int min, int max);
void printArray(int arr[], int n);
int unshiftArray(int arr[],int n,int a);
int pushArray(int arr[],int n, int b);

int main(){
	srand(time(0));
	int n, a, b, c, x, arr[100];
	
	do{
		printf("Nhap so phan tu cua mang:");
		scanf("%d",&n);
		if(n<=0){
			printf("Nhap sai, so phan tu trong mang phai lon hon 0!\n");
		}
	}while(n<=0);
	for(int i=0;i<n;i++){
		arr[i] = randomInRange(-10,10);
	}
	printf("- Cac phan tu cua mang la: \n");
    printArray(arr, n);
    printf("\n");
    
	printf("- Them 1 phan tu vao dau mang\n");
    printf("\tNhap phan tu can them: ");
    scanf("%d",&a);
	n = unshiftArray(arr,n,a);
    printf("\tCac phan tu cua mang la: \n");
    printArray(arr, n);
    printf("\n");
    
    printf("- Them 1 phan tu vao cuoi mang\n");
    printf("\tNhap phan tu can them: ");
    scanf("%d", &b);
    n = pushArray(arr,n,b);
    printf("\tCac phan tu cua mang la: \n");
    printArray(arr, n);
    printf("\n");
    
    printf("- Them 1 phan tu vao vi tri bat ki trong mang\n");
    printf("\tNhap phan tu can them: ");
    scanf("%d", &c);
    n = insertAtRandomIndex(arr, n, c);
    printf("\tCac phan tu cua mang la: \n");
    printArray(arr, n);
    printf("\n");
    
    printf("- Xoa phan tu dau tien trong mang co gia tri bang x\n");
    printf("\tNhap x can tim: ");
    scanf("%d", &x);
}

int randomInRange(int min, int max){
	return (rand() % (max - min + 1)) + min;
}

void printArray(int arr[], int n)
{
    for (int i = 0; i < n; i++)
        printf("%5d ", arr[i]);
}

int unshiftArray(int arr[],int n,int a){
	for(int i = n;i>0;i--){
		arr[i] = arr[i-1];
	}
	arr[0]=a;
	return n + 1;
}

int pushArray(int arr[],int n, int b){
	arr[n]=b;
	return n + 1;
}

int insertAtRandomIndex(int arr[],int n,int c){
	int indexToInsert=randomInRange(0,n);
	for(int i = n + 1; i > indexToInsert;i--)
		arr[i] = arr[i-1];
	arr[indexToInsert]=c;
	return n + 1;
}

int deleteAtIndex(int arr[], int n, int index)
{
    for (int i = index; i < n - 1; i++)
        arr[i] = arr[i + 1]; 
    return n - 1;
}

