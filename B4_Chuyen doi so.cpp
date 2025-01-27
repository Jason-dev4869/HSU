#include<iostream>
using namespace std;

void binaryConvert(int n){
	if(n==0) return;
	binaryConvert(n/2);
	cout << n % 2;
}

void BinArray(int N){
	int a[100], n = 0;
	while(N!=0){
		a[n++] = N % 2;
		N/=2;
	}
	for(int i=n-1; i>=0 ; i--) 
		cout << a[i];
}

int Sum(int n){
	if(n==1) return 1;
	return Sum(n-1) + n;
}

int GiaiThua(int n){
	if(n==0) return 1;
	return GiaiThua(n-1) * n;
}

int Fibonacci(int n){
	if(n==0) return 0;
	if(n==1) return 1;
	if(n>=2) return Fibonacci(n-1) + Fibonacci(n-2);
}

int main(){
	int n;
	cout<<"Nhap vao n so nguyen duong:";
	cin >> n;
	binaryConvert(n);
	cout << endl;
	BinArray(n);
	cout << "\n" << Sum(n);
	cout << "\n" << GiaiThua(n);
	cout << "\n" << Fibonacci(n);
}