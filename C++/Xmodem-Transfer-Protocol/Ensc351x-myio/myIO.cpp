
#include <unistd.h>			// for read/write/close
#include <fcntl.h>			// for open/creat
#include <sys/socket.h> 		// for socketpair
#include <algorithm>    // std::max
#include <vector>
#include <mutex>
#include <condition_variable>
#include <iostream>

#include "myIO.h"
#include "SocketReadcond.h"

using namespace std;

class ThreadLock
{
public:
	int bufsize = 0;
	int match_pair = -1;
	std::mutex mutx;
	std::condition_variable cond_var;
};

#define num_sockets 4

static std::vector<ThreadLock*> VecThreadLock( num_sockets );
std::mutex vectorMutex;

//Create Thread 2 lock obj add to vector
int mySocketpair( int domain, int type, int protocol, int des[2] )
{
	int returnVal = socketpair(domain, type, protocol, des);

	std::lock_guard<std::mutex> lock(vectorMutex);

	VecThreadLock.resize(max(des[0],des[1]) + 1);

	ThreadLock *first_sock = new ThreadLock;
	ThreadLock *second_sock = new ThreadLock;
	first_sock-> match_pair = des[1];
	second_sock-> match_pair = des[0];
	VecThreadLock[des[0]] = first_sock;
	VecThreadLock[des[1]] = second_sock;

	return returnVal;
}

int myOpen(const char *pathname, int flags, mode_t mode)
{
	int return_open =  open(pathname, flags, mode);
	std::unique_lock<std::mutex> lock(vectorMutex);

	if(return_open >= VecThreadLock.size())
	{ VecThreadLock.resize(return_open + 1); }

	if(!VecThreadLock[return_open])
	{ VecThreadLock[return_open] = new ThreadLock();}

	VecThreadLock[return_open]->bufsize = 0;
	VecThreadLock[return_open]->match_pair = 0;

	return return_open;
}

int myCreat(const char *pathname, mode_t mode)
{
	int return_create =  creat(pathname, mode);
	std::unique_lock<std::mutex> lock(vectorMutex);

	if(return_create >= VecThreadLock.size())
	{ VecThreadLock.resize(return_create + 1); }

	if(!VecThreadLock[return_create])
	{ VecThreadLock[return_create] = new ThreadLock();}

	VecThreadLock[return_create]->bufsize = 0;
	VecThreadLock[return_create]->match_pair = 0;

	return return_create;
}
int myClose( int fd )
{
	// mod for close sockets
	if (VecThreadLock[fd])
	{
		std::unique_lock<std::mutex> lock(vectorMutex);
		delete VecThreadLock[fd];
		VecThreadLock[fd] = NULL;
	}
	return close(fd);
}

ssize_t myRead( int fildes, void* buf, size_t nbyte )
{
	return myReadcond(fildes, buf,nbyte, 1, 0, 0);
}

//Lock, Write , IncBuf  unlock at return
ssize_t myWrite( int fildes, const void* buf, size_t nbyte )
{
	int index = VecThreadLock[fildes]->match_pair;
	//std::unique_lock<std::mutex> lock(VecThreadLock[fildes]->mutx);
	ssize_t byteswrite = write(fildes, buf, nbyte );

		VecThreadLock[index]->bufsize += byteswrite;
		VecThreadLock[index]->cond_var.notify_all();

	return byteswrite;
}

//Lock, Wread, decrBuf unlock at return
int myReadcond(int des, void * buf, int n, int min, int time, int timeout)
{
	int index = VecThreadLock[des]->match_pair;
	//std::unique_lock<std::mutex> lk(VecThreadLock[index]->mutx);
	ssize_t bytesRead = wcsReadcond(des, buf, n, min, time, timeout );

		VecThreadLock[des]->bufsize -= bytesRead;
		VecThreadLock[index]->cond_var.notify_all();

	return bytesRead;
}

//Lock, block read
int myTcdrain(int des)
{
	int index = VecThreadLock[des]->match_pair;
	std::unique_lock<std::mutex> lock(VecThreadLock[index]->mutx);

	//Handel read or write
	VecThreadLock[des]->cond_var.wait(lock, [des]() {//	return VecThreadLock[des]->bufsize <= 0;});
		if (des % 2 == 0)
			return (VecThreadLock[des]->bufsize <= 1);
		else
			return (VecThreadLock[VecThreadLock[des]->match_pair]->bufsize == 0);});

	VecThreadLock[des]->bufsize = 0;
	VecThreadLock[index]->bufsize = 0;
	return 0;
}


