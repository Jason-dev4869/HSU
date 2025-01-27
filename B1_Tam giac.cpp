#include <iostream>
using namespace std;

int main(){
	int a, b, c;
	cout << "Vui long nhap 3 canh cua tam giac: ";
	cin>>a>>b>>c;
	
	if(a == b + c || b == c + a || c == b + a){
		cout << "Duong thang (Khong phai la tam giac)";
		return 1;
	}
	bool check;
	if(a*a == b*b + c*c || b*b == c*c + a*a || c*c == b*b + a*a){
		cout<< "Tam giac vuong";
		check = true;
	}
	if(a == b && b == c)
		cout<< "Tam giac deu";
	else if(a == b || b == c || c == a)
		if(!check) cout << "Tam giac can";
		else cout << "can";
	else
		if(!check)cout << "Tam giac thuong";
}