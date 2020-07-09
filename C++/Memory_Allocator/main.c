#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "kallocator.h"

void* initializeTest(int **p, int size);
void printArray(int **p, int size);
void printMemory(int **p, int size, char* base);

void testStats();

void test1();
void test2();
void test3();
void test4();
void test5();

void testA();
void testB();
void testC();
void testD();
void testE();
void testE2();
void testF();
void testF2();

void testComp();
void testComp2();
void testComp3();

void* initializeTest(int **p, int size)
{
	printf("InitializeTest...\n");

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));
		if (p[i] == NULL) { printf("Allocation failed\n");continue; } 
		if (i == 0) { *(p[i]) = i; }
		else { *(p[i]) = i; }
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");
	void* base = p[0];

	return base;
}

void printArray( int **p, int size)
{
	//printf("Print Arrray...\n");
	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}
}

void printMemory(int **p, int size,  char* base)
{
	//printf("Print Memory...\n");
	char* addrIndex = NULL;
	int A, B, C, D = 0;
	unsigned int result = 0;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: ", j, addrIndex);
		D = addrIndex[3]; C = addrIndex[2];B = addrIndex[1]; A = addrIndex[0];
		result = (D << 24) | (C << 16) | (B << 8) | A;
		printf("%u\n", result);
	}
}

void testStats()
{
	printf("//////////////////// Stats Test ////////////////////"); printf("\n\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();

	kfree(p[0]); p[0] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();

	kfree(p[1]); p[1] = NULL;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();

	kfree(p[3]); p[3] = NULL;
	kfree(p[5]); p[5] = NULL;
	kfree(p[7]); p[7] = NULL;
	kfree(p[9]); p[8] = NULL;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();

	destroy_allocator();
}

void test1()
{
	printf("//////////////////// Init Test ////////////////////\n\n");

	initialize_allocator(100, FIRST_FIT);

	int* p[50] = { NULL };
	int size = 10;
	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");
	void* base = p[0];
	char* addrIndex = base;

	print_statistics();

	kfree(p[1]); p[1] = NULL;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base; print_statistics();

	kfree(p[0]); p[0] = NULL;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base; print_statistics();
	 
	kfree(p[3]); p[3] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[7]); p[7] = NULL;
	kfree(p[8]); p[8] = NULL;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base; print_statistics();

	kfree(p[2]); p[2] = NULL;
	kfree(p[9]); p[9] = NULL;
	kfree(p[5]); p[5] = NULL;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base;

	print_statistics();
	destroy_allocator();
}

void test2()
{
	printf("//////////////////// FIRST_FIT Test ////////////////////\n\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	kfree(p[3]); p[3] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;

	printf("REmove [3] [6] [8]\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("Kalloc 999999\n");
	p[0] = kalloc(sizeof(int)); if (p[0] == NULL) { printf("Allocation failed\n"); } *(p[0]) = 999999;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("Kalloc 78\n");
	p[0] = kalloc(sizeof(int)); if (p[0] == NULL) { printf("Allocation failed\n"); } *(p[0]) = 78;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("Kalloc 25\n");
	p[0] = kalloc(sizeof(int)); if (p[0] == NULL) { printf("Allocation failed\n"); } *(p[0]) = 25;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	destroy_allocator();
}

void test3()
{
	printf("//////////////////// BEST_FIT Test ////////////////////\n\n");

	initialize_allocator(100, BEST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");print_statistics();

	p[10] = kalloc(sizeof(int)); if (p[10] == NULL) { printf("Allocation failed\n"); } *(p[10]) = 10; size++;
	p[11] = kalloc(sizeof(int)); if (p[11] == NULL) { printf("Allocation failed\n"); } *(p[11]) = 11; size++;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	kfree(p[3]); p[3] = NULL;
	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;
	print_statistics();

	kfree(p[5]); p[5] = NULL;
	kfree(p[6]); p[6] = NULL;
	print_statistics();

	kfree(p[9]); p[9] = NULL;
	kfree(p[10]); p[10] = NULL;
	kfree(p[11]); p[11] = NULL;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	p[1] = kalloc(8); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 99;
	printf("Best Fit insert size: 8, value 999...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	p[1] = kalloc(4); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 43;
	printf("Best Fit insert size: 4, value 43...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	p[1] = kalloc(5); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 55;
	printf("Best Fit insert size: 5, value 55...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	p[1] = kalloc(11); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 151;
	printf("Best Fit insert size: 11, value 151...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	destroy_allocator();
}

void test4()
{
	printf("//////////////////// WORST_FIT Test ////////////////////\n\n");

	initialize_allocator(100, WORST_FIT);
	int* p[50] = { NULL };
	int size = 20;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	kfree(p[3]); p[3] = NULL;
	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;

	kfree(p[5]); p[5] = NULL;
	kfree(p[6]); p[6] = NULL;

	kfree(p[8]); p[8] = NULL;
	kfree(p[9]); p[9] = NULL;
	kfree(p[10]); p[10] = NULL;
	kfree(p[11]); p[11] = NULL;
	kfree(p[12]); p[12] = NULL;
	kfree(p[13]); p[13] = NULL;

	kfree(p[15]); p[15] = NULL;
	kfree(p[16]); p[16] = NULL;
	kfree(p[17]); p[17] = NULL;

	kfree(p[19]); p[19] = NULL;

	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	p[1] = kalloc(8); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 99;
	printf("Worst Fit insert size: 8, value 99...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	p[1] = kalloc(4); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 16;
	printf("Worst Fit insert size: 4, value 16...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	p[1] = kalloc(4); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 44;
	printf("Worst Fit insert size: 4, value 44...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();
	destroy_allocator();
}

void test5()
{
	printf("//////////////////// FreeList Not Enough Test ////////////////////\n\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	kfree(p[0]); p[0] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;

	p[1] = kalloc(8); if (p[1] == NULL) { printf("Allocation failed\n"); } *(p[1]) = 44; size++;
	printf("Insert size: 8 (Check End), value 44...\n");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	kfree(p[1]); p[1] = NULL;
	printf("Remvoe last block(free list last block size = 8)...");
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();
	destroy_allocator();
}

void testA()
{
	printf("//////////////////// TESTA - Base ////////////////////"); printf("\n");

	initialize_allocator(100, FIRST_FIT);

	printf("Using first fit algorithm on memory size 100\n");
	int* p[50] = { NULL };

	for (int i = 0; i < 10; ++i) {
		p[i] = kalloc(sizeof(int));
		if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	print_statistics();

	for (int i = 0; i < 10; ++i) {
		if (i % 2 == 0) { continue; }
		printf("Freeing p[%d]\n", i);kfree(p[i]);p[i] = NULL;
	}printf("\n");

	for (int j = 0; j < 10; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}

	printf("available_memory %d", available_memory());
	void* before[100] = { NULL };
	void* after[100] = { NULL };
	compact_allocation(before, after);

	printf("\n\n");
	print_statistics();
	destroy_allocator();
}

void testB()
{
	printf("//////////////////// TESTB - free test ////////////////////"); printf("\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));
		if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	kfree(p[1]); p[1] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	kfree(p[3]);p[3] = NULL;
	kfree(p[4]);p[4] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	kfree(p[6]);p[6] = NULL;
	kfree(p[8]);p[8] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	kfree(p[7]);p[7] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testC()
{
	printf("//////////////////// TESTC - kalloc test ////////////////////"); printf("\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));
		if (p[i] == NULL) { printf("Allocation failed\n");continue; }
		*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	kfree(p[1]); p[1] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;
	kfree(p[7]); p[7] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	printf("Insert at P[1]\n");
	p[1] = kalloc(sizeof(int));if (p[1] == NULL) { printf("Allocation failed\n"); }*(p[1]) = 99;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	printf("Insert at P[3]\n");
	p[3] = kalloc(sizeof(int));if (p[3] == NULL) { printf("Allocation failed\n"); }*(p[3]) = 44;

	for (int j = 0; j < size; j++)
	{
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	printf("Insert at P[7]\n");
	p[7] = kalloc(sizeof(int));if (p[7] == NULL) { printf("Allocation failed\n"); }*(p[7]) = 777;

	for (int j = 0; j < size; j++)
	{
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	printf("Insert at P[8]\n");
	p[8] = kalloc(sizeof(int));if (p[8] == NULL) { printf("Allocation failed\n"); }*(p[8]) = 808;

	p[8] = kalloc(sizeof(int));if (p[8] == NULL) { printf("Allocation failed\n"); }*(p[8]) = 909;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testD()
{
	printf("//////////////////// TESTC - Algo test FF ////////////////////"); printf("\n");

	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	kfree(p[1]); p[1] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;
	kfree(p[7]); p[7] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[3] = kalloc(7);if (p[3] == NULL) { printf("Allocation failed\n"); }*(p[3]) = 7;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testE()
{
	printf("//////////////////// TESTC - Algo test BF ////////////////////"); printf("\n");

	initialize_allocator(100, BEST_FIT);
	int* p[50] = { NULL };
	int size = 10;

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[7]); p[7] = NULL;
	kfree(p[9]); p[9] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	printf("Insert at P[2]\n");
	p[1] = kalloc(sizeof(int));if (p[1] == NULL) { printf("Allocation failed\n"); }*(p[1]) = 2;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	kfree(p[1]); p[1] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[1] = kalloc(8);if (p[1] == NULL) { printf("Allocation failed\n"); }*(p[1]) = 8;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[2] = kalloc(12);if (p[2] == NULL) { printf("Allocation failed\n"); }*(p[2]) = 12;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testE2()
{
	printf("//////////////////// TESTC - Algo test BF2 ////////////////////"); printf("\n");

	initialize_allocator(100, BEST_FIT);
	int* p[50] = { NULL };
	int size = 10;

	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");

	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[5]); p[5] = NULL;
	kfree(p[8]); p[8] = NULL;
	kfree(p[7]); p[7] = NULL;
	kfree(p[9]); p[9] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[1] = kalloc(12);if (p[1] == NULL) { printf("Allocation failed\n"); }*(p[1]) = 12;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[8] = kalloc(8);if (p[8] == NULL) { printf("Allocation failed\n"); }*(p[8]) = 8;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testF()
{
	printf("//////////////////// TESTC - Algo test WF ////////////////////"); printf("\n");

	initialize_allocator(100, WORST_FIT);
	int* p[50] = { NULL };
	int size = 20;
	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");
	void* base = p[0];
	char* addrIndex = base;

	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[4]); p[4] = NULL;
	kfree(p[5]); p[5] = NULL;
	kfree(p[6]); p[6] = NULL;
	kfree(p[8]); p[8] = NULL;
	kfree(p[9]); p[9] = NULL;
	kfree(p[10]); p[10] = NULL;
	kfree(p[11]); p[11] = NULL;
	kfree(p[12]); p[12] = NULL;
	kfree(p[14]); p[14] = NULL;
	kfree(p[15]); p[15] = NULL;
	kfree(p[16]); p[16] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[8] = kalloc(sizeof(int)); if (p[8] == NULL) { printf("Allocation failed\n"); } *(p[8]) = 88;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[9] = kalloc(sizeof(int)); if (p[9] == NULL) { printf("Allocation failed\n"); } *(p[9]) = 99;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	p[2] = kalloc(sizeof(int)); if (p[2] == NULL) { printf("Allocation failed\n"); } *(p[2]) = 444;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	kfree(p[0]); p[0] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[7]); p[7] = NULL;
	kfree(p[8]); p[8] = NULL;
	kfree(p[9]); p[9] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base;

	kfree(p[13]); p[13] = NULL;
	kfree(p[17]); p[17] = NULL;
	kfree(p[18]); p[18] = NULL;
	kfree(p[19]); p[19] = NULL;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	print_statistics();
	destroy_allocator();
}

void testF2()
{
	printf("//////////////////// Free Test 2 ////////////////////"); printf("\n\n");

	initialize_allocator(100, WORST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	for (int i = 0; i < size; ++i) {
		p[i] = kalloc(sizeof(int));if (p[i] == NULL) { printf("Allocation failed\n");continue; }*(p[i]) = i;
		printf("p[%d] = %p ; *p[%d] = %d\n", i, p[i], i, *(p[i]));
	}printf("\n");
	void* base = p[0];
	char* addrIndex = base;

	kfree(p[0]); p[0] = NULL;

	p[8] = kalloc(sizeof(int)); if (p[8] == NULL) { printf("Allocation failed\n"); } *(p[8]) = 8;

	for (int j = 0; j < size; j++) {
		if (p[j] == NULL) { printf("p[%d] = %p ; *p[%d] = NULL\n", j, p[j], j); }
		else { printf("p[%d] = %p ; *p[%d] = %d\n", j, p[j], j, *(p[j])); }
	}printf("\n");

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base;

	kfree(p[1]); p[1] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[5]); p[5] = NULL;

	for (int j = 0; j < size; j++) {
		addrIndex = (char*)base + j * 4;
		printf("[%d] %p: %d\n", j, addrIndex, addrIndex[0]);
	}printf("\n"); addrIndex = base;

	print_statistics();
	destroy_allocator();
}

void testComp()
{
	printf("//////////////////// Compact Allocation ////////////////////"); printf("\n\n");
	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 20;
	char* base = (char*)initializeTest(&(*p), size);
	kfree(p[0]); p[0] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[5]); p[5] = NULL;
	kfree(p[11]); p[11] = NULL;
	kfree(p[13]); p[13] = NULL;
	kfree(p[15]); p[15] = NULL;
	kfree(p[17]); p[17] = NULL;
	kfree(p[18]); p[18] = NULL;
	kfree(p[19]); p[19] = NULL;
	printf("Print Array...\n"); printArray(&(*p), size);  printf("\n");
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("available_memory %d\n", available_memory());
	void* before[100] = { NULL };
	void* after[100] = { NULL };
	int count = compact_allocation(before, after);
	for (int i = 0; i < count; ++i) {	}

	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	destroy_allocator();
}

void testComp2()
{
	printf("//////////////////// COMP 1 @Base ////////////////////"); printf("\n\n");
	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 1;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("available_memory %d\n", available_memory());
	void* before[100] = { NULL };
	void* after[100] = { NULL };
	compact_allocation(before, after);

	destroy_allocator();
}

void testComp3()
{
	printf("//////////////////// COMP 1 NOT @Base ////////////////////"); printf("\n\n");
	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 6;
	char* base = (char*)initializeTest(&(*p), size);
	kfree(p[0]); p[0] = NULL;
	kfree(p[1]); p[1] = NULL;
	kfree(p[2]); p[2] = NULL;
	kfree(p[3]); p[3] = NULL;
	kfree(p[4]); p[4] = NULL;

	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	printf("available_memory %d\n", available_memory());
	void* before[100] = { NULL };
	void* after[100] = { NULL };
	compact_allocation(before, after);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	compact_allocation(before, after);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");
	print_statistics();

	destroy_allocator();
}

int main(int argc, char* argv[])
{
	testStats();

	test1();
	test2();
	test3();
	test4();
	test5();

	testA();
	testB();
	testC();
	testD();
	testE();
	testE2();
	testF();
	testF2();

	testComp();
	testComp2();
	testComp3();
	
	return 0;
}

/* TEST TEMPLATE***

void testTemp()
{
	printf("//////////////////// - ////////////////////"); printf("\n\n");
	initialize_allocator(100, FIRST_FIT);
	int* p[50] = { NULL };
	int size = 10;
	char* base = (char*)initializeTest(&(*p), size);
	printf("Print Memory...\n"); printMemory(&(*p), size, base); printf("\n");

	print_statistics();
	destroy_allocator();
}

*/