
#ifdef _DLINKEDLIST_H_
 
// File:        dlinkedlist.cpp
// Author:      Ya Qi Liu
// Date:        January 18, 2016
// Description: Implmentation of a template doubly-linked-list class

#include <cstdlib>
#include <stdexcept>
#include <string>


//------------------------------------HELPER FUNCTIONS-----------------------------------------

// helper function for deep copy
// Used by copy constructor and operator=
template <class T>
void DLinkedList <T> :: CopyList(const DLinkedList& ll)
{
	//Check for Empty list
	if (ll.IsEmpty() == true)
	{
		this->size = 0;
		return;
	}
	//Initialize variables and temp is assigned to front of list
	Node<T>* temp = ll.front;
	this->size = 0;
	this->front = temp;
	this->back = temp;

	//Insert nodes of ll into this->list with loop
	while (temp != NULL)
	{
		this->InsertBack(temp->data);
		temp = temp->next;
	}
}


// helper function for deep delete
// Used by destructor and copy/assignment
template <class T>
void DLinkedList <T>::DeleteList()
{
	//Check for empty List
	if (front == NULL && back == NULL)
	{
		return;
	}

	//Traves through List and remove nodes
	Node<T>* temp = front;
	while (temp != NULL)
	{
		temp = front->next;
		delete front;
		front = temp;
	}
	//Set size to 0 and pointers to NULL
	size = 0;
	front = back = NULL;
}


//--------------------------------------------Constructors-------------------------------------------------   

// default constructor
//Initialize Template Class of Link List
template <class T>
DLinkedList<T>::DLinkedList()
{
	size = 0;
	front = NULL;
	back = NULL;
}


 // copy constructor, performs deep copy of list elements
template <class T>
 DLinkedList <T>:: DLinkedList(const DLinkedList& ll)
{
	//Use helper function
	CopyList(ll);
}


 // destructor
 template <class T>
 DLinkedList <T>::~DLinkedList()
 {
	 //Use helper function
	 DeleteList();
 }



//------------------------------------------------MUTATORS---------------------------------------------   

// Inserts an item at the front of the list
// POST:  List contains item at position 0
// PARAM: item = item to be inserted
template <class T>
void DLinkedList <T>::InsertFront(T item)
{
	Node<T>* temp = new Node<T>(item);
	//Empty List insert
	if (IsEmpty() == true)
	{
		front = temp;
		back = front;
	}
	//Insert at front of list
	else 
	{
		front->prev = temp;
		temp->next = front;
		front = temp;
	}
	size = size + 1;
}


// Inserts an item at the back of the list
// POST:  List contains item at back
// PARAM: item = item to be inserted
template <class T>
void DLinkedList <T>::InsertBack(T item)
{
	Node<T> *temp = new Node<T>(item);
	//Empty List insert
	if (IsEmpty() == true)
	{
		front = temp;
		back = front;
	}
	//Insert at back of list
	else
	{
		back->next = temp;
		temp->prev = back;
		back = temp;
	}
	size = size + 1;
}


// Inserts an item in position p (0-indexed)
// Throws exception for invalid index
// PRE:   0 <= p <= size
// POST:  List contains item at position p
// PARAM: item = item to be inserted, p = position where item will be inserted
template <class T>
void DLinkedList <T>::InsertAt(T item, int p)
{
	//Check for proper index within boundary
	if (p > size || p < 0)
	{
		//ERROR handle for out of Range
		throw std::out_of_range("Out of Range");
	}

	Node<T> *node = new Node<T>(item);
	Node<T> *current = front;
	int count = 0;

	//If index is at 0 (front of list) insert at front
	if (p == 0)
	{
		InsertFront(node->data);
		return;
	}
	//index if at 1 more end of list insert back
	else if (p == size)
	{
		InsertBack(node->data);
		return;
	}
	//Inerset at middle
	while (current)
	{
		//Traverse to index and insert
		if (count == p)
		{
			node->next = current;
			current->prev->next = node;
			node->prev = current->prev;
			current->prev = node;

			size = size + 1;
			return;
		}
		count++;
		current = current->next;
	}
}


// Removes and returns an item from position p (0-indexed)
// Throws exception if list is empty or index invalid
// PRE:   0 <= p <= size
// POST:  Item is removed from list
// PARAM: p = position from where item will be removed
template <class T>
T DLinkedList <T>::RemoveAt(int p)
{
	////Throw exception if list is empty
	if (IsEmpty() == true)
	{
		throw std::out_of_range("Empty List");
	}
	//Throw exception for p is out of range
	else if (p >= size || p < 0)
	{
		throw std::out_of_range("Out of Range");
	}

	Node<T> *deleteNode = front;
	T ReturnData = deleteNode->data;
	int count = 0;

	//Remove at first Node
	if (p == 0 && size > 1)
	{
		ReturnData = deleteNode->data;

		front = deleteNode->next;
		front->prev = NULL;

		delete deleteNode;
		size = size - 1;
		return ReturnData;
	}
	//Remove at Last Node
	else if (p == size-1 && size > 1)
	{
		deleteNode = back;
		ReturnData = deleteNode->data;
		back = deleteNode->prev;
		back->next = NULL;

		delete deleteNode;
		size = size - 1;
		return ReturnData;
	}
	//Remove Only Node
	else if (size == 1 && p == 0)
	{
		ReturnData = deleteNode->data;
		front = NULL;
		back = NULL;
		delete deleteNode;
		size = size - 1;
		return ReturnData;
	}
	//Remove Middle Node
	else
	{
		while (deleteNode != NULL)
		{
			if (count == p)
			{
				ReturnData = deleteNode->data;
				deleteNode->prev->next = deleteNode->next;
				deleteNode->next->prev = deleteNode->prev;

				delete deleteNode;
				size = size - 1;
				return ReturnData;
			}
			count++;
			deleteNode = deleteNode->next;
		}
	}

	return ReturnData;
}



// Removes duplicates from the list, preserving existing order of remaining items.
// The first occurrence of any duplicate (relative to the front of the list)
// is the one which remains.
// We have not yet learned about efficiency so you may implement this in any way
// as long as the resulting list satisfies the requirement above.
// PRE:   
// POST:  List contains no duplicates, front and back point to the appropriate nodes
// PARAM: 
template <class T>
void DLinkedList <T>::RemoveDuplicates()
{
	////Throw exception if list is empty
	if (IsEmpty() == true)
	{
		throw std::out_of_range("Empty List ");
	}

	Node<T> *current = front;
	Node<T> *search = current->next;
	int indexOut = 0;
	int indexIn = 1;

	//Search for same data
	while (current != NULL)
	{
		while (search != NULL)
		{
			if (search->data == current->data)
			{ 
				//Remove at Index
				search = search->prev;
				RemoveAt(indexIn);
				indexIn--;
			}

			indexIn++;
			search = search->next;
		}

		//Stoping point
		if (search == NULL && current->next == NULL)
		{
			break;
		}

		current = current->next;
		search = current->next;

		indexOut++;
		indexIn = indexOut + 1;
	}
}


//--------------------------------------------ACCESSORS------------------------------------------------   

// Returns size of list
template <class T>
int DLinkedList <T>:: Size() const
{
	 return size;
}


// Returns whether the list is empty
template <class T>
bool DLinkedList <T>:: IsEmpty() const
{
	if (Size() == 0 )
	{
		return true;
	}
	else
	{
		return false;
	}
}


// Returns existence of item
template <class T>
bool DLinkedList <T>:: Contains (T item) const
{
	if (IsEmpty() == true)
	{
		throw std::out_of_range("Empty List ");
	}

	Node<T> *node = new Node<T>(item);
	Node<T> *current = front;

	while (current != NULL)
	{
		if (current->data == node->data)
		{
			return true;
		}
		current = current->next;
	}
	return false;
}


// Returns item at index (0-indexed)
// Throws exception for invalid index
template <class T>
T DLinkedList <T>::ElementAt(int p) const
{
	//Throw exception for errors
	if (IsEmpty() == true)
	{
		throw std::out_of_range("Empty List ");
	}
	if (p >= size || p < 0)
	{
	  throw std::exception("Out of Bounce");
	}

	Node<T>* temp = front;
	int count = 0;

	while (temp != NULL)
	{
		if (count == p)
		{
			return temp->data;
		}

		count++;
		temp = temp->next;
	}
	
	return front->data;
}


//------------------------------------OVERLOADED OPERATORS-----------------------------------------

// overloaded assignment operator
// must work in the following cases:
// list2 = list1 -> general case
// list2 = list2 -> should do nothing
template <class T>
DLinkedList<T>& DLinkedList <T>::operator = (const DLinkedList& ll)
{
	//If ll is a empty list
	if (ll.IsEmpty() == true)
	{
		this->DeleteList();
		return *this;
	}
	//Delete List and copy ll into this list
	if (this != &ll)
	{
		if (this->front != NULL)
		{
			this->DeleteList();
		}

		CopyList(ll);
	}
	return *this;
}


#endif