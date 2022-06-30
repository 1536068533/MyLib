/*不带头节点的单链表
内存分配失败时，会返回false
LNode*等价LinkList，但LNode*用来表示链表节点指针，LinkList用来表示整个链表*/

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