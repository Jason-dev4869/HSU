#import <iostream>
using namespace std;

struct NODE{
	int info;
	NODE* pNext;
};
struct LIST{
	NODE* pHead;
	NODE* pTail;
};

void Initialize(LIST &l){
	l.pHead = NULL;
	l.pTail = NULL;
}

bool IsEmpty(LIST l){
	return l.pHead == NULL;
}

NODE* CreateNode(int x){
	NODE* p = new NODE;
	if(p == NULL){
		cout << "Cannot Initialize" <<endl;
		return NULL;
	}
	p->info = x;
	p->pNext = NULL;
	return p;
}

NODE* InsertHead(LIST &l, int x){
	NODE* p = CreateNode(x);
	if(p!=NULL){
		if(IsEmpty(l)) l.pHead = l.pTail = p;
		else{
			p->pNext = l.pHead;
			l.pHead = p;
		}
	}
	return p;
}

NODE* InsertTail(LIST &l, int x){
	NODE* p = CreateNode(x);
	if(p!=NULL){
		if(IsEmpty(l)) l.pHead = l.pTail = p;
		else{
			l.pTail->pNext = p;
			l.pTail = p;
		}
	}
	return p;
}

void CreateList(LIST &l){
	int x;
	do{
		cin >> x;
		if(x==0) break;
		InsertTail(l,x);
	}while(1);
}

void OutputList(LIST l){
	for(NODE* p=l.pHead; p!=NULL; p=p->pNext) cout << p->info << "\t";
	cout << endl;
}

int main(){
	LIST l;
	Initialize(l);
	CreateList(l);
	OutputList(l);
}