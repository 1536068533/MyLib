/*不带头节点的单链表
只有内存分配失败时，会返回NULL，删除节点失败不会返回NULL
LNode*等价LinkList，但LNode*用来表示链表节点指针，LinkList用来表示整个链表*/

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct LNode {
	void* data;
	struct LNode* next;
}LNode, * LinkList;

LinkList InitList(LinkList L) {
	/*初始化一个空的单链表，返回true*/
	L = NULL;
	return L;
}

bool Empty(LinkList L) {
	/*判断单链表是否为空链表*/
	return (L == NULL);
}

LNode* GetElem(LinkList L, int i) {
	/*传入链表开头地址和链表坐标参数，返回对应链表节点地址*/
	if (i < 1 || Empty(L))
		return NULL;
	else if (i == 1)
		return L;
	else {
		LNode* p = L->next;
		for (int j = 2; j < i; j++) {
			p = p->next;
			if (p == NULL)
				return p;
		}
		return p;
	}
}

int LinkListLen(LinkList L) {
	/*获取链表长度*/
	if (Empty(L))
		return 0;
	else {
		int len = 1;
		LNode* p = L;
		while (p->next != NULL) {
			p = p->next;
			len++;
		}
		return len;
	}
}

LinkList TailInsert(LinkList L, void* Ldata) {
	/*尾插法，从链表尾部插入数据
	配合静态变量指针r，一直指向链表的最后一个节点，提高性能节省资源
	添加节点失败则返回NULL*/
	if (Empty(L)) {
		L = (LinkList)malloc(sizeof(LNode));
		if (L == NULL)  //分配内存可能会出现失败的情况（如内存已满），返回false
			return NULL;
		L->data = Ldata;
		L->next = NULL;
		return L;
	}
	else {
		LNode* s = (LinkList)malloc(sizeof(LNode));
		if (s == NULL)  //分配内存可能会出现失败的情况（如内存已满），返回false
			return NULL;
		GetElem(L, LinkListLen(L))->next = s;
		s->data = Ldata;
		s->next = NULL;
		return L;
	}
}

LinkList HeadInsert(LinkList L, void* Ldata) {
	/*头插法，从链表头部插入数据*/
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //内存分配失败
		return NULL;
	s->data = Ldata;
	s->next = L;
	return s;
}

LinkList IndexInsert(LinkList L, int i, void* Ldata) {
	/*按位插入节点，即按链表下标插入节点*/
	if (i<1 || i>LinkListLen(L) + 1)
		return L;
	if (Empty(L) || i == 1)
		return HeadInsert(L, Ldata);
	LinkList p = L;
	while (i > 2) {  //利用循环找到要插入的链表节点下标的前一个链表节点
		p = p->next;
		i--;
	}
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //内存分配失败
		return NULL;
	s->data = Ldata;
	s->next = p->next;
	p->next = s;
	return L;
}

LinkList TailDelete(LinkList L) {
	/*删除链表末尾节点*/
	if (L == NULL)
		return NULL;
	else if (L->next == NULL) {
		free(L);
		return NULL;
	}
	LNode* p = GetElem(L, LinkListLen(L) - 1);
	free(p->next);
	p->next = NULL;
	return L;
}

LinkList IndexDelete(LinkList L, int i) {
	/*根据链表下标删除节点*/
	int len = LinkListLen;
	if (i<0 || i > len)
		return L;
	else if (i == 1) {
		LNode* p = L->next;
		free(L);
		return p;
	}
	else if (i == len)
		return TailDelete(L);
	LNode* pLast = GetElem(L, i - 1);
	LNode* pNext = GetElem(L, i + 1);
	free(pLast->next);
	pLast->next = pNext;
	return L;
}

LinkList DeleteNode(LinkList L, LNode* p) {
	/*根据传入的链表节点地址删除链表节点*/
	if (p == NULL)
		return L;
	if (p->next == NULL)
		return TailDelete(L);
	if (p->next->next == NULL) {
		p->data = p->next->data;
		free(p->next);
		p->next = NULL;
		return L;
	}
	LNode* q = p->next;
	p->data = p->next->data;
	p->next = q->next;
	free(q);
	return L;
}

LNode* LocateELem(LinkList L, void* Ldata) {
	/*按值查找*/
	if (L == NULL)
		return NULL;
	LNode* p = L->next;
	while (p != NULL && p->data != Ldata)
		p = p->next;
	return p;
}

LinkList HeadDelete(LinkList L) {
	/*删除头节点*/
	if (L == NULL)
		return NULL;
	else if (L->next == NULL) {
		free(L);
		return NULL;
	}
	LNode* p = L;
	L = L->next;
	free(p);
	return L;
}

LinkList DeleteLinkList(LinkList L) {
	/*删除整个链表并释放空间*/
	if (L == NULL)
		return NULL;
	else if (L->next == NULL)
		return HeadDelete(L);
	LNode* p = L;
	int len = LinkListLen(L);
	while (len > 0) {
		L = HeadDelete(L);
		len--;
	}
	return L;
}