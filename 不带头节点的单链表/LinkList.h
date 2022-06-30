/*����ͷ�ڵ�ĵ�����
�ڴ����ʧ��ʱ���᷵��false
LNode*�ȼ�LinkList����LNode*������ʾ����ڵ�ָ�룬LinkList������ʾ��������*/

#pragma once

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct LNode {
	void* data;
	struct LNode* next;
}LNode, * LinkList;

bool InitList(LinkList* pL);
bool Empty(LinkList L);
LNode* GetElem(LinkList L, int i);
int LinkListLen(LinkList L);
bool TailInsert(LinkList L, void* Ldata);
bool HeadInsert(LinkList L, void* Ldata);
bool IndexInsert(LinkList L, int i, void* Ldata);
bool TailDelete(LinkList L);
bool IndexDelete(LinkList L, int i);
bool DeleteNode(LinkList L, LNode* p);
LNode* LocateELem(LinkList L, void* Ldata);
bool HeadDelete(LinkList L);
bool DeleteLinkList(LinkList* pL);