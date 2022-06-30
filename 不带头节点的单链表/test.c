#include "LinkList.h"

int main() {
	LinkList L = NULL;
	if ((L = InitList(L)) == NULL)
		printf("初始化链表成功！\n");
	else
		printf("初始化链表失败！\n");
	printf("初始化后的链表地址：%p\n", L);
	if (Empty(L))
		printf("判断链表是否为空：这是空链表！\n");
	else
		printf("判断链表是否为空：这不是空链表！\n");
	int get_elem = 2;
	printf("空链表第%d个元素的指针地址：%p\n", get_elem, GetElem(L, get_elem));
	printf("空链表的长度：%d\n", LinkListLen(L));
	printf("链表大小：%zd\n", sizeof(LNode));
	L = TailInsert(L, "一");
	L = TailInsert(L, "二");
	L = TailInsert(L, "三");
	L = TailInsert(L, "四");
	L = TailInsert(L, "五");
	printf("当前链表长度：%d\n", LinkListLen(L));
	L = HeadInsert(L, "负一");
	L = HeadInsert(L, "负二");
	L = IndexInsert(L,1,"这是按位序插入的一");
	L = IndexInsert(L, 5, "这是按位序插入的，插入在第五节点的位置");
	L = IndexDelete(L, 7);

	int i = 1;
	LinkList prt = L;
	while (prt != NULL) {
		printf("链表的第%d个元素为：%s\n", i, (char*)GetElem(L, i)->data);
		prt = prt->next;
		i++;
	}
	return 0;
}