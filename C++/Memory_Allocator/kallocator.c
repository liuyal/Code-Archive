#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "kallocator.h"
#include "list.h"

struct KAllocator
{
	enum allocation_algorithm aalgorithm;
	int size;
	int currentSize;
	void* memory;
	struct nodeStruct* allocatedList;
	struct nodeStruct* freeList;
};

struct KAllocator kallocator;

void initialize_allocator(int _size, enum allocation_algorithm _aalgorithm)
{
	assert(_size > 0);
	char* address = NULL;

	kallocator.aalgorithm = _aalgorithm;
	kallocator.size = _size;
	kallocator.memory = malloc((size_t)kallocator.size);
	address = (char*)kallocator.memory;

	for (int i = 0; i < _size; i++) { address[i] = 0; }

	kallocator.currentSize = 0;
	kallocator.allocatedList = NULL;
	kallocator.freeList = NULL;

	List_insertHead(&kallocator.freeList, List_createNode(_size, kallocator.memory));
}

// free other dynamic allocated memory to avoid memory leak
void destroy_allocator()
{
	deleteList(&kallocator.allocatedList);
 	deleteList(&kallocator.freeList);

	free(kallocator.memory);
	free(kallocator.freeList);
	free(kallocator.allocatedList);
}

// Allocate memory from kallocator.memory 
// ptr = address of allocated memory
void* kalloc(int _size)
{
	void* ptr = NULL;
	void* base = kallocator.memory;
	bool FL_Available = false;

	if (kallocator.allocatedList == NULL) // NO block in memory
	{
		List_insertHead(&kallocator.allocatedList, List_createNode(_size, base));
		kallocator.currentSize += _size;
		kallocator.freeList->size -= _size;
		kallocator.freeList->memory = (void*)((char*)base + _size);
		return base;
	}

	if (kallocator.freeList == NULL) // CAN NEVER HAPPEN
	{
		struct nodeStruct* TailNode = List_GetTail(kallocator.allocatedList);
		ptr = (void*)((char*)TailNode->memory + TailNode->size);
		List_insertTail(&kallocator.allocatedList, List_createNode(_size, ptr));
		kallocator.currentSize += _size;
		return ptr;
	}
	else //CHECK If gap in free list is big enough
	{
		struct nodeStruct* currentNode = kallocator.freeList;
		while (currentNode != NULL)
		{
			if (_size <= currentNode->size) { FL_Available = true; break; }
			currentNode = currentNode->next;
		}
	}

	if (!FL_Available) // no gap big enough insert at end
	{
		struct nodeStruct* TailNode = List_GetTail(kallocator.allocatedList);
		ptr = (void*)((char*)TailNode->memory + TailNode->size);
		List_insertTail(&kallocator.allocatedList, List_createNode(_size, ptr));
		kallocator.currentSize += _size;
		return ptr;
	}

	if (kallocator.aalgorithm == FIRST_FIT)
	{
		struct nodeStruct* currentNode = kallocator.freeList;
		int size = 0;
		void *memory = NULL;

		while (currentNode != NULL)
		{
			size = currentNode->size;
			memory = currentNode->memory;

			if (_size == size)
			{
				ptr = memory;
				List_deleteNode(&kallocator.freeList, currentNode);
				break;
			}
			else if (_size < size)
			{
				ptr = memory;
				currentNode->size = currentNode->size - _size;
				currentNode->memory = (void*)((char*)memory + _size);
				break;
			}
			else if (_size > size) {} //DO NOTHING

			currentNode = currentNode->next;
		}
	}
	else if (kallocator.aalgorithm == BEST_FIT)
	{
		struct nodeStruct* currentNode = kallocator.freeList;
		struct nodeStruct* tempNode = kallocator.freeList;
		int bestSize = kallocator.size;
		int index = 0;
		void *memory = NULL;

		while (currentNode != NULL)
		{
			if (_size <= currentNode->size && bestSize > currentNode->size)
			{
				bestSize = currentNode->size;
				memory = currentNode->memory;
				tempNode = currentNode;
			}
			index++;
			currentNode = currentNode->next;
		}

		if (_size == bestSize)
		{
			ptr = memory;
			List_deleteNode(&kallocator.freeList, tempNode);
		}
		else if (_size < bestSize)
		{
			ptr = memory;
			tempNode->size = tempNode->size - _size;
			tempNode->memory = (void*)((char*)memory + _size);
		}
	}
	else if (kallocator.aalgorithm == WORST_FIT)
	{
		struct nodeStruct* currentNode = kallocator.freeList;
		struct nodeStruct* tempNode = kallocator.freeList;
		int bestSize = 0;
		int index = 0;
		void *memory = NULL;

		while (currentNode != NULL)
		{
			if (bestSize < currentNode->size)
			{
				bestSize = currentNode->size;
				memory = currentNode->memory;
				tempNode = currentNode;
			}
			index++;
			currentNode = currentNode->next;
		}

		if (_size == bestSize)
		{
			ptr = memory;
			List_deleteNode(&kallocator.freeList, tempNode);
		}
		else if (_size < bestSize)
		{
			ptr = memory;
			tempNode->size = tempNode->size - _size;
			tempNode->memory = (void*)((char*)memory + _size);
		}
	}

	List_insertTail(&kallocator.allocatedList, List_createNode(_size, ptr));

	List_sort(&kallocator.allocatedList);

	kallocator.currentSize += _size;

	return ptr;
}

void kfree(void* _ptr)
{
	assert(_ptr != NULL);

	char* address = _ptr;

	struct nodeStruct* FreeNode = List_findNode(kallocator.allocatedList, _ptr);
	int size = FreeNode->size;
	void* memory = FreeNode->memory;

	struct nodeStruct* NewNode = List_createNode(size, memory);

	List_insertTail(&kallocator.freeList, NewNode);

	List_sort(&kallocator.freeList);

	cleanFreeList(kallocator.freeList);

	List_deleteNode(&kallocator.allocatedList, FreeNode);

	for (int i = 0; i < size; i++) { address[i] = 0; }

	kallocator.currentSize -= size;
}

// compact allocated memory
// update _before, _after and compacted_size
int compact_allocation(void** _before, void** _after)
{
	int compacted_size = 0;
	char* Nextaddress = NULL;
	void** bAddr = NULL;
	void** afAddr = NULL;
	int chunkSize = 0;
	int i = 0;
	int j = 0;

	struct nodeStruct* OPNode = kallocator.allocatedList;
	struct nodeStruct* TailNode = NULL;

	if (kallocator.allocatedList == NULL)// 0 item
	{
		_before[0] = _after[0] = NULL;
		return 0;
	}
	else if (kallocator.allocatedList->next == NULL)// 1 item
	{
		if (kallocator.allocatedList->memory == kallocator.memory) //1 item @ base
		{
			_before[0] = _after[0] = kallocator.memory;
		}
		else // 1 item not @ base
		{
			_before[0] = kallocator.allocatedList->memory;
			_after[0] = kallocator.memory;

			// SET MEMORY***
			bAddr = _before[0];
			afAddr = _after[0];
			afAddr[0] = bAddr[0];
			bAddr[0] = NULL;

			kallocator.allocatedList->memory = kallocator.memory;

			kallocator.freeList->memory = (void*)((char*)_before[0] + kallocator.allocatedList->size);

			cleanFreeList(kallocator.freeList);
		}
		return 1;
	}

	List_sort(&kallocator.allocatedList);
	List_sort(&kallocator.freeList);

	while (OPNode != NULL) //Save before
	{
		_before[i] = OPNode->memory;
		OPNode = OPNode->next;
		i++;
	}

	OPNode = kallocator.allocatedList;
	chunkSize = OPNode->size;
	OPNode->memory = kallocator.memory;
	Nextaddress = (void*)((char*)kallocator.memory + chunkSize);
	OPNode = OPNode -> next;

	while (OPNode != NULL) //COMPACT MEMORY
	{
		OPNode->memory = Nextaddress;
		chunkSize = OPNode->size;
		Nextaddress = (void*)((char*)Nextaddress + chunkSize);
		OPNode = OPNode->next;
	}

	OPNode = kallocator.allocatedList;

	while (OPNode != NULL) 	// Save After
	{
		_after[j] = OPNode->memory;
		OPNode = OPNode->next;
		j++;
	}

	if (i != j) { printf("COMPACTION ERROR!!!\n"); }

	//Update memory
	for (int k = 0; k < j; k++)
	{
		//GET Value at before -> STORE VALUE AT AFTER
		bAddr = _before[k];
		afAddr = _after[k];
		*afAddr = *bAddr; // ISSUE****
		*bAddr = NULL;
	}
	
	//Update Free List
	TailNode = List_GetTail(kallocator.allocatedList);
	Nextaddress = (void*)((char*)TailNode->memory + TailNode->size);
	OPNode = kallocator.freeList;
	while (OPNode != NULL) 
	{
		OPNode->memory = Nextaddress;
		OPNode = OPNode->next;
	}
	cleanFreeList(kallocator.freeList);

	compacted_size = j;
	return compacted_size;
}

// Calculate available memory size
int available_memory()
{
	int available_memory_size = 0;
	available_memory_size = kallocator.size - kallocator.currentSize;
	return available_memory_size;
}

// Calculate the statistics
void print_statistics()
{
	int allocated_size = 0;
	int allocated_chunks = 0;
	int free_size = 0;
	int free_chunks = 0;
	int smallest_free_chunk_size = 0;
	int largest_free_chunk_size = 0;

	struct nodeStruct* tempAlloc = kallocator.allocatedList;
	struct nodeStruct* tempFree = kallocator.freeList;

	allocated_size = kallocator.size - available_memory();
	
	while (tempAlloc != NULL)
	{
		allocated_chunks++;
		tempAlloc = tempAlloc->next;
	}

	free_size = available_memory();

	smallest_free_chunk_size = tempFree->size;

	while (tempFree != NULL)
	{
		if (smallest_free_chunk_size > tempFree->size)
		{
			smallest_free_chunk_size = tempFree->size;
		}
		if (largest_free_chunk_size < tempFree->size)
		{
			largest_free_chunk_size = tempFree->size;
		}
		free_chunks++;
		tempFree = tempFree->next;
	}

	printf("Allocated size = %d\n", allocated_size);
	printf("Allocated chunks = %d\n", allocated_chunks);
	printf("Free size = %d\n", free_size);
	printf("Free chunks = %d\n", free_chunks);
	printf("Largest free chunk size = %d\n", largest_free_chunk_size);
	printf("Smallest free chunk size = %d\n\n", smallest_free_chunk_size);
}

