#import <fstream>
#import <iostream>
using namespace std;

struct Room{
	int District;
	float Area;
	float Price;
	int Bedroom;
	int NumWC;
	int NumAC;
	float Deposite;
};

void ReadFile(Room* &r, int &n){
	FILE *f = fopen("PhongTro.txt", "r");
	if(f==NULL){
		cout << "Cannot open file" <<endl; n = 0;
		return;
	}
	fscanf(f, "%d", &n);
	r = new Room[n];
	for(int i = 0; i<n; i++){
		fscanf(f, "%d", &r[i].District);
		fscanf(f, "%f", &r[i].Area);
		fscanf(f, "%f", &r[i].Price);
		fscanf(f, "%d", &r[i].Bedroom);
		fscanf(f, "%d", &r[i].NumWC);
		fscanf(f, "%d", &r[i].NumAC);
		fscanf(f, "%f", &r[i].Deposite);
	}
}

void Output(Room r){
	cout<<" - District: "<<r.District<<"\t";
	cout<<" - Area: "<<r.Area<<"m2\t";
	cout<<" - Price: "<<r.Price<<"tr\t";
	cout<<" - Number of Bedroom: "<<r.Bedroom<<"\t";
	cout<<" - Number of WC: "<<r.NumWC<<"\t";
	cout<<" - Number of AC: "<<r.NumAC<<"\t";
	cout<<" - Deposite: "<<r.Deposite<<"tr\n";
}

void PrintArr(Room r[], int n){
	for(int i=0; i<n; i++) Output(r[i]);
}

void ListByNumWC(Room r[], int n){
	int num;
	cout << "Enter number of WC want to find:";
	cin >> num;
	for(int i = 0; i<n; i++){
		if(r[i].NumWC == num) Output(r[i]);
	}
}

void CountByBedRoom(Room r[], int n){
	int num, count;
	cout << "Enter number of Bedroom want to find";
	cin >> num;
	for(int i = 0; i<n; i++){
		if(r[i].Bedroom == num) count++;
	}
	cout << "There is/are " <<count<< " room have " << num << " bedroom" <<endl;
}

void FindMinByDeposite(Room r[], int n){
	Room min = r[0];
	for(int i = 0; i<n; i++){
		if(r[i].Deposite < min.Deposite){
			min = r[i];
			Output(min);
		}
	}
	Output(min);
}

void FindMaxByAC(Room r[], int n){
	Room max = r[0];
	for(int i = 0; i<n; i++){
		if(r[i].NumAC > max.NumAC){
			max = r[i];
			Output(max);
		} 
	}
}

int main(){
	Room *r; int n;
	ReadFile(r, n);
	PrintArr(r, n);
	cout << "\n";
	ListByNumWC(r,n);
	cout << "\n";
	CountByBedRoom(r,n);
	cout << "\n";
	FindMinByDeposite(r,n);
	cout << "\n";
	FindMaxByAC(r,n);
}