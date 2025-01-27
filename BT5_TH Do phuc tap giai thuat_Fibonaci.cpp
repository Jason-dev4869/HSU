#include <iostream>
using namespace std;
#define n 100

//O(2^n)
int fb1(int n){
	if(n<=1) return n;
	if(n>=2) return fb1(n-1) + fb1(n-2);
}

//O(n) f[n+1];
long long fb2(int n){
	long long f[n+1];
	if(n<=1) return 1;
	f[0] = 1;
	f[1] = 1;
	for(int i = 2; i<=n; i++) f[i] = f[i-1] + f[i-2];
	return f[n];
}
//O(n) tmp;
long long fb3(int n){
	if(n==0 || n==1) return 1;
	long long b = 1, a = 0, c;
	for(int i = 2; i<=n; i++){
		c = b;
		b = a+b;
		a = c;
	}
	return b;
}

int main(){
	cout << fb1(n);
	cout << fb2(n);
	cout << fb3(n);
}