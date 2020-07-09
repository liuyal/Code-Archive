// File:        redblacktree.h
// Date:        2016-02-27
// Description: Declaration of a RedBlackTree class and template Node class 

#ifndef _REDBLACKTREE_H_
#define _REDBLACKTREE_H_

#include <cstdlib>
#include <stdexcept>
#include <string>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

template <class T>
class Node
{
public:
	T data;
	Node<T>* left;
	Node<T>* right;
	Node<T>* p;     // parent pointer
	bool is_black;

	// parameterized constructor
	Node(T value)
	{
		data = value;
		left = NULL;
		right = NULL;
		p = NULL;
		is_black = false;
	}
};

template <class T>
class RedBlackTree
{
private:

	Node<T>* root;
	int size;

	// recursive helper function for deep copy
	// creates a new node based on sourcenode's contents, links back to parentnode,
	//   and recurses to create left and right children
	Node<T>* CopyTree(Node<T>* sourcenode, Node<T>* parentnode);

	// recursive helper function for tree deletion
	// deallocates nodes in post-order
	void RemoveAll(Node<T>* node);

	// performs BST insertion and returns pointer to inserted node
	// Note that this should only be called if item does not already exist in the tree
	// Does not increase tree size.
	Node<T>* BSTInsert(T item); //Done

	// helper function for in-order traversal
	void InOrder(const Node<T>* node, T* arr, int arrsize, int& index) const;//Done

	// rotation functions
	void LeftRotate(Node<T>* node);//Done
	void RightRotate(Node<T>* node);//Done

	// get the predecessor of a node
	Node<T>* Predecessor(Node<T>* node);//Done

	// Tree fix, performed after removal of a black node
	// Note that the parameter x may be NULL
	void RBDeleteFixUp(Node<T>* x, Node<T>* xparent, bool xisleftchild);

	// Calculates the height of the tree
	// Requires a traversal of the tree, O(n)
	int CalculateHeight(Node<T>* node) const;

public:

	// default constructor--------------------------------------------------
	RedBlackTree();

	// copy constructor, performs deep copy of parameter
	RedBlackTree(const RedBlackTree<T>& rbtree);

	// destructor
	// Must deallocate memory associated with all nodes in tree
	~RedBlackTree();

	// Mutator functions-----------------------------------------------------

	// Calls BSTInsert and then performs any necessary tree fixing.
	// If item already exists, do not insert and return false.
	// Otherwise, insert, increment size, and return true.
	bool Insert(T item);

	// Removal of an item from the tree.
	// Must deallocate deleted node after RBDeleteFixUp returns
	bool Remove(T item);

	// deletes all nodes in the tree. Calls recursive helper function.
	void RemoveAll();

	// Accessor functions------------------------------------------------------

	// Returns existence of item in the tree.
	// Return true if found, false otherwise.
	bool Search(T item) const;//Done

	// Searches for item and returns a pointer to the node contents so the
	//   value may be accessed or modified
	// Use with caution! Do not modify the item's key value such that the
	//   red-black / BST properties are violated.
	T* Retrieve(T item);//Done

	// performs an in-order traversal of the tree
	// arrsize is the size of the returned array (equal to tree size attribute)
	T* Dump(int& arrsize) const;//Done

	// returns the number of items in the tree
	int Size() const;

	// returns the height of the tree, from root to deepest null child. Calls recursive helper function.
	// Note that an empty tree should have a height of 0, and a tree with only one node will have a height of 1.
	int Height() const;

	// returns a pointer to the root of the tree
	// NOTE: This will be used only for grading.
	// Providing access to the tree internals is dangerous in practice!
	Node<T>* GetRoot() const
	{
		return this->root;
	}

	// overloaded assignment operator
	RedBlackTree<T>& operator=(const RedBlackTree<T>& rbtree);


	/////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////

	//Verify Helper Functions
	//Put into Array
	void PreOrder(const Node<T>* node, T* arr, int arrsize, int& index) const
	{
		if (node != NULL)
		{
			cout << node->data << " ";
			arr[index] = node->data;
			index++;
			PreOrder(node->left, arr, arrsize, index);
			PreOrder(node->right, arr, arrsize, index);
		}
	}

	void InOrderB(const Node<T>* node, T* arr, int arrsize, int& index) const
	{
		if (node != NULL)
		{
			InOrderB(node->left, arr, arrsize, index);
			cout << node->data << " ";
			arr[index] = node->data;
			index++;
			InOrderB(node->right, arr, arrsize, index);
		}
	}

	void PostOrder(const Node<T>* node, T* arr, int arrsize, int& index) const
	{
		if (node != NULL)
		{
			PostOrder(node->left, arr, arrsize, index);
			PostOrder(node->right, arr, arrsize, index);
			cout << node->data << " ";
			arr[index] = node->data;
			index++;
		}
	}

	// Verifying Properties of Red black Tree
	void verify(const RedBlackTree<T>& tree)
	{
		Node<int> *R = tree.GetRoot();
		if (R == NULL || size == 0) { cout << "Empty Tree.." << endl; return; }

		bool CheckH = false;
		bool V1 = Verify1(R);
		bool V2 = Verify2(R);
		int V3 = Verify3(R);

		if (V3 >= 2) { CheckH = true; }

		cout << "Root is Black: ";
		if (V1 == true) { cout << "[YES!]" << endl; }
		else { cout << "[NO!]" << endl; }

		cout << "Every Red Has 2 Black Children: ";
		if (V2 == true) { cout << "[YES!]" << endl; }
		else { cout << "[NO!]" << endl; }

		cout << "Balanced Black Height: ";
		if (CheckH == true) { cout << "[YES!]" << endl; }
		else { cout << "[NO!]" << endl; }

		cout << "Size: " << tree.Size() << endl;
		cout << "Height: " << tree.Height() << endl;
		T* T1 = new T[tree.Size()]; T* T2 = new T[tree.Size()];T* T3 = new T[tree.Size()];
		int i11 = 0; int i12 = 0; int i13 = 0;
		cout << "PreOrder: ";tree.PreOrder(R, T1, tree.Size(), i11);cout << endl;
		cout << "InOrder: ";tree.InOrderB(R, T2, tree.Size(), i12);cout << endl;
		cout << "PostOrder: ";tree.PostOrder(R, T3, tree.Size(), i13);cout << endl << endl;

		delete[] T1;
		delete[] T2;
		delete[] T3;
	}

	// Verifying Property 1: Root is Black
	bool Verify1(Node<T>* node)
	{
		if (root == NULL || root->is_black == true) { return true; }
		else { return false; }
	}

	// Verifying Property 2: Every Red Node Has Left,Right,p as Black nodes
	bool Verify2(Node<T>* node)
	{
		if (node == NULL) { return true; }
		bool L, R = true;

		L = Verify2(node->left); if (L == false) { return false; }
		R = Verify2(node->right); if (R == false) { return false; }

		if (node->is_black == false && node->p != NULL)
		{
			if ((node->left != NULL && node->left->is_black == false) || (node->right != NULL && node->right->is_black == false) || (node->p->is_black == false))
			{
				return false;
			}
			else
			{
				return true;
			}
		}

		if (L == true && R == true) { return true; }
		else { return false; }
	}

	int is_red(Node<T> *node)
	{
		return node != NULL && node->is_black == false;
	}

	//Balanced Red Black
	int Verify3(Node<T> *node)
	{
		int lh, rh = 0;

		if (node == NULL) { return 2; }

		else
		{
			Node<T> *ln = node->left;
			Node<T> *rn = node->right;

			lh = Verify3(ln);
			rh = Verify3(rn);

			/* Invalid binary search tree */
			if ((ln != NULL && ln->data >= node->data) || (rn != NULL && rn->data <= node->data)) { return 0; }

			/* Black height mismatch */
			if (lh != 0 && rh != 0 && lh != rh) { return 0; }

			/* Only count black links */
			if (lh != 0 && rh != 0) { return is_red(node) ? lh : lh + 1; }

			else { return 0; }
		}


	}

	//Creat BST for Compare
	bool BSTInsert2(T item)
	{
		if (Search(item) == true)
		{
			return false;
		}

		Node<T>*node;
		node = BSTInsert(item);

		this->root->is_black = true;
		this->size++;

		if (this->size > 3)
		{
			this->root->right->is_black = true;

		}

		return true;
	}

	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////

};

#include "rbtreepartial.cpp"

#include "redblacktree.cpp"

#endif