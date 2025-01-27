/* Ly thuyet
Binary Search se di tim gtri x o phan tu o giua danh sach
DK: Danh sach phai co thu tu Vd: 1,3,5,6,8,10,12
Khi thuc hien tim gia tri X:
- Neu X > ptu o giua thi tiep tuc tim kiem o phan nam ben phai ptu trong danh sach
VD: X = 21; A = [2|5|8|10|12|13|15|18|21|24];
Co ptu giu danh sach la 12 vi X > 12 nen se tim cac gia tri sau 12 ([13|15|18|21|24])

- Neu X < ptu o giua thi tiep tuc tim kiem o phan nam ben trai ptu trong danh sach
VD: X = 10; A = [2|5|8|10|12|13|15|18|21|24];
Co ptu giu danh sach la 12, vi X < 12  nen se tim cac gia tri truoc 12 ([2|5|8|10])

- Neu X = ptu, tim kiem se dung lai
VD: X = 10; A = [2|5|8|10|12|13|15|18|21|24];
Co ptu giu danh sach la 12, vi X < 12 nen se tim cac gia tri truoc 12 ([2|5|8|10])
	+ X se tiep tuc so sanh voi ptu giua danh sach la 5, 
		vi X > 5 nen se tim cac gia tri sau 5 ([8|10])
	+ X se tiep tuc so sanh voi ptu giua danh sach la 8, 
		vi X > 8 nen se tim cac gia tri sau 8 ([10])
	+ Khi nay X = 10 => Chuong trinh se dung lai (Success);
	+ G/su gtri tim X = 11, khi con 1 ptu duy nhat la [10] 
		=> Chuong trinh se dung lai (Failed)
*/

#include <iostream>
using namespace std;

int BinarySearchLoop(int a[], int n, int x){
	int left = 0, right = n-1;
	while (left <= right){
		int mid = (left + right) / 2;
		if(x == a[mid]) return mid;
		else if(x < a[mid]) right = mid - 1;
		else if(x > a[mid]) left = mid + 1;
	}
	return -1;
}

int BinarySearchRecursive(int a[], int left, int right, int x){
	if(left > right) return -1;
	int mid = (left + right) / 2;
	if(x == a[mid]) return mid;
	else if(x < a[mid]) return BinarySearchRecursive(a, left, mid-1, x);
	else if(x > a[mid]) return BinarySearchRecursive(a, mid+1, right, x);
}

int main(){
	int a[] = {2,5,8,10,12,13,15,18,21,24};
	int n = sizeof(a)/sizeof(a[0]);
	int x, left = 0, right = n-1;
	cout << "Nhap so can tim tong mang: ";
	cin >> x;
	
	cout <<"\n" << "Loop: " <<"\n";
	cout << BinarySearchLoop(a,n,x);
	cout <<"\n" << "Recursive: " <<"\n";
	cout << BinarySearchRecursive(a,left,right,x);
}

/* Phan tich Giai thuat
Best case: Ptu mid = X; so lan so sanh = 1;
Worse case: khong co ptu = X; So lan so sanh: log(n);
Average case: G/su xac suat cac ptu = x nhu nhau: So lan so sanh: log(n/2;
Do phuc tap: T(n) = O(log(n));
*/