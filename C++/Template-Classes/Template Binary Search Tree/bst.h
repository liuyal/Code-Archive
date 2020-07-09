
// File:       BST.h
// Date:        2016-02-27
// Description: Declaration of a RedBlackTree class and template Node class 

#ifndef _BST_H_
#define _BST_H_

#include <vector>
#include <stdexcept>
#include <string>
#include <stdio.h>
#include <stdlib.h>

#include <cstdlib>
#include <iostream>

using namespace std;

template <class T>
class Node
{
public:
	T data;
	Node<T>* left;
	Node<T>* right;
	Node<T>* p;     // parent pointer

	// parameterized constructor
	Node(T value)
	{
		data = value;
		left = NULL;
		right = NULL;
		p = NULL;
	}
};

template <class T>
class BST
{
private:

	Node<T>* root;
	int size;

	// Performs an in-order traversal of tree
	// PRE:
	// POST: Prints contents of tree in order
	void InOrderPrint(Node<T>* nd);

	// Performs a pre-order traversal of tree
	// PRE:
	// POST: Prints contents of tree with pre order traversal
	void PreOrderPrint(Node<T>* nd);

	// Performs an post-order traversal of tree
	// PRE:
	// POST: Prints contents of tree with post order traversal
	void PostOrderPrint(Node<T>* nd);

	// Deletes all the nodes in the tree
	// PRE:
	// POST: Deletes all nodes, de-allocating dynamic memory
	void DeleteTree(Node<T>* nd);

	Node<T>* Predecessor(Node<T>* node);

public:
	// Default Constructor
	// PRE:
	// POST: root set to NULL
	BST();

	// De-allocates dynamic memory associated with tree
	// PRE:
	// POST:
	// **NOTE: not implemented!
	~BST();

	void Insert(T item);
	bool Remove(T item);

	// Searches tree for target
	// PRE:
	// PARAM: target = value to be found
	// POST: Returns true iff target is in tree
	bool Search(T target);

	// Prints contents of tree pre, in, post order
	// PRE:
	// POST: Prints contents of tree three times:
	//       pre order, in order and post order
	void Print();


};

#include "bst.cpp"

#endif