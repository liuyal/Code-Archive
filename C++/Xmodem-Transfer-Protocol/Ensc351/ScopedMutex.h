
#ifndef SCOPEDMUTEX_H_
#define SCOPEDMUTEX_H_

#include <pthread.h>

class ScopedMutex {
public:
	ScopedMutex(pthread_mutex_t* SMutexP);
	virtual ~ScopedMutex();

private:
	pthread_mutex_t* mutexP;
};

#endif /* SCOPEDMUTEX_H_ */
