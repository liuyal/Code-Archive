#ifndef __KLOCK_H__
#define __KLOCK_H__

#include<stdio.h>
#include <pthread.h>

typedef struct
{
	 pthread_mutex_t mutex;
	 long unsigned int uid;

} SmartLock;

void init_lock(SmartLock* lock);

int lock(SmartLock* lock);

void unlock(SmartLock* lock);

void cleanup();

#endif
