#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <stdbool.h>
#include "list.h"

static _Bool doSinglePassOnSort(struct nodeStruct **headRef);
static void swapElements(struct nodeStruct **previous, struct nodeStruct *nodeA, struct nodeStruct *b);

struct nodeStruct* List_createNode(int size, void *memory)
{
	struct nodeStruct *pNode = malloc(sizeof(struct nodeStruct));
	if (pNode != NULL)
	{
		pNode->size = size;
		pNode->memory = memory;
	}
	return pNode;
}

void List_insertHead(struct nodeStruct **headRef, struct nodeStruct *node)
{
	node->next = *headRef;
	*headRef = node;
}

void List_insertTail(struct nodeStruct **headRef, struct nodeStruct *node)
{
	node->next = NULL;

	if (*headRef == NULL)
	{
		*headRef = node;
	}
	else
	{
		struct nodeStruct *current = *headRef;

		while (current->next != NULL)
		{
			current = current->next;
		}
		current->next = node;
	}
}

int List_countNodes(struct nodeStruct *head)
{
	int count = 0;
	struct nodeStruct *current = head;
	while (current != NULL)
	{
		current = current->next;
		count++;
	}
	return count;
}

struct nodeStruct* List_findNode(struct nodeStruct *head, void *memory)
{
	struct nodeStruct *current = head;
	while (current != NULL)
	{
		if (current->memory == memory)
		{
			return current;
		}
		current = current->next;
	}
	return NULL;
}

struct nodeStruct* List_GetTail(struct nodeStruct *head)
{
	struct nodeStruct *current = head;
	while (current->next != NULL)
	{
		current = current->next;
	}
	return current;
}

void List_deleteNode(struct nodeStruct **headRef, struct nodeStruct *node)
{
	assert(headRef != NULL);
	assert(*headRef != NULL);

	if (*headRef == node)
	{
		*headRef = node->next;
	}
	else
	{
		// Find the previous node:
		struct nodeStruct *previous = *headRef;
		while (previous->next != node)
		{
			previous = previous->next;
			assert(previous != NULL);
		}
		// Unlink node:
		assert(previous->next == node);
		previous->next = node->next;
	}
	// Free memory:
	free(node);
}

void deleteList(struct nodeStruct** head_ref)
{
   struct nodeStruct* current = *head_ref;
   struct nodeStruct* next;
 
   while (current != NULL) 
   {
       next = current->next;
       free(current);
       current = next;
   }
   *head_ref = NULL;
}

void List_sort(struct nodeStruct **headRef)
{
	while (doSinglePassOnSort(headRef)) {}
}
static _Bool doSinglePassOnSort(struct nodeStruct **headRef)
{
	_Bool didSwap = false;
	while (*headRef != NULL)
	{
		struct nodeStruct *nodeA = *headRef;

		// If we don't have 2 remaining elements, nothing to swap.
		if (nodeA->next == NULL) { break; }
		struct nodeStruct *nodeB = nodeA->next;
		// Swap needed?
		if (nodeA->memory > nodeB->memory)
		{
			swapElements(headRef, nodeA, nodeB);
			didSwap = true;
		}
		// Advance to next elements
		headRef = &((*headRef)->next);
	}
	return didSwap;
}
static void swapElements(struct nodeStruct **previous, struct nodeStruct *nodeA, struct nodeStruct *nodeB)
{
	*previous = nodeB;
	nodeA->next = nodeB->next;
	nodeB->next = nodeA;
}

void cleanFreeList(struct nodeStruct *head) // NEED FIX
{
	struct nodeStruct *current = head;
	int currentSize = 0;
	int nextSize = 0;
	void* currentMemory = NULL;
	void* nextMemory = NULL;

	if (current == NULL || current->next == NULL) { return; }

	while (current->next != NULL)
	{
		currentSize = current->size;
		currentMemory = current->memory;
		nextSize = current->next->size;
		nextMemory = current->next->memory;

		if ((void*)((char*)currentMemory + currentSize) >= nextMemory)
		{
			current->size = currentSize + nextSize;
			List_deleteNode(&current, current->next);
			current = head;
			if (current->next == NULL) { return; }
		}
		else
		{
			current = current->next;
		}
	}
}