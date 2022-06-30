#include "LinkList.h"

int main() {
	LinkList L = NULL;
	if (InitList(&L))
		printf("初始化链表成功！\n");
	else
		printf("初始化链表失败！\n");
	printf("初始化后的链表地址：%p\n", L);
	printf("初始化后的链表的长度：%d\n", LinkListLen(L));
	if (Empty(L))
		printf("判断链表是否为空：这是空链表！\n");
	else
		printf("判断链表是否为空：这不是空链表！\n");
	int get_elem = 1;
	printf("空链表第%d个元素的指针地址：%p\n", get_elem, GetElem(L, get_elem));
	printf("链表大小：%zd\n", sizeof(LNode));
	TailInsert(L, "一");
	TailInsert(L, "二");
	TailInsert(L, "三");
	TailInsert(L, "四");
	TailInsert(L, "五");
	printf("当前链表长度：%d\n", LinkListLen(L));
	HeadInsert(L, "负一");
	HeadInsert(L, "负二");
	IndexInsert(L, 1, "这是按位序插入的一");
	IndexInsert(L, 5, "这是按位序插入的，插入在第五节点的位置");
	IndexDelete(L, 7);

	int i = 1;
	LinkList prt = L;
	while (prt != NULL) {
		printf("链表的第%d个元素为：%s\n", i, (char*)GetElem(L, i)->data);
		prt = prt->next;
		i++;
	}

	DeleteLinkList(&L);
	printf("删除链表后的链表地址：%p", L);
	return 0;
}