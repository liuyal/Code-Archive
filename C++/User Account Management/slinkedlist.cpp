// File:        slinkedlist.cpp
// Date:        March 26, 2016
// Description: Implementation of a template singly-linked-list class

#ifdef _SLINKEDLIST_H_

#include <cstdlib>
#include <string>
#include <vector>

//------------------------------------HELPER FUNCTIONS-----------------------------------------

// helper function for deep copy
// Used by copy constructor and operator=
template <class T>
void SLinkedList <T> ::CopyList(const SLinkedList& ll)
{
	//Check for Empty list
	if (ll.IsEmpty() == true)
	{
		this->size = 0;
		this->front = this->back = NULL;
		return;
	}
	//Initialize variables and temp is assigned to front of list
	Node<T>* Temp = ll.front;
	this->size = 0;

	//Insert nodes of ll into this->list with loop
	while (Temp != NULL)
	{
		this->InsertBack(Temp->data);
		Temp = Temp->next;
	}
}

// helper function for deep delete
// Used by destructor and copy/assignment
template <class T>
void SLinkedList <T>::DeleteList()
{
	RemoveAll();
}

//--------------------------------------------Constructors-------------------------------------------------   

// default constructor
//Initialize Template Class of Link List
template <class T>
SLinkedList<T>::SLinkedList()
{
	size = 0;
	front = NULL;
	back = NULL;
}

// copy constructor, performs deep copy of list elements
template <class T>
SLinkedList<T>::SLinkedList(const SLinkedList& ll)
{
	//Use helper function
	CopyList(ll);
}

// destructor
template <class T>
SLinkedList <T>::~SLinkedList()
{
	//Use helper function
	if (this->size != 0) {DeleteList();}
}

//------------------------------------------------MUTATORS---------------------------------------------   

// Inserts an item at the front of the list
// POST:  List contains item at front
// PARAM: item = item to be inserted
template <class T>
void SLinkedList <T>::InsertFront(T item)
{
	Node<T> *NewNode = new Node<T>(item);
	NewNode->data = item;
	NewNode->next = front;

	front = NewNode;
	this->size++;
}

// Inserts an item at the back of the list
// POST:  List contains item at back
// PARAM: item = item to be inserted
template <class T>
void SLinkedList <T>::InsertBack(T item)
{
	Node<T> *NewNode = new Node<T>(item);
	NewNode->data = item;
	NewNode->next = NULL;

	if (front == NULL)
	{
		front = back = NewNode;
	}
	else 
	{
		Node<T> *temp = front;

		while (temp->next != NULL) { temp = temp->next; }
		temp->next = NewNode;
		back = NewNode;

	}

	this->size++;
}

// Removes the first occurrence of the supplied parameter
// Removes and returns true if found, otherwise returns false if parameter is not found or list is empty
template <class T>
bool SLinkedList <T>::Remove(T item)
{
	if (this->size == 0){return false;}

	Node<T> *Temp = front;

	if (front->data == item)
	{
		Temp = front;
		front = Temp->next;
		delete Temp;
		this->size--;
		return true;
	}

	Node<T> *current = front;

	while (current != NULL)
	{
		if (current->next != NULL && current->next->data == item)
		{
			if (current->next == back) { back = current; }

			Temp = current->next;
			current->next = current->next->next;

			delete Temp;
			this->size--;
			return true;
		}
		current = current->next;
	}
	return false;
}

// Removes all items in the list
template <class T>
void SLinkedList <T>::RemoveAll()
{
	if (this->size == 0) { front = back = NULL;  return; }

	Node<T>* Temp = front;

	while (Temp != NULL)
	{
		Temp = front->next;
		delete front;
		front = Temp;
	}

	front = back = NULL;
	this->size = 0;
}

//--------------------------------------------ACCESSORS------------------------------------------------   

// Returns size of list
template <class T>
int SLinkedList <T>::Size() const
{
	return this->size;
}

// Returns whether the list is empty
template <class T>
bool SLinkedList <T>::IsEmpty() const
{
	if (this->size == 0) { return true; }
	else { return false; }
}

// Returns existence of item
template <class T>
bool SLinkedList <T>::Contains(T item) const
{
	if (IsEmpty() == true){return false;}

	Node<T> *node = front;

	while (node != NULL)
	{
		if (node->data == item)
		{ 
			return true;
		}
		node = node->next;
	}

	return false;
}

// Returns a pointer to the in-place list item or NULL if item not found
template <class T>
T* SLinkedList <T>::Retrieve(T item)
{
	T* value = NULL;

	Node<T> *node = front;

	while (node != NULL)
	{
		if (node->data == item)
		{
			value = &(node->data);
			break;
		}
		node = node->next;
	}

	return value;
}

// Returns a vector containing the list contents using push_back
template <class T>
vector<T> SLinkedList <T>::Dump() const
{
	vector<T> Stuff;

	Node<T> *node = front;

	while (node != NULL)
	{
		Stuff.push_back(node->data);
	
		node = node->next;
	}

	return Stuff;
}

//------------------------------------OVERLOADED OPERATORS-----------------------------------------

// overloaded assignment operator
// must work in the following cases:
// list2 = list1 -> general case
// list2 = list2 -> should do nothing
template <class T>
SLinkedList<T>& SLinkedList <T>::operator = (const SLinkedList& ll)
{
	if (ll.IsEmpty() == true)
	{
		this->DeleteList();
	}

	if (this != &ll)
	{
		if (this->size != 0)
		{
			this->DeleteList();
		}

		CopyList(ll);
	}

	return *this;
}

#endif