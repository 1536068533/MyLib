/*����ͷ�ڵ�ĵ�����
ֻ���ڴ����ʧ��ʱ���᷵��NULL��ɾ���ڵ�ʧ�ܲ��᷵��NULL
LNode*�ȼ�LinkList����LNode*������ʾ����ڵ�ָ�룬LinkList������ʾ��������*/

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct LNode {
	void* data;
	struct LNode* next;
}LNode, * LinkList;

LinkList InitList(LinkList L) {
	/*��ʼ��һ���յĵ���������true*/
	L = NULL;
	return L;
}

bool Empty(LinkList L) {
	/*�жϵ������Ƿ�Ϊ������*/
	return (L == NULL);
}

LNode* GetElem(LinkList L, int i) {
	/*��������ͷ��ַ������������������ض�Ӧ����ڵ��ַ*/
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
	/*��ȡ������*/
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
	/*β�巨��������β����������
	��Ͼ�̬����ָ��r��һֱָ����������һ���ڵ㣬������ܽ�ʡ��Դ
	��ӽڵ�ʧ���򷵻�NULL*/
	if (Empty(L)) {
		L = (LinkList)malloc(sizeof(LNode));
		if (L == NULL)  //�����ڴ���ܻ����ʧ�ܵ���������ڴ�������������false
			return NULL;
		L->data = Ldata;
		L->next = NULL;
		return L;
	}
	else {
		LNode* s = (LinkList)malloc(sizeof(LNode));
		if (s == NULL)  //�����ڴ���ܻ����ʧ�ܵ���������ڴ�������������false
			return NULL;
		GetElem(L, LinkListLen(L))->next = s;
		s->data = Ldata;
		s->next = NULL;
		return L;
	}
}

LinkList HeadInsert(LinkList L, void* Ldata) {
	/*ͷ�巨��������ͷ����������*/
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //�ڴ����ʧ��
		return NULL;
	s->data = Ldata;
	s->next = L;
	return s;
}

LinkList IndexInsert(LinkList L, int i, void* Ldata) {
	/*��λ����ڵ㣬���������±����ڵ�*/
	if (i<1 || i>LinkListLen(L) + 1)
		return L;
	if (Empty(L) || i == 1)
		return HeadInsert(L, Ldata);
	LinkList p = L;
	while (i > 2) {  //����ѭ���ҵ�Ҫ���������ڵ��±��ǰһ������ڵ�
		p = p->next;
		i--;
	}
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //�ڴ����ʧ��
		return NULL;
	s->data = Ldata;
	s->next = p->next;
	p->next = s;
	return L;
}

LinkList TailDelete(LinkList L) {
	/*ɾ������ĩβ�ڵ�*/
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
	/*���������±�ɾ���ڵ�*/
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
	/*���ݴ��������ڵ��ַɾ������ڵ�*/
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
	/*��ֵ����*/
	if (L == NULL)
		return NULL;
	LNode* p = L->next;
	while (p != NULL && p->data != Ldata)
		p = p->next;
	return p;
}

LinkList HeadDelete(LinkList L) {
	/*ɾ��ͷ�ڵ�*/
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
	/*ɾ�����������ͷſռ�*/
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