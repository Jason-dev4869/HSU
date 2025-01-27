#include <iostream>
using namespace std;

/*Cong thuc Tam giac Pascal: 
a[i][0] = a[i][i] =1
a[i][k] = a[i-1][k-1] + a[i-1][k]*/

//Recursion Method n^2*2^N 
int calculatePascalValue(int n, int k){
	if(k==0||k==n) return 1;
	else return calculatePascalValue(n-1, k-1) + calculatePascalValue(n-1, k);
}
void displayPascalTriangle(int n){
	for (int i = 0; i < n; i++)
    {
        for (int j = 0; j <= i; j++)
            cout << calculatePascalValue(i, j) << "\t";
        cout << endl;
    }
}

//Matrix Method time = O(N^2) + space O(NxN)
void MatixPascalTriangle(int n){
	int pascal[n][n];
	//Tao tam giac Pascal
	for(int i = 0; i < n; i++)
		for(int j = 0; j <= i; j++)
			if(j == 0 || j == i) pascal[i][j] = 1;
			else pascal[i][j] = pascal[i-1][j-1] + pascal[i-1][j];
	//In tam giac Pascal
	for(int i = 0; i < n; i++){
		for(int j = 0; j <= i; j++) 
			cout << pascal[i][j] << "\t";
		cout << endl;
	}
}

//Loop Method time O(N^2)
void LoopPascalTriangle(int n){
	for(int i = 0; i < n; i++){
		int num = 1;
		for(int k = 0; k <= i; k++){
			cout << num << "\t";
			num = num * (i - k) / (k + 1);
		}
		cout <<endl;
	}
}

int main(){
	int n;
	cout << "Nhap so dong cua tam giac Pascal: ";
	cin >> n;
	cout << "De quy: " << "\n";
	displayPascalTriangle(n);
	cout << "\n" << "Ma tran: " << "\n";
	MatixPascalTriangle(n);
	cout << "\n" << "Vong lap: " << "\n";
	LoopPascalTriangle(n);
	return 0;
}