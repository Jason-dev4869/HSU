#include <iostream>
#define MAX 100
using namespace std;

void GenerateArray(int a[], int&n){
	do{
		cout << "Enter number of value want to use: ";
		cin >> n;
	}while(n < 1 || n > MAX);
	for(int i = 0; i < n; i++) a[i] = (-10 + rand() % 21);
}

int main(){
	int a[MAX];
	int n;
	GenerateArray(a,n);
}