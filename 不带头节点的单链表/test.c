#include "LinkList.h"

int main() {
	LinkList L = NULL;
	if ((L = InitList(L)) == NULL)
		printf("��ʼ������ɹ���\n");
	else
		printf("��ʼ������ʧ�ܣ�\n");
	printf("��ʼ����������ַ��%p\n", L);
	if (Empty(L))
		printf("�ж������Ƿ�Ϊ�գ����ǿ�����\n");
	else
		printf("�ж������Ƿ�Ϊ�գ��ⲻ�ǿ�����\n");
	int get_elem = 2;
	printf("�������%d��Ԫ�ص�ָ���ַ��%p\n", get_elem, GetElem(L, get_elem));
	printf("������ĳ��ȣ�%d\n", LinkListLen(L));
	printf("�����С��%zd\n", sizeof(LNode));
	L = TailInsert(L, "һ");
	L = TailInsert(L, "��");
	L = TailInsert(L, "��");
	L = TailInsert(L, "��");
	L = TailInsert(L, "��");
	printf("��ǰ�����ȣ�%d\n", LinkListLen(L));
	L = HeadInsert(L, "��һ");
	L = HeadInsert(L, "����");
	L = IndexInsert(L,1,"���ǰ�λ������һ");
	L = IndexInsert(L, 5, "���ǰ�λ�����ģ������ڵ���ڵ��λ��");
	L = IndexDelete(L, 7);

	int i = 1;
	LinkList prt = L;
	while (prt != NULL) {
		printf("����ĵ�%d��Ԫ��Ϊ��%s\n", i, (char*)GetElem(L, i)->data);
		prt = prt->next;
		i++;
	}
	return 0;
}