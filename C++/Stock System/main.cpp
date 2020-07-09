// File:        main.cpp
// Date:        2016-02-27
// Description: Test driver for RedBlackTree and StockSystem classes
//              Only basic cases for RedBlackTree are tested. You are responsible
//              for adding your own code to thoroughly test your RedBlackTree class.
//              See PDF specification for tips for testing your tree structure using
//              pre-order traversal.
//https://www.cs.usfca.edu/~galles/visualization/RedBlack.html
//http://tommikaikkonen.github.io/rbtree/
//http://www.eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx

#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#include <string.h>
#include "time.h"

#include <iostream>
#include <cstdlib>
#include <string>

#include "redblacktree.h"
#include "stocksystem.h"

using namespace std;

// forward declarations
void PrintMenu();
void RBTreeTest();
void ConstructorTest();
void CopyTest();
void InsertTestA();
void InsertTestB();
void RemoveTest();
void RemoveTest2();
void HeightTest();
void AssignmentTest();
void DestructorTest();
void StockSystemTest();

void MTest();

// program entry point
int main()
{  
	_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_WARN, _CRTDBG_FILE_STDOUT);
	_CrtSetReportMode(_CRT_ERROR, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_ERROR, _CRTDBG_FILE_STDOUT);
	_CrtSetReportMode(_CRT_ASSERT, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_ASSERT, _CRTDBG_FILE_STDOUT);
	
	DestructorTest();

	ConstructorTest();

	CopyTest();

	InsertTestA();

	InsertTestB();

	RemoveTest();

	system("pause");

	RemoveTest2();

	HeightTest();

	AssignmentTest();

	RBTreeTest();

	cout << "--------------------------_CrtDumpMemoryLeaks---------------------------" << endl;
	_CrtDumpMemoryLeaks();
	system("pause");

	StockSystemTest();

	system("pause");
	cout << endl << endl;

	MTest();

	return 0;
}

void PrintMenu()
{
	cout << "****************************************************\n"
		<< "* Please select an option:                         *\n"
		<< "* 1. Print balance             6. Restock an item  *\n"
		<< "* 2. Print catalogue           7. Sell an item     *\n"
		<< "* 3. Add a new SKU                                 *\n"
		<< "* 4. Edit item description                         *\n"
		<< "* 5. Edit item price           8. Quit             *\n"
		<< "****************************************************\n" << endl;
	cout << "Enter your choice: ";
}

void RBTreeTest()
{
	cout << "--------------------------RBTreeTest---------------------------" << endl;

	RedBlackTree<int> tree1;

	tree1.Insert(1);
	tree1.Insert(3);
	tree1.Insert(2); // should cause 2 rotations to occur
	tree1.Insert(4);
	tree1.Remove(4);

	cout << "Tree contains " << tree1.Size() << " entries." << endl;
	cout << "Tree height: " << tree1.Height() << endl;

	RedBlackTree<int> tree2(tree1);

	tree1.RemoveAll();

	RedBlackTree<int> tree3;
	tree3.Insert(5);
	tree3 = tree2;

	cout << "End of Tree Test" << endl;
	cout << endl;
	cout << endl;
}

void DestructorTest()
{
	cout << "--------------------------DestructorTest---------------------------" << endl;

	RedBlackTree<int> tree;
	cout << "Create Tree..." << endl;
	tree.Insert(6);
	tree.Insert(7);
	tree.Insert(8);
	tree.Insert(9);
	cout << "Remove All of Tree..." << endl << endl;
	tree.RemoveAll();

	RedBlackTree<int> tree2;
	cout << "Create Tree2..." << endl << endl;
	tree2.Insert(0);
	tree2.Insert(1);
	tree2.Insert(2);
	tree2.Insert(3);

	RedBlackTree<int> tree3(tree2);
	cout << "Create Tree3 (Copy of Tree2)..." << endl;
	cout << "Insert into Tree3..." << endl << endl;
	tree3.Insert(10);
	tree3.Insert(55);
	tree3.Insert(96);
	tree3.Insert(777);

	cout << "Destory Empty Tree1..." << endl;
	cout << "Destory Tree2..." << endl;
	cout << "Destory Copy Tree3..." << endl << endl;
}

void ConstructorTest()
{
	cout << "--------------------------Constructor Test---------------------------" << endl;

	RedBlackTree<int> tree;
	cout << "Create Tree..." << endl;
	tree.Insert(6);
	tree.Insert(7);
	tree.Insert(8);
	tree.Insert(9);
	tree.Insert(11);
	tree.Insert(2);
	tree.Insert(1);
	tree.Insert(3);
	tree.Insert(4);
	tree.Insert(5);

	cout << endl << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	RedBlackTree<int> treeC(tree);
	cout << "Perform Copy Tree..." << endl;
	cout << "Size of Copy: " << treeC.Size() << endl;

	//Verify order of Tree
	cout << endl << "Verify Copy Red Black Tree..." << endl;
	treeC.verify(treeC);

	cout << "Copy Blank Tree..." << endl;
	RedBlackTree<int> treeA;
	cout << "Size of Empty tree1: " << treeA.Size() << endl;
	RedBlackTree<int> treeC2(treeA);
	cout << "Size of Copy of tree1: " << treeC2.Size() << endl;

	//BST NOT RED BLACK (FOR COMPARE)!!!
	RedBlackTree<int> BST;
	BST.BSTInsert2(6);BST.BSTInsert2(7);
	BST.BSTInsert2(8);BST.BSTInsert2(9);
	BST.BSTInsert2(11);BST.BSTInsert2(2);
	BST.BSTInsert2(1);BST.BSTInsert2(3);
	BST.BSTInsert2(4);BST.BSTInsert2(5);
	cout << endl << "BST Verify..." << endl << "**NOT RED BLACK TREE**" << endl << endl;
	BST.verify(BST);

	cout << endl;
}

void CopyTest()
{
	cout << "--------------------------CopyTest---------------------------" << endl;

	RedBlackTree<int> tree;
	cout << "Create Tree..." << endl;
	tree.Insert(6);
	tree.Insert(77);
	tree.Insert(1);
	tree.Insert(9);
	tree.Insert(11);
	tree.Insert(5);

	cout << endl << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	cout << "Size: " << tree.Size() << endl;
	RedBlackTree<int> treeC(tree);
	cout << "Perform Copy Tree..." << endl;
	cout << "Size of Copy: " << treeC.Size() << endl;

	cout << endl << "Verify Copy Red Black Tree..." << endl;
	treeC.verify(treeC);

	cout << "Remove 2 Elements of Copy" << endl; 
	treeC.Remove(5);
	treeC.Remove(1);
	cout << "Size of Copy: " << treeC.Size() << endl;

	//Verify order of Tree
	cout << endl << "Verify Copy Red Black Tree..." << endl;
	treeC.verify(treeC);

	cout << endl;
}

void InsertTestA()
{
	cout << "--------------------------Insert TestA---------------------------" << endl;

	cout << "Basic Size of Three" << endl;

	cout << endl << "Insert 5 4 3" << endl;
	RedBlackTree<int> tree1;
	tree1.Insert(5);
	tree1.Insert(4);
	tree1.Insert(3);
	Node<int>*R1 = tree1.GetRoot();
	cout << "Root is black: ";
	if (R1->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R1->left->data < R1->data && R1->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R1->right->data > R1->data && R1->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree1.Size() << endl;


	cout << endl << "Insert 6 4 5" << endl;
	RedBlackTree<int> tree2;
	tree2.Insert(6);
	tree2.Insert(4);
	tree2.Insert(5);
	Node<int>*R2 = tree2.GetRoot();
	cout << "Root is black: ";
	if (R2->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R2->left->data < R2->data && R2->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R2->right->data > R2->data && R2->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree2.Size() << endl;

	cout << endl << "Insert 1 2 3" << endl;
	RedBlackTree<int> tree3;
	tree3.Insert(1);
	tree3.Insert(2);
	tree3.Insert(3);
	Node<int>*R3 = tree3.GetRoot();
	cout << "Root is black: ";
	if (R3->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R3->left->data < R3->data && R3->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R3->right->data > R3->data && R3->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree3.Size() << endl;

	cout << endl << "Insert 1 3 2" << endl;
	RedBlackTree<int> tree4;
	tree4.Insert(1);
	tree4.Insert(3);
	tree4.Insert(2);
	Node<int>*R4 = tree4.GetRoot();
	cout << "Root is black: ";
	if (R4->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R4->left->data < R4->data && R4->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R4->right->data > R4->data && R4->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree4.Size() << endl;

	cout << endl << "Insert 5 4 6" << endl;
	RedBlackTree<int> tree5;
	tree5.Insert(5);
	tree5.Insert(4);
	tree5.Insert(6);
	Node<int>*R5 = tree5.GetRoot();
	cout << "Root is black: ";
	if (R5->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R5->left->data < R5->data && R5->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R5->right->data > R5->data && R5->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree5.Size() << endl;

	cout << endl << "Insert 5 6 4" << endl;
	RedBlackTree<int> tree6;
	tree6.Insert(5);
	tree6.Insert(6);
	tree6.Insert(4);
	Node<int>*R6 = tree6.GetRoot();
	cout << "Root is black: ";
	if (R6->is_black == true) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Left (Smaller and Red): ";
	if (R6->left->data < R6->data && R6->left->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Check Right (Larger and Red): ";
	if (R6->right->data > R6->data && R6->right->is_black == false) { cout << "[YES!]" << endl; }
	else { cout << "[NO!]" << endl; }
	cout << "Size: " << tree6.Size() << endl;

	cout << endl << endl;
}

void InsertTestB()
{
	cout << "--------------------------Insert TestB---------------------------" << endl;

	RedBlackTree<int> tree;
	tree.Insert(20);
	tree.Insert(3);
	tree.Insert(7);
	tree.Insert(5);
	tree.Insert(6);
	tree.Insert(10);
	tree.Insert(21);
	tree.Insert(23);
	cout << "New Tree..." << endl;
	cout << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	RedBlackTree<int> treeC(tree);
	cout <<  "Copy And Insert..." << endl;
	treeC.Insert(55);
	treeC.Insert(9);
	treeC.Insert(11);
	treeC.Insert(777);
	cout << "Verify Copy and Inserted Red Black Tree..." << endl;
	treeC.verify(treeC);

	cout << endl;
}

void RemoveTest()
{
	cout << "--------------------------RemoveTest---------------------------" << endl;

	cout << endl << "Insert Tree..." << endl;
	RedBlackTree<int> tree1;
	tree1.Insert(47);
	tree1.Insert(32);
	tree1.Insert(71);
	tree1.Insert(65);
	tree1.Insert(87);
	tree1.Insert(82);
	tree1.Insert(93);
	cout << endl << "Verify1 Red Black Tree..." << endl;
	tree1.verify(tree1);
	cout << "Remove 2 elements(87 65)..." << endl;
	tree1.Remove(87);
	tree1.Remove(65);
	cout << endl << "Verify2 Red Black Tree..." << endl;
	tree1.verify(tree1);
	cout << "Remove All Tree..." << endl;
	tree1.RemoveAll();
	cout << "Tree Size: " << tree1.Size() << endl << endl;

	cout << "Insert Elements into Tree2..." << endl;
	RedBlackTree<int> tree2;
	tree2.Insert(5);
	tree2.Insert(6);
	tree2.Insert(3);
	tree2.Insert(1);
	tree2.Insert(8);
	tree2.Insert(23);
	tree2.Insert(11);
	tree2.Insert(24);
	tree2.Insert(10);
	tree2.Insert(4);
	tree2.Insert(2);
	tree2.Insert(25);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);

	cout << "Remove 5 Elements (6 24 11 3 8)..." << endl;
	tree2.Remove(6);
	tree2.Remove(24);
	tree2.Remove(11);
	tree2.Remove(3);
	tree2.Remove(8);

	cout << endl << "Verify2 Red Black Tree2..." << endl;
	tree2.verify(tree2);

	cout << "Insert 3 Elements into Tree3..." << endl;
	RedBlackTree<int> tree3;
	tree3.Insert(5);
	tree3.Insert(6);
	tree3.Insert(3);
	cout << endl << "Verify Red Black Tree3..." << endl;
	tree3.verify(tree3);

	cout << "Remove 3 Elements (5 6 3)..." << endl;
	//tree3.Remove(5);
	tree3.Remove(3);
	tree3.Remove(6);

	cout << endl << "Verify Red Black Tree3..." << endl;
	tree3.verify(tree3);

	cout << "RemoveAll() For Tree3..." << endl;
	tree3.RemoveAll();

	cout << endl << "Insert 3 Elements into Tree4..." << endl;
	RedBlackTree<int> tree4;
	tree4.Insert(4);
	tree4.Insert(6);
	tree4.Insert(3);

	cout << endl << "Verify Red Black Tree4..." << endl;
	tree4.verify(tree4);
	tree4.Remove(4);
	tree4.Remove(3);
	tree4.Remove(6);

	cout << "Verify Red Black Tree4..." << endl;
	tree4.verify(tree4);

	cout << "RemoveAll() For Empty Tree4..." << endl;
	tree4.RemoveAll();

	cout << endl;
}

void RemoveTest2()
{
	cout << "--------------------------RemoveTest2---------------------------" << endl;

	RedBlackTree<int> tree;
	tree.Insert(20);
	tree.Insert(3);
	tree.Insert(7);
	tree.Insert(5);
	tree.Insert(6);
	tree.Insert(10);
	tree.Insert(21);
	tree.Insert(23);
	cout << endl << "New Tree..." << endl;
	cout << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	cout << "Remove Root..." << endl;
	tree.Remove(7);
	cout << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	cout << "New Tree2..." << endl;

	RedBlackTree<int> tree2;
	tree2.Insert(5);
	tree2.Insert(6);
	tree2.Insert(3);
	tree2.Insert(1);
	tree2.Insert(8);
	tree2.Insert(23);
	tree2.Insert(11);
	tree2.Insert(24);
	tree2.Insert(10);
	tree2.Insert(4);
	tree2.Insert(2);
	tree2.Insert(25);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);

	cout << "Remove 5 Elements (6 24 11 3 8)..." << endl;
	tree2.Remove(6);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);
	tree2.Remove(24);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);
	tree2.Remove(11);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);
	tree2.Remove(3);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);
	tree2.Remove(8);
	cout << endl << "Verify Red Black Tree2..." << endl;
	tree2.verify(tree2);


	cout << "Create Tree3..." << endl;
	RedBlackTree<int> tree3;
	tree3.Insert(5);
	tree3.Insert(6);
	tree3.Insert(3);
	tree3.Insert(1);
	tree3.Insert(8);
	tree3.Insert(23);
	tree3.Insert(11);
	tree3.Insert(24);
	tree3.Insert(10);
	tree3.Insert(4);
	tree3.Insert(2);
	tree3.Insert(25);

	tree3.Remove(6);
	tree3.Remove(24);
	tree3.Remove(11);
	tree3.Remove(3);

	tree3.Insert(6);

	cout  << "Verify Red Black Tree3..." << endl;
	tree3.verify(tree3);

	cout << "Remove Root..." << endl;
	tree3.Remove(8);

	cout  << "Verify Red Black Tree3..." << endl;
	tree3.verify(tree3);

	cout << endl;
}

void HeightTest()
{
	cout << "--------------------------Height Test---------------------------" << endl;

	RedBlackTree<int> tree;
	cout<< "Creat Tree..." << endl;
	cout << "Height: " << tree.Height() << endl;
	cout << "Insert 1" << endl;
	tree.Insert(1);
	cout << "Height: " << tree.Height() << endl <<endl ;
	cout << "Insert 5 Item" << endl;
	tree.Insert(20);
	tree.Insert(3);
	tree.Insert(7);
	tree.Insert(5);
	tree.Insert(6);
	tree.Insert(10);
	tree.Insert(21);
	tree.Insert(23);
	cout << "Height: " << tree.Height() << endl;

	cout << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	cout << "Remove 1" << endl;
	tree.Remove(1);
	cout << "Height: " << tree.Height() << endl <<endl ;

	cout << "Remove All..." << endl;
	tree.RemoveAll();
	cout << "Height: " << tree.Height() << endl;

	cout << "Verify Red Black Tree..." << endl;
	tree.verify(tree);

	cout << endl;
}

void AssignmentTest()
{
	cout << "--------------------------AssignmentTest---------------------------" << endl;

	cout << endl << "Basic Tree Size of Four" << endl;
	cout  << "Insert.." << endl;
	RedBlackTree<int> tree;
	tree.Insert(5);
	tree.Insert(4);
	tree.Insert(3);
	tree.Insert(2);

	cout << "Verify Red Black Tree 1..." << endl;
	tree.verify(tree);

	RedBlackTree<int> tree2;
	cout << "Assign Tree 1 to Tree 2..." << endl << endl;
	tree2 = tree;

	cout << "Verify Red Black Tree 2..." << endl;
	tree2.verify(tree2);

	cout << "Creat Blank Tree..." << endl ;
	RedBlackTree<int> treeEmpty;
	cout << "Size: " << treeEmpty.Size() << endl << endl;

	RedBlackTree<int> tree3(tree);
	cout << "Creat Tree3 Copy of Tree1..." << endl ;
	cout << "Insert..." << endl;
	tree3.Insert(3);
	tree3.Insert(2);
	cout << "Verify Red Black Tree 3..." << endl;
	tree3.verify(tree3);

	cout << "Assign Tree3 to Empty Tree..." << endl << endl;
	cout << "Verify Red Black Tree 3..." << endl;
	tree3 = treeEmpty;
	tree3.verify(tree3);

	cout << endl;
}

void StockSystemTest()
{
	cout << "--------------------------StockSystemTest---------------------------" << endl;

	StockSystem Sys;

	cout << "Create Stock System..." << endl;
	cout << "Default Balance: $" << Sys.GetBalance() << endl << endl;

	if (Sys.StockNewItem(StockItem(11111, "Apple", 10)) == true) { cout << "Stock Added..." << endl; }
	else { cout << "Stock Not Added..." << endl; }
	if (Sys.StockNewItem(StockItem(77777, "Dog", 5)) == true) { cout << "Stock Added..." << endl; }
	else { cout << "Stock Not Added..." << endl; }
	if (Sys.StockNewItem(StockItem(11111, "Pear", 12)) == true) { cout << "Stock Added..." << endl; }
	else { cout << "Stock Not Added (Already Exists)..." << endl; }
	cout << endl << "Balance: $" << Sys.GetBalance() << endl;
	cout << Sys.GetCatalogue() << endl;

	if (Sys.EditStockItemDescription(77777, "Boat") == true) { cout << "Stock Description Changed..." << endl; }
	else { cout << "Stock Description Not Changed(Not Found)..." << endl; }
	if (Sys.EditStockItemDescription(77717, "Pie") == true) { cout << "Stock Description Changed..." << endl; }
	else { cout << "Stock Description Not Changed(Not Found)..." << endl; }
	cout << endl << "Balance: $" << Sys.GetBalance() << endl;
	cout << Sys.GetCatalogue() << endl;

	if (Sys.EditStockItemPrice(11111, 777) == true) { cout << "Stock Price Changed..." << endl; }
	else { cout << "Stock Price Not Changed..." << endl; }
	if (Sys.EditStockItemPrice(44444, 10) == true) { cout << "Stock Price Changed..." << endl; }
	else { cout << "Stock Price Not Changed(Not Found)..." << endl; }
	cout << endl << "Balance: $" << Sys.GetBalance() << endl;
	cout << Sys.GetCatalogue() << endl;

	if (Sys.Restock(11111, 5, 10) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock..." << endl; }
	if (Sys.Restock(22222, 5, 10) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock(Already Exists)..." << endl; }
	if (Sys.Restock(77777, 5, 200) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock..." << endl; }
	if (Sys.Restock(77777, 3, 1000) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock..." << endl; }
	if (Sys.Restock(77777, 10, 3000) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock..." << endl; }
	if (Sys.Restock(77777, 555, 500000) == true) { cout << "Stock Restock..." << endl; }
	else { cout << "Stock Not Restock(Balance Too Low)..." << endl; }
	cout << endl << "Balance: $" << Sys.GetBalance() << endl;
	cout << Sys.GetCatalogue() << endl;

	if (Sys.Sell(11111, 7) == true) { cout << "Stock Sold..." << endl; }
	else { cout << "Stock Not Sold..." << endl; }
	if (Sys.Sell(77777, 11) == true) { cout << "Stock Sold..." << endl; }
	else { cout << "Stock Not Sold(Not Found)..." << endl; }
	if (Sys.Sell(99999, 100) == true) { cout << "Stock Sold..." << endl; }
	else { cout << "Stock Not Sold(Not Found)..." << endl; }
	if (Sys.Sell(11111, 11) == true) { cout << "Stock Sold..." << endl; }
	else { cout << "Stock Not Sold(0 Stock)..." << endl; }
	cout << endl << "Balance: $" << Sys.GetBalance() << endl;
	cout << Sys.GetCatalogue() << endl;


	cout << endl;
}


void MTest()
{
	int choice = 0;
	string inputchoice;
	int asku;
	string inputasku;
	string adesc;
	double aprice;
	string inputaprice;
	int amount;
	string inputamt;
	string ctlg = "";

	StockSystem mystore;

	while (choice != 8)
	{
		PrintMenu();
		// get the menu choice from standard input
		getline(cin, inputchoice);
		choice = atoi(inputchoice.c_str());

		switch (choice)
		{
		case 1: // Print balance
			cout << "Funds: $" << mystore.GetBalance() << endl << endl;
			break;
		case 2: // Print catalogue
			ctlg = mystore.GetCatalogue();
			cout << ctlg << endl;
			break;
		case 3: // Add SKU
			cout << "Enter a numeric SKU (will be converted to 5 digits): ";
			getline(cin, inputasku);
			asku = atoi(inputasku.c_str());
			cout << "Enter item description: ";
			getline(cin, adesc);
			cout << "Enter a retail price: $";
			getline(cin, inputaprice);
			aprice = atof(inputaprice.c_str());
			if (mystore.StockNewItem(StockItem(asku, adesc, aprice)))
				cout << "Successfully added item to catalogue." << endl;
			else
				cout << "Item not added to catalogue." << endl;
			break;
		case 4: // Edit item description
			cout << "Enter a numeric SKU to edit: ";
			getline(cin, inputasku);
			asku = atoi(inputasku.c_str());
			cout << "Enter item description: ";
			getline(cin, adesc);
			if (mystore.EditStockItemDescription(asku, adesc))
				cout << "Item successfully updated." << endl;
			else
				cout << "Item not updated." << endl;
			break;
		case 5: // Edit item price
			cout << "Enter a numeric SKU to edit: ";
			getline(cin, inputasku);
			asku = atoi(inputasku.c_str());
			cout << "Enter a retail price: $";
			getline(cin, inputaprice);
			aprice = atof(inputaprice.c_str());
			if (mystore.EditStockItemPrice(asku, aprice))
				cout << "Item successfully updated." << endl;
			else
				cout << "Item not updated." << endl;
			break;
		case 6: // Restock an item
			cout << "Enter a numeric SKU to purchase: ";
			getline(cin, inputasku);
			asku = atoi(inputasku.c_str());
			cout << "Enter a quantity to purchase: ";
			getline(cin, inputamt);
			amount = atoi(inputamt.c_str());
			cout << "Enter the per-unit purchase price: $";
			getline(cin, inputaprice);
			aprice = atof(inputaprice.c_str());
			if (mystore.Restock(asku, amount, aprice))
				cout << "Item successfully restocked." << endl;
			else
				cout << "Item not restocked." << endl;
			break;
		case 7: // Sell an item
			cout << "Enter the SKU of item to sell: ";
			getline(cin, inputasku);
			asku = atoi(inputasku.c_str());
			cout << "Enter a quantity to sell: ";
			getline(cin, inputamt);
			amount = atoi(inputamt.c_str());
			if (mystore.Sell(asku, amount))
				cout << "Transaction complete. Have a nice day." << endl;
			else
				cout << "Item is out of stock. Sorry!" << endl;
			break;
		case 8: // Quit
				// no need to do anything, will cause while loop to break
			break;
		default:
			cout << "Invalid choice." << endl;
			break;
		}
	}
}