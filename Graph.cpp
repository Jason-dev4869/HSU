#include <fstream>
#include <iostream>
using namespace std;
#define MAX 100
struct CANH
{
	int bd;//Dinh bat dau
	int kt;//Dinh ket thuc
	int ts;//Trong so
};
void docfile(int a[][MAX], int &N)
{
	ifstream f("a.txt");
	f>>N;
	for(int i=0; i<N; i++)
		for(int j=0; j<N; j++)
			f>>a[i][j];
}
void xuatMaTran(int a[][MAX], int N)
{
	for(int i=0; i<N; i++)
	{
		for(int j=0; j<N; j++)
			cout<<a[i][j]<<"\t";
		cout<<endl;
	}
}

void LietKeCanh(int a[][MAX], int N, CANH mangCanh[], int &m)
{
	for(int i=0; i<N; i++)
		for(int j=i+1; j<N; j++)
		{
			if(a[i][j]>0) //co canh noi
			{
				mangCanh[m].bd = i;
				mangCanh[m].kt = j;
				mangCanh[m].ts = a[i][j];
				m++;
			}
		}
}

void xuatCanh(CANH a[], int m)
{
	for(int i=0; i<m; i++)
		cout<<a[i].bd<<a[i].kt<<":\t"<<a[i].ts<<endl;
}

void SelectionSortsCanh(CANH a[], int m){
	for(int i = 0; i < m; i++){
		int min = i;
		for(int j = i + 1; j < m; j ++){
			if(a[j].ts < a[min].ts)
				min = j;
		}
		swap(a[i], a[min]);
	}
}

int main()
{
	int a[MAX][MAX];
	int N;
	docfile(a, N);
	xuatMaTran(a, N);
	CANH mangCanh[MAX*MAX];
	int m=0; //so canh
	LietKeCanh(a, N, mangCanh, m);
	xuatCanh(mangCanh, m);
	cout<<"\n--- Sort Canh tang dan theo trong so ---\n";
	SelectionSortsCanh(mangCanh, m);
	xuatCanh(mangCanh, m);
}