#include <iostream>
using namespace std;
#include <stdlib.h>
typedef int DATA;
#include "Queue.h"
#define MAX 10

void CreateArr(int a[], int n){
	for(int i = 0; i < n; i++)
		a[i] = rand();
}

void PrintArr(int a[], int n){
	for(int i = 0; i<n; i++)
		cout<<a[i]<<"\t";
	cout<<endl;
}

int FindMax(int a[], int n){
	int max = a[0];
	for(int i = 1; i < n; i++)
		if(max<a[i]) max = a[i];
	return max;
}

void CountingSort(int a[], int n, int exp){
	LQUEUE Bucket[10];
	for(int i = 0; i < 10; i++)
		Initialize(Bucket[i]);
	
	for(int i = 0; i < n; i++)
		Enqueue(Bucket[a[i]/exp%10], a[i]);
	
	int k = 0;
	for(int i = 0; i < 10; i++){
		while(!isEmpty(Bucket[i])){
			a[k++] = Dequeue(Bucket[i]);
		}
	}
	PrintArr(a, n);
}

void RadixSort(int a[], int n){
	int max = FindMax(a,n);
	int exp = 1;
	while(max>0){
		CountingSort(a, n, exp);
		max = max / 10;
		exp = exp * 10;
	}
}

int main(){
	LQUEUE q;
	Initialize (q);
	
	int a[MAX], n=MAX;
	CreateArr(a,n);
	RadixSort(a,n);
	
}