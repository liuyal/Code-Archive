
#include "ScopedMutex.h"
#include "VNPE.h"

//static pthread_mutex_t SMutex;

ScopedMutex::ScopedMutex(pthread_mutex_t* SMutexP)
:mutexP(SMutexP)
{
	PE_0(pthread_mutex_lock(mutexP));
}

ScopedMutex::~ScopedMutex() {
	PE_0(pthread_mutex_unlock(mutexP));
}
