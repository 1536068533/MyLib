#include "LinkList.h"

bool InitList(LinkList* pL) {
	/*初始化一个空的单链表，返回true*/
	*pL = (LinkList)malloc(sizeof(LNode));
	if (*pL == NULL)
		return false;
	(** pL).data = NULL;
	(** pL).next = NULL;
	return true;
}

bool Empty(LinkList L) {
	/*判断单链表是否为空链表
	是否已经初始化开辟了内存空间*/
	return (L == NULL);
}

LNode* GetElem(LinkList L, int i) {
	/*传入链表开头地址和链表坐标参数，返回对应链表节点地址，没有该节点则返回NULL*/
	if (i < 1 || i > LinkListLen(L) || Empty(L))
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

bool TailInsert(LinkList L, void* Ldata) {
	/*尾插法，从链表尾部插入数据
	添加节点失败则返回false*/
	if (Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL) {
		L->data = Ldata;
		return true;
	}
	else {
		LNode* s = (LinkList)malloc(sizeof(LNode));
		if (s == NULL)  //分配内存可能会出现失败的情况（如内存已满），返回false
			return false;
		GetElem(L, LinkListLen(L))->next = s;
		s->data = Ldata;
		s->next = NULL;
		return true;
	}
}

bool HeadInsert(LinkList L, void* Ldata) {
	/*头插法，从链表头部插入数据*/
	if (Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL) {
		L->data = Ldata;
		return true;
	}
	else {
		LNode* s = (LNode*)malloc(sizeof(LNode));
		if (s == NULL)  //内存分配失败
			return false;
		s->data = L->data;
		s->next = L->next;
		L->data = Ldata;
		L->next = s;
		return true;
	}
}

bool IndexInsert(LinkList L, int i, void* Ldata) {
	/*按位插入节点，即按链表下标插入节点*/
	if (i<1 || i>LinkListLen(L) + 1 || Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL && i == 2) {
		return false;
	}
	if (i == 1)
		return HeadInsert(L, Ldata);
	while (i > 2) {  //利用循环找到要插入的链表节点下标的前一个链表节点
		L = L->next;
		i--;
	}
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //内存分配失败
		return false;
	s->data = Ldata;
	s->next = L->next;
	L->next = s;
	return true;
}

bool TailDelete(LinkList L) {
	/*删除链表末尾节点
	如果传入的链表本身是个空链表（此时没有删除任何节点）则返回false
	如果链表只有一个节点，则删除该节点的数据，但不会释放内存，最后返回true
	如果链表有至少两个节点，则释放末尾节点内存并返回true*/
	if (L == NULL)
		return false;
	else if (L->next == NULL) {
		L->data = NULL;
		return true;
	}
	LNode* p = GetElem(L, LinkListLen(L) - 1);
	free(p->next);
	p->next = NULL;
	return true;
}

bool IndexDelete(LinkList L, int i) {
	/*根据链表下标删除节点
	如果传入的链表本身是个空链表（此时没有删除任何节点）或传入的链表下标不在范围内则返回false
	如果指定删除链表唯一的节点，则删除该节点数据，但不会释放内存，最后返回true
	如果链表有至少两个节点，则释放指定节点内存并返回true*/
	int len = LinkListLen(L);
	if (i<=0 || i > len)
		return false;
	else if (i == 1) {
		return HeadDelete(L);
	}
	else if (i == len)
		return TailDelete(L);
	LNode* pLast = GetElem(L, i - 1);
	LNode* pNext = pLast->next->next;
	free(pLast->next);
	pLast->next = pNext;
	return true;
}

bool DeleteNode(LinkList L, LNode* p) {
	/*根据传入的链表节点地址删除链表节点
	如果传入的链表本身是个空链表（此时没有删除任何节点）则返回false
	如果链表有至少两个节点，则释放指定节点内存并返回true*/
	if (p == NULL)
		return false;
	else if (p->next == NULL)
		return TailDelete(L);
	else if (p->next->next == NULL) {
		p->data = p->next->data;
		free(p->next);
		p->next = NULL;
		return true;
	}
	else {
		LNode* q = p->next;
		p->data = q->data;
		p->next = q->next;
		free(q);
		return true;
	}
}

LNode* LocateELem(LinkList L, void* Ldata) {
	/*按值查找*/
	if (L == NULL)
		return NULL;
	else if (L->data == Ldata)
		return L;
	else {
		LNode* p = L->next;
		while (p != NULL && p->data != Ldata)
			p = p->next;
		return p;
	}
}

bool HeadDelete(LinkList L) {
	/*删除头节点
	如果传入的链表本身是个空链表（此时没有删除任何节点）则返回false
	如果链表只有一个节点则删除该节点的数据，但不会释放内存，最后返回true
	如果链表有至少两个节点，则释放第一个节点内存并返回true*/
	if (L == NULL)
		return false;
	else if (L->next == NULL) {
		L->data = NULL;
		return true;
	}
	else {
		L->data = L->next->data;
		LNode* p = L->next;
		L->next = L->next->next;
		free(p);
		return true;
	}
}

bool DeleteLinkList(LinkList* pL) {
	/*删除链表所有节点并释放空间，让链表回到初始化之前的状态
	如果传入的链表本身是个空链表（此时没有删除任何节点）则返回false
	如果有删除节点操作则返回true*/
	if (*pL == NULL)
		return false;
	else {
		int len = LinkListLen(*pL);
		while (len > 1) {
			HeadDelete(*pL);
			len--;
		}
		free(*pL);
		*pL = NULL;
		return true;
	}
}