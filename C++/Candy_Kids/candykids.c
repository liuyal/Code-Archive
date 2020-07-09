#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <errno.h>
#include <signal.h>
#include <assert.h>
#include <semaphore.h>
#include <time.h>

#include "bbuff.h"
#include "stats.h"

//Stop Flag
_Bool stop_thread = false;

typedef struct 
{
	int factory_number;
	double time_stamp_in_ms;
} candy_t;


double current_time_in_ms(void)
{
    struct timespec now;
    clock_gettime(CLOCK_REALTIME, &now);
    return now.tv_sec * 1000.0 + now.tv_nsec/1000000.0;
}


void *factory_thread_function(void* param)
{
	//printf("%s\n", "making factory");
	srand(time(NULL));
	int factoryID = *((int *) param);
	//int factoryID = (int)(intptr_t)param;

	while(!stop_thread)
	{
		int factoryWait = rand() % 4;

		printf("\tFactory %d ships candy & waits %ds\n", factoryID, factoryWait);
		
		candy_t* newCandy = malloc(sizeof(candy_t));
   		newCandy->factory_number = factoryID;
    	newCandy->time_stamp_in_ms = current_time_in_ms();
    	
    	bbuff_blocking_insert(newCandy);
    	stats_record_produced(factoryID);

		sleep(factoryWait);
	}

	return NULL;
}


void *kids_thread_function(void* param)
{
	//printf("%s\n", "making kids");
	//int kidID = *((int *) param);
	srand(time(NULL));
	int candyEat = 0;

	while(1)
	{
		int kidWait = rand()%2;

		candy_t* kidCandy = bbuff_blocking_extract();

		if (kidCandy != NULL)
		{
			//printf("\tkid %d ate candy & waits %ds\n", kidID, kidWait);
			candyEat++;
			stats_record_consumed(kidCandy->factory_number, current_time_in_ms() - kidCandy->time_stamp_in_ms);
		}

		sleep(kidWait);
		free(kidCandy);
	}

	return NULL;
}


int main (int argc, char *argv[])
{
	// 1.  Extract arguments
	char *command = argv[0];
	int factories_num = atoi(argv[1]);
	int kids_num = atoi(argv[2]);
	int seconds = atoi(argv[3]);

	printf("inputs: %s %d %d %d\n\n", command, factories_num, kids_num, seconds);

	if (factories_num <= 0 || kids_num <= 0 || seconds <= 0)
	{
		printf("%s\n", "Error: All arguments must be positive.");
		exit(-1);
	}

	// 2.  Initialize modules
	bbuff_init();
	stats_init(factories_num);

	// 3.  Launch candy-factory threads
	pthread_t factory_threads[factories_num]; 
	int factory_id[factories_num]; 

	for (int i = 0 ; i < factories_num; i++)
	{
		factory_id[i] = i;
		pthread_attr_t attr;
        pthread_attr_init(&attr);

		if (pthread_create(&factory_threads[i], &attr, factory_thread_function, &factory_id[i])) 
		{
			printf ("Create pthread error!\n");
			exit (1);
		}
	}

	// 4.  Launch kid threads
	pthread_t kid_threads[kids_num];
	int kid_id[kids_num]; 

	for (int i = 0; i < kids_num; i++)
	{	
		kid_id[i] = i;
		pthread_attr_t attr;
        pthread_attr_init(&attr);
		
		if (pthread_create(&kid_threads[i], &attr, kids_thread_function, &kid_id[i])) 
		{
			printf ("Create pthread error!\n");
			exit (1);
		}
	}

	// 5.  Wait for requested time
	for (int i = 0; i < seconds; i++)
	{
		printf("Time %is:\n", i);
		sleep(1);
	}
	
	// 6.  Stop candy-factory threads
	printf("%s\n", "Stopping candy factories...");

	stop_thread = true;

	for (int i = 0; i < factories_num; i++)
	{
		pthread_join(factory_threads[i],  NULL);
		printf("Candy-factory %d done\n", i);
	}

	// 7.  Wait until no more candy
	while(!bbuff_is_empty())
	{
		printf("Wait until no more candy\n");
		sleep(1);
	}

	// 8.  Stop kid threads
	printf("%s\n", "Stopping kids.");

	for (int i = 0; i < kids_num; i++) 
	{
		pthread_cancel(kid_threads[i]);
		pthread_join(kid_threads[i], NULL);
	}

	// 9.  Print statistics
	printf("%s\n", "Statistics:");
	stats_display();

	// 10. Cleanup any allocated memory
	stats_cleanup();

	return 0;
}