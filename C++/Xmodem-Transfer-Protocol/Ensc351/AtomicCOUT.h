

#include "ScopedMutex.h"
#include "AtomicConsole.h"
#include <iostream>

// this macro can be used for C++ console output where you don't want
// 	multiple threads interleaving their chained insertion operations.
//	It is used like:
//		COUT << "Hello " << "World." << endl;
//	Thanks to Javier *** for the idea.
//  This may not be the optimal way to acheive the desired effect.  It
//	might be better for each thread to build a stringStream referenced from TLS and
//  flush the stringStream when endl or flush is encountered.
#define COUT (ScopedMutex(&consoleMutex), std::cout)

#define CERR (ScopedMutex(&consoleMutex), std::cerr)
