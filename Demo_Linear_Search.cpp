/* Ly Thuyet
Linear Search se so sanh danh sach tu ptu dau tien lan luot toi cuoi
voi gia tri x can tim se cho ra 2 ket qua:
- Neu co ptu = x, thuat toan lap tuc dung lai (Success)
- Neu deu cuoi danh sach khong co ptu = x, thuat toan se dung lai(Failed)

VD: 
* cho x = 5; A = [7|13|5|21|6|2|8|15];
So sanh tung gia tri cho toi khi tim ra x nam o a[2]

* cho x = 9; A = [7|13|5|21|6|2|8|15] X;
So sanh tung gtri, khong tim thay x, xuat kq khong tim thay
*/

#include <iostream>
using namespace std;

int LinearSearch(int a[], int n, int x){
	//Lap for cho i = 0 (Bat dau phan tu dau tien chay cho toi cuoi mang)
	for(int i = 0; i < n; i++)
		//So sanh a[i] voi gtri x can tim
		if(x == a[i])
			return i; //tim thay
	return -1;	//khong tim thay
}

int main(){
	int x;
	int a[] = {1, 4, -9, 8, 66, 73, 100};
	int  n = sizeof(a)/sizeof(a[0]);
	cout << "Nhap so can tim tong mang: ";
	cin >> x;
	
	cout<< LinearSearch(a,n,x);
}

/* Phan tich Giai thuat
Best case: Phan tu dau tien = X; so lan so sanh = 1;
Worse case: Phan tu cuoi = X hoac khong co ptu = X; So lan so sanh: n;
Average case: G/su xac suat cac ptu = x nhu nhau: So lan so sanh: (n+1)/2;
Do phuc tap: T(n) = O(n);
*/