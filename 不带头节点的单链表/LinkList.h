#pragma once

#include <stdbool.h>
#include <stdio.h>

typedef struct LNode {
	void* data;
	struct LNode* next;
}LNode, * LinkList;

LinkList InitList(LinkList L);
bool Empty(LinkList L);
LNode* GetElem(LinkList L, int i);
int LinkListLen(LinkList L);
LinkList TailInsert(LinkList L, void* Ldata);
LinkList HeadInsert(LinkList L, void* Ldata);
LinkList IndexInsert(LinkList L, int i, void* Ldata);
LinkList TailDelete(LinkList L);
LinkList IndexDelete(LinkList L, int i);
LinkList DeleteNode(LinkList L, LNode* p);
LNode* LocateELem(LinkList L, void* Ldata);
LinkList HeadDelete(LinkList L);
LinkList DeleteLinkList(LinkList L);