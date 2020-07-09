
// File:        ccqueue.cpp
// Author:      Ya Qi Liu
// Date:        January 18, 2016 
// Description:  Implmentation of a customer complaint queue class

#include <sstream>
#include <string>

#include "ccqueue.h"


//----------------------------------------------CONSTRUCTOR------------------------------------------------------


// default constructor
// maxticketid begins at 0
// note that tickets does not need to be re-declared
CCQueue :: CCQueue()
{
	DLinkedList<Ticket> *tickets = new DLinkedList<Ticket>;
	maxticketid = 0;
}


//------------------------------------------------MUTATORS------------------------------------------------------


// enqueues a new ticket at the back of the ticket queue and returns true
// ticketid is assigned automatically as 1+maxticketid if enqueueing is possible
// does not enqueue and returns false if either parameter is empty string
// POST:  new ticket with supplied parameters is added to back of tickets,
//        maxticketid is incremented
// PARAM: customer and complaint fields to pass to Ticket constructor
bool CCQueue::Add(string customer, string complaint)
{
	if (customer.length() == 0 || complaint.length() == 0)
	{
		return false;
	}
	else
	{
		Ticket NewTicket = Ticket(maxticketid + 1, customer, complaint);

		tickets.InsertBack(NewTicket);

		maxticketid++;
		return true;
	}
}


// removes and returns an item from the front of the ticket queue
// throws a logic_error if the ticket queue is empty
// POST:  first item of the ticket queue is removed
Ticket CCQueue::Service()
{
	if (tickets.IsEmpty() == true)
	{
		throw std::out_of_range("Empty List");
	}
	
	Ticket RemovedTicket = tickets.RemoveAt(0);

	return RemovedTicket;

}


// moves an item towards the front of the queue by 1 position and returns true
// returns false if supplied index is 0 (first item) or outside the list boundaries
// POST:  DLinkedList items at position and position-1 swap spots in the list
// PARAM: initial index of item to move up
bool CCQueue::MoveUp(int index)
{
	if (index <= 0 || index >= tickets.Size())
	{
		return false;
	}

	Ticket RemovedTicket = tickets.RemoveAt(index);

	tickets.InsertAt(RemovedTicket, index - 1);


	return true;
}



// moves an item towards the back of the queue by 1 position and returns true
// returns false if supplied index is the last item or outside the list boundaries
// POST:  DLinkedList items at position and position+1 swap spots in the list
// PARAM: initial index of item to move down
bool CCQueue::MoveDown(int index)
{
	if (index >= tickets.Size() - 1 || index < 0)
	{
		return false;
	}

	Ticket RemovedTicket = tickets.RemoveAt(index);

	tickets.InsertAt(RemovedTicket, index + 1);


	return true;
}



//------------------------------------------------ACCESSORS------------------------------------------------------


// returns the number of tickets
int CCQueue::Size() const
{
	return tickets.Size();
}




