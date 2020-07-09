#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include "klock.h"

SmartLock glocks[2];

void testA();
void testB();

void *thread_0(void *arg)
{
    while (lock(&glocks[0]) == 0); // Force locking glocks[0]
  	{
  		printf("Thread0 glock[0]\n");
   		sleep(1);
   	}
    while (lock(&glocks[1]) == 0); // Force locking glocks[1]
	{
		printf("Thread0 glock[1]\n");
	}

    printf("thread 0 is working on critical section for 1 second\n");

    sleep(1);

    unlock(&glocks[0]);
    unlock(&glocks[1]);

    return NULL;
}

void *thread_1(void *arg)
{
    while (1)
    {
        int lock1_res = lock(&glocks[1]);
        printf("Thread1 glock[1]\n");
        sleep(2);

        if (lock1_res)
        {
            int lock0_res = lock(&glocks[0]);
            printf("Thread1 glock[0]\n");

            if (lock0_res)
            {
                printf("thread 1 is working on critical section for 1 second\n");
                sleep(1);
                unlock(&glocks[1]);
                unlock(&glocks[0]);
                break;
            }
            else
            {
            	// If thread_1 is not able to lock glocks[0] now, it will also
            	// unlock glocks[1] and sleep for 1 second before retry so that
            	// thread_0 can acquire glocks[1]
                unlock(&glocks[1]);
                sleep(1);
            }
        }
    }
    return NULL;
}

void *thread_2(void *arg)
{
    while (1)
    {
        int lock0 = lock(&glocks[0]);
        int lock1 = lock(&glocks[1]);

        if (lock0 == 1 && lock1 == 1)
        {
            printf("thread 2 is working on critical section for 1 second\n");
            sleep(1);
            unlock(&glocks[1]);
            unlock(&glocks[0]);
            break;
        }
    }
	return NULL;
}

void testA()
{
	init_lock(&glocks[0]);
	init_lock(&glocks[1]);

	pthread_t tids[2];

	pthread_create(&tids[0], NULL, thread_0, NULL);
	pthread_create(&tids[1], NULL, thread_1, NULL);

	pthread_join(tids[0], NULL);
	pthread_join(tids[1], NULL);
}

void testB()
{
	init_lock(&glocks[0]);
	init_lock(&glocks[1]);

	pthread_t tids;

	pthread_create(&tids, NULL, thread_2, NULL);

	pthread_join(tids, NULL);

}
/* This is a simple deadlock condition similar to the RAG showed in
 * assignment web page.
 * The critical sections of thread_0 and thread_1 should both be able
 * to invoke if the klock is implemented correctly, and there should
 * be no memory leak after finishing the main function.*/
int main(int argc, char *argv[])
{

	//testA();

	testB();


    // You can assume that cleanup will always be the last function call
    // in main function of the test cases.
    cleanup();

    return 0;
}
