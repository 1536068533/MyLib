#include "LinkList.h"

int main() {
	LinkList L = NULL;
	if (InitList(&L))
		printf("��ʼ������ɹ���\n");
	else
		printf("��ʼ������ʧ�ܣ�\n");
	printf("��ʼ����������ַ��%p\n", L);
	printf("��ʼ���������ĳ��ȣ�%d\n", LinkListLen(L));
	if (Empty(L))
		printf("�ж������Ƿ�Ϊ�գ����ǿ�����\n");
	else
		printf("�ж������Ƿ�Ϊ�գ��ⲻ�ǿ�����\n");
	int get_elem = 1;
	printf("�������%d��Ԫ�ص�ָ���ַ��%p\n", get_elem, GetElem(L, get_elem));
	printf("�����С��%zd\n", sizeof(LNode));
	TailInsert(L, "һ");
	TailInsert(L, "��");
	TailInsert(L, "��");
	TailInsert(L, "��");
	TailInsert(L, "��");
	printf("��ǰ�����ȣ�%d\n", LinkListLen(L));
	HeadInsert(L, "��һ");
	HeadInsert(L, "����");
	IndexInsert(L, 1, "���ǰ�λ������һ");
	IndexInsert(L, 5, "���ǰ�λ�����ģ������ڵ���ڵ��λ��");
	IndexDelete(L, 7);

	int i = 1;
	LinkList prt = L;
	while (prt != NULL) {
		printf("����ĵ�%d��Ԫ��Ϊ��%s\n", i, (char*)GetElem(L, i)->data);
		prt = prt->next;
		i++;
	}

	DeleteLinkList(&L);
	printf("ɾ�������������ַ��%p", L);
	return 0;
}