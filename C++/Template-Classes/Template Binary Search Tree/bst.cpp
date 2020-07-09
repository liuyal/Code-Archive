
// File:        bst.cpp
// Date:        2016-02-27
// Description: Implementation of a RedBlackTree class and template Node class 

#ifdef _BST_H_

#include <vector>
#include <stdexcept>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>
#include <iostream>

// Performs an in-order traversal of tree
// PRE:
// POST: Prints contents of tree in order
template <class T>
void BST<T>::InOrderPrint(Node<T>* nd)
{
	if (nd != NULL)
	{
		InOrderPrint(nd->left);
		cout << nd->data << " ";
		InOrderPrint(nd->right);
	}
}

// Performs a pre-order traversal of tree
// PRE:
// POST: Prints contents of tree with pre order traversal
template <class T>
void BST<T>::PreOrderPrint(Node<T>* nd)
{
	if (nd != NULL)
	{
		cout << nd->data << " ";
		PreOrderPrint(nd->left);
		PreOrderPrint(nd->right);
	}
}

// Performs an post-order traversal of tree
// PRE:
// POST: Prints contents of tree with post order traversal
template <class T>
void BST<T>::PostOrderPrint(Node<T>* nd)
{
	if (nd != NULL)
	{
		PostOrderPrint(nd->left);
		PostOrderPrint(nd->right);
		cout << nd->data << " ";
	}
}

// Deletes all the nodes in the tree
// PRE:
// POST: Deletes all nodes, de-allocating dynamic memory
template <class T>
void BST<T>::DeleteTree(Node<T>* nd)
{
	if (nd != NULL)
	{
		DeleteTree(nd->left);
		DeleteTree(nd->right);
		delete nd;
	}
}

// get the predecessor of a node
template <class T>
Node<T>* BST<T>::Predecessor(Node<T>* node)
{
	Node<T>* pre = NULL;
	// do not allow operation on a null node
	if (node != NULL)
	{
		// case: node has no left child
		if (node->left == NULL)
			pre = NULL;
		else
		{
			// go left once, then follow right pointers until no more right pointers found
			pre = node->left;
			while (pre->right != NULL)
			{
				pre = pre->right;
			}
			//while loop exited, pre contains the predecessor or NULL
		}
	}
	return pre;
}

// -----------------------------------------------------------------------------

// Default Constructor
// PRE:
// POST: root set to NULL
template <class T>
BST<T>::BST()
{
	size = 0;
	root = NULL;
}

// De-allocates dynamic memory associated with tree
// PRE:
// POST:
template <class T>
BST<T>::~BST()
{
	DeleteTree(root);
}

// Insert value in tree maintaining bst property
// PRE:
// PARAM: value = value to be inserted
// POST: Value is inserted, in order, in tree
template <class T>
void BST<T>::Insert(T item)
{
	Node<T>* refnode; // will be pointer to parent of inserted node
	Node<T>* newnode; // will be pointer to inserted node
					  // special case: empty tree
	if (size <= 0)
	{
		root = new Node<T>(item);
		newnode = root;
	}
	else // general case: non-empty tree
	{
		refnode = root;
		// find the insertion location
		while ((item < refnode->data && refnode->left != NULL) || (item > refnode->data && refnode->right != NULL))
		{
			if (item < refnode->data)
				refnode = refnode->left;
			else if (item > refnode->data)
				refnode = refnode->right;
		}
		// exited while loop, refnode points to the parent of the insertion location and has a null location to insert
		newnode = new Node<T>(item);
		newnode->p = refnode;
		if (item < refnode->data)
			refnode->left = newnode;
		else
			refnode->right = newnode;
	}
	this->size++;
}


template <class T>
bool BST<T>::Remove(T item)
{
	if (this->size <= 0 || Search(item) == false) { return false; }

	Node<T>* node = root;

	while (node != NULL)
	{
		if (item == node->data) { break; }
		else if (item < node->data) { node = node->left; }
		else { node = node->right; }
	}

	if (this->size == 1) { delete root; root = NULL; this->size--; return true; }
	else if (this->size == 2) 
	{
		if (node == root)
		{
			if (root->left != NULL)
			{
				root->data = root->left->data;
				delete root->left;
				return true;
			}
			else if (root->right != NULL)
			{
				root->data = root->right->data;
				delete root->right;
				return true;
			}
		}

		delete node;
		node = NULL;
		root->left = NULL;
		root->right = NULL;
		this->size--;
		return true;
	}

	Node<T>* pred = Predecessor(node);

	node->data = pred->data;

	if (pred->p->right == pred) { pred->p->right = NULL; }
	else if (pred->p->left == pred) { pred->p->left = NULL; }

	delete pred;
	this->size--;
	return true;
}

// Searches tree for target
// PRE:
// PARAM: target = value to be found
// POST: Returns true iff target is in tree
template <class T>
bool BST<T>::Search(T target)
{
	if (this->size <= 0) { return false; }

	Node<T>* nd = root;
	while (nd != NULL)
	{
		if (target == nd->data) { return true; }
		else if (target < nd->data) { nd = nd->left; }
		else { nd = nd->right; }
	}
	return false;
}

// Prints contents of tree pre, in, post order
// PRE:
// POST: Prints contents of tree three times:
//       pre order, in order and post order
template <class T>
void BST<T>::Print()
{
	cout << "Pre Order" << endl;
	PreOrderPrint(root);
	cout << endl << "In Order" << endl;
	InOrderPrint(root);
	cout << endl << "Post Order" << endl;
	PostOrderPrint(root);
}



#endif