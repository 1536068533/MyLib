#include "LinkList.h"

bool InitList(LinkList* pL) {
	/*��ʼ��һ���յĵ���������true*/
	*pL = (LinkList)malloc(sizeof(LNode));
	if (*pL == NULL)
		return false;
	(** pL).data = NULL;
	(** pL).next = NULL;
	return true;
}

bool Empty(LinkList L) {
	/*�жϵ������Ƿ�Ϊ������
	�Ƿ��Ѿ���ʼ���������ڴ�ռ�*/
	return (L == NULL);
}

LNode* GetElem(LinkList L, int i) {
	/*��������ͷ��ַ������������������ض�Ӧ����ڵ��ַ��û�иýڵ��򷵻�NULL*/
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

bool TailInsert(LinkList L, void* Ldata) {
	/*β�巨��������β����������
	��ӽڵ�ʧ���򷵻�false*/
	if (Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL) {
		L->data = Ldata;
		return true;
	}
	else {
		LNode* s = (LinkList)malloc(sizeof(LNode));
		if (s == NULL)  //�����ڴ���ܻ����ʧ�ܵ���������ڴ�������������false
			return false;
		GetElem(L, LinkListLen(L))->next = s;
		s->data = Ldata;
		s->next = NULL;
		return true;
	}
}

bool HeadInsert(LinkList L, void* Ldata) {
	/*ͷ�巨��������ͷ����������*/
	if (Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL) {
		L->data = Ldata;
		return true;
	}
	else {
		LNode* s = (LNode*)malloc(sizeof(LNode));
		if (s == NULL)  //�ڴ����ʧ��
			return false;
		s->data = L->data;
		s->next = L->next;
		L->data = Ldata;
		L->next = s;
		return true;
	}
}

bool IndexInsert(LinkList L, int i, void* Ldata) {
	/*��λ����ڵ㣬���������±����ڵ�*/
	if (i<1 || i>LinkListLen(L) + 1 || Empty(L))
		return false;
	else if (L->data == NULL && L->next == NULL && i == 2) {
		return false;
	}
	if (i == 1)
		return HeadInsert(L, Ldata);
	while (i > 2) {  //����ѭ���ҵ�Ҫ���������ڵ��±��ǰһ������ڵ�
		L = L->next;
		i--;
	}
	LNode* s = (LNode*)malloc(sizeof(LNode));
	if (s == NULL)  //�ڴ����ʧ��
		return false;
	s->data = Ldata;
	s->next = L->next;
	L->next = s;
	return true;
}

bool TailDelete(LinkList L) {
	/*ɾ������ĩβ�ڵ�
	���������������Ǹ���������ʱû��ɾ���κνڵ㣩�򷵻�false
	�������ֻ��һ���ڵ㣬��ɾ���ýڵ�����ݣ��������ͷ��ڴ棬��󷵻�true
	������������������ڵ㣬���ͷ�ĩβ�ڵ��ڴ沢����true*/
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
	/*���������±�ɾ���ڵ�
	���������������Ǹ���������ʱû��ɾ���κνڵ㣩����������±겻�ڷ�Χ���򷵻�false
	���ָ��ɾ������Ψһ�Ľڵ㣬��ɾ���ýڵ����ݣ��������ͷ��ڴ棬��󷵻�true
	������������������ڵ㣬���ͷ�ָ���ڵ��ڴ沢����true*/
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
	/*���ݴ��������ڵ��ַɾ������ڵ�
	���������������Ǹ���������ʱû��ɾ���κνڵ㣩�򷵻�false
	������������������ڵ㣬���ͷ�ָ���ڵ��ڴ沢����true*/
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
	/*��ֵ����*/
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
	/*ɾ��ͷ�ڵ�
	���������������Ǹ���������ʱû��ɾ���κνڵ㣩�򷵻�false
	�������ֻ��һ���ڵ���ɾ���ýڵ�����ݣ��������ͷ��ڴ棬��󷵻�true
	������������������ڵ㣬���ͷŵ�һ���ڵ��ڴ沢����true*/
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
	/*ɾ���������нڵ㲢�ͷſռ䣬������ص���ʼ��֮ǰ��״̬
	���������������Ǹ���������ʱû��ɾ���κνڵ㣩�򷵻�false
	�����ɾ���ڵ�����򷵻�true*/
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