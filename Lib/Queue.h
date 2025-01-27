#include <iostream>
using namespace std;
#define N 100
typedef int DATA;

typedef struct NODE {
    DATA info;
    NODE* pNext;
} NODE;

typedef struct {
    NODE* pHead;
    NODE* pTail;
} LQUEUE;

void Initialize(LQUEUE &q) {
    q.pHead = NULL;
    q.pTail = NULL;
}

bool isEmpty(LQUEUE q) {
    return (q.pHead == NULL);
}

NODE* CreateNode(int x) {
    NODE* p = new NODE;
    if (p == NULL) {
        cout << "Khong cap phat duoc vung nho!!!";
        return NULL;
    }
    p->info = x;
    p->pNext = NULL;
    return p;
}

NODE* InsertTail(LQUEUE &q, int x) {
    NODE* p = CreateNode(x);
    if (p != NULL) {
        if (isEmpty(q)) {
            q.pHead = q.pTail = p;
        } else {
            q.pTail->pNext = p;
            q.pTail = p;
        }
    }
    return p;
}

bool deleteHead(LQUEUE &q) {
    if (!isEmpty(q)) {
        NODE* p = q.pHead;
        q.pHead = q.pHead->pNext;
        if (q.pHead == NULL) {
            q.pTail = NULL;
        }
        delete p;
        return true;
    }
    return false;
}

bool Enqueue(LQUEUE &q, DATA x) {
    NODE* p = InsertTail(q, x);
    return (p != NULL);
}

DATA Dequeue(LQUEUE &q) {
    if (!isEmpty(q)) {
        DATA x = q.pHead->info;
        deleteHead(q);
        return x;
    }
    return -1;
}

DATA getFront(LQUEUE q) {
    if (!isEmpty(q))
        return q.pHead->info;
    return -1;
}

DATA getRear(LQUEUE q) {
    if (!isEmpty(q))
        return q.pTail->info;
    return -1;
}