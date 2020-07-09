// Linked list module.

#ifndef LIST_H_
#define LIST_H_

struct nodeStruct
 {
    int size;
	void *memory;
    struct nodeStruct *next;
};

struct nodeStruct* List_createNode(int size, void *memory);

void List_insertHead (struct nodeStruct **headRef, struct nodeStruct *node);

void List_insertTail (struct nodeStruct **headRef, struct nodeStruct *node);

int List_countNodes (struct nodeStruct *head);

struct nodeStruct* List_findNode(struct nodeStruct *head, void *memory);

struct nodeStruct* List_GetTail(struct nodeStruct *head);

void List_deleteNode (struct nodeStruct **headRef, struct nodeStruct *node);

void deleteList(struct nodeStruct** head_ref);

void List_sort(struct nodeStruct **headRef);

void cleanFreeList(struct nodeStruct *headRef);

#endif
