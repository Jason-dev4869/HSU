#include <iostream>
using namespace std;
typedef int DATA;

typedef struct NODE {
	DATA info;
	NODE* pNext;
} NODE;

typedef struct {
	NODE* pHead;
} STACK;

void Initialize(STACK &s) {
	s.pHead = NULL;
}
bool IsEmpty(STACK s) {
	if (s.pHead == NULL)
		return true;
	return false;
}

NODE* CreateNode(DATA x) {
	NODE* p = new NODE;
	if (p != NULL) {
		p->info = x; // g?n th?ng tin cho ph?n t? p
		p->pNext = NULL;
	}
	return p;
}


NODE* InsertHead(STACK &list, DATA x) {
	NODE* p = CreateNode(x);
	if (p != NULL) {
		p->pNext = list.pHead;
		list.pHead = p;
	}
	return p;
}
bool DeleteHead(STACK &list) {
	if ( !IsEmpty(list) ) {
		NODE* p = list.pHead;
		list.pHead = list.pHead->pNext;
		delete p; return true;
	}
	return false;
}
bool Push(STACK &s, DATA x) {
	NODE* p = InsertHead(s,x);
	if (p != NULL)
		return true;
	return false;
}
DATA Pop(STACK &s) {
    if ( !IsEmpty(s) ) {
	DATA x = s.pHead->info;
	DeleteHead(s);
	return x;
    }
    return NULL;
}
DATA GetTop(STACK s) {
    if ( !IsEmpty(s) ) {
	DATA x = s.pHead->info;
	return x;
    }
    return NULL;
}

void Output(STACK list) {
	NODE* p = list.pHead;
	while (p != NULL) {
		cout<<p->info<<"\t";
		p = p->pNext;
	}
}


int main()
{
	STACK s;
	Initialize(s);
	Push(s, 10);
	Push(s, 9);
	Push(s, 8);
	Push(s, 7);
	cout<<Pop(s)<<endl; //7 *** 10 9 8 5 6
	Push(s, 5); 
	Push(s, 6);
	cout<<Pop(s)<<endl;  //6
	cout<<Pop(s)<<endl;  //5
	cout<<Pop(s)<<endl;  //8
	Push(s, 7); //10 9 7 8 9
	Push(s, 8);
	Push(s, 9);
	cout<<Pop(s)<<endl; //9
	cout<<Pop(s)<<endl; //8
	Push(s, 10); //10 9 7 10
	Output(s);
}