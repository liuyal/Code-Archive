#ifndef STACK_H
#define STACK_H

// Title: stack.h
//
//**************************************************************************************
//
//Objective: To create the basic member functions to be able to create
//and manipulate a stack.


#include <iostream>

using namespace std;

template <class T>
class Node
{
public:
	T data;
	//string data;
	Node<T>* next;

	// default constructor
	template <class T>
	Node(T value)
	{
		data = value;
		next = NULL;
	}
};

//A Stack with a pointer to the top of the stack.  All insertions and removals happen 
//at the top of the stack.
template <class T>
class Stack
{
private:

	Node<T>* top; // Points to the top of the stack
	int size; // number of items stored
	void CopyStack(const Stack& stack);
	void DeleteStack();
	T ElementAt(int n) const;

public:
	
	Stack();
	//Default Constructor used to create an empty Stack object.

	Stack(const Stack& stack);
	// copy constructor, performs deep copy of list elements

	~Stack();
	//Destructor for Stack objects.

	void Push(T item); 
	//PreCondition: Start with a Stack object.
	//PostCondition: Add the item in a new frame at the top of the Stack.

	T Pop();
	//PreCondition: Start with Stack object.
	//PostCondition: Remove the top Stack Frame and return the item stored at the top.

	T Peek() const;

	bool Empty() const;
	//Checks to see if the Stack is empty.  Returns true if empty, else returns false.
	//Stack remains unchanged after function call.

	int Size() const;

	void Print() const;

	Stack& operator=(const Stack& stack);
};

#include "stack.cpp"

#endif