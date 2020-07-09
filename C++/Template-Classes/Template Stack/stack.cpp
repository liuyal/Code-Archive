
#ifdef  STACK_H

// Title:		stack.cpp
// Author:      Ya Qi Liu
// Date:        January 18, 2016

#include <iostream>
#include <stdexcept>

//------------------------------------HELPER FUNCTIONS-----------------------------------------

// helper function for deep copy
// Used by copy constructor and operator=
template <class T>
void Stack<T> ::CopyStack(const Stack& stack)
{
	if (stack.Empty() == true)
	{
		this->size = 0;
		return;
	}
	//Initialize variables and temp is assigned to front of list
	Stack<T> *TempStack = new Stack;

	Node<T>* temp = stack.top;
	this->size = 0;
	this->top = temp;

	//Insert nodes of stack into TempStack
	//Note TempStack is Reversed
	while (temp != NULL)
	{
		TempStack->Push(temp->data);
		temp = temp->next;
	}

	Node<T>* temp2 = TempStack->top;

	//Insert From TempStack Into this
	while (temp2 != NULL)
	{
		this->Push(temp2->data);
		temp2 = temp2->next;
	}

	TempStack->DeleteStack();
}

/*--------------------------------------------------------*/
// helper function for deep delete
// Used by destructor and copy/assignment
template <class T>
void Stack<T>::DeleteStack()
{
	if (Empty())
	{
		this->size = 0;
		return;
	}

	//Traves through stack and remove nodes
	Node<T>* temp = top;
	while (temp != NULL)
	{
		temp = top->next;
		delete top;
		top = temp;
	}
	//Set size to 0 and pointers to NULL
	size = 0;
	top = NULL;
}

/*--------------------------------------------------------*/
template <class T>
T Stack<T>::ElementAt(int n) const
{
	if (Empty())
	{
		throw std::logic_error("Out of Range");
	}
	if (n >= size || n < 0)
	{
		throw std::logic_error("Out of Range");
	}

	Node<T>* temp = top;
	int count = 0;

	while (temp != NULL)
	{
		if (count == n)
		{
			return temp->data;
		}
		count++;
		temp = temp->next;
	}

	return top->data;
}


/*--------------------------------------------Constructors------------------------------------------------- */

//Default Constructor used to create an empty Stack object.
template <class T>
Stack<T>::Stack()
{
	top = NULL;
	size = 0;
}

/*--------------------------------------------------------*/

// helper function for deep copy
// Used by copy constructor and operator=
template <class T>
Stack<T>::Stack(const Stack& stack)
{
	CopyStack(stack);

}

/*--------------------------------------------------------*/

//Destructor for Stack objects.
template <class T>
Stack<T>::~Stack()
{
	DeleteStack();
}

/*---------------------------------------------MUTATORS-------------------------------------------*/

//PreCondition: Start with a Stack object.
//PostCondition: Add the string in a new frame at the top of the Stack.
template <class T>
void Stack<T>::Push(T item) 
{
	Node<T> *NewNode = new Node<T>(item);
	NewNode->data = item;

	if (Empty())
	{
		top = NewNode;
		NewNode->next = NULL;
		this->size++;
		return;
	}
	else
	{
		NewNode->next = top;
		top = NewNode;
		this->size++;
		return;
	}
}

/*--------------------------------------------------------*/

//PreCondition: Start with Stack object.
//PostCondition: Remove the top Stack Frame and return the string stored at the top.
//               of the Stack.
template <class T>
T Stack<T>::Pop()
{
	if (!Empty())
	{
		Node<T> *TopNode = top;
		top = top->next;
		T data = TopNode->data;
		
		this->size--;
		delete TopNode;
		return data;
	}

	throw std::logic_error("Out of Range");
}


//--------------------------------------------ACCESSORS------------------------------------------------   

template <class T>
T Stack<T>::Peek() const
{
	return this->top->data;
}

/*--------------------------------------------------------*/

//Checks to see if the Stack is empty.  Returns true if empty, else returns false.
//Stack remains unchanged after function call.
template <class T>
bool Stack<T>::Empty()  const
{
	return Size() == 0;
}

/*--------------------------------------------------------*/

template <class T>
int Stack<T>::Size()  const
{
	return size;
}


template <class T>
void Stack<T>::Print() const
{
	cout  << "Print Stack:" << endl;
	for (int i = 0;i < this->Size();i++)
	{
		cout << i << " | " << this->ElementAt(i) << endl;
	}
	cout << endl;
}

//--------------------------------------------operator = ------------------------------------------------   
template <class T>
Stack<T>& Stack <T>::operator = (const Stack& stack)
{
	if (stack.Empty() == true)
	{
		this->DeleteStack();
		return *this;
	}

	if (this != &stack)
	{
		if (this->top != NULL)
		{
			this->DeleteStack();
		}

		CopyStack(stack);
	}
	return *this;
}


#endif