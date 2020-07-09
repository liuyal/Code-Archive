// File:        hashtable.cpp
// Description: Implementation of a hash table class 
//              must include hashtableprivate.h file for additional private member functions

#include <cstdlib>
#include <math.h> 
#include <string>
#include <vector>

#include "slinkedlist.h"
#include "useraccount.h"
#include "hashtable.h"

//------------------------------------HELPER FUNCTIONS-----------------------------------------

// hash function, uses Horner's method
// Assume input string consists only of lower-case a to z
int HashTable::Hash(string input) const
{
	int value = input[0] - 96;
	int ch = 0;

	if (input.length() == 1) 
	{
		value = value % this->maxsize;
	}
	else
	{
		for (unsigned int i = 0; i < input.length() - 1; i++)
		{
			ch = input[i + 1] - 96;
			value = (value * 32) + ch;
			value = value % this->maxsize;
		}
	}
	return value;
}

// helper function to find smallest prime number greater than supplied parameter
int HashTable::SmallestPrime(int n) const
{
	do { IsPrime(n);n++; } while (IsPrime(n) != true);
	return n;
}

// helper function to determine whether a number is prime
bool HashTable::IsPrime(int n) const
{
	if (n <= 3) { return n > 1; }
	else if (n % 2 == 0 || n % 3 == 0) { return false; }
	else
	{
		for (int i = 5; i * i <= n; i += 6)
		{
			if (n % i == 0 || n % (i + 2) == 0) { return false; }
		}

		return true;
	}
}

// Resizes the hashtable into a larger array.
// Return false if n is smaller than current array size or if n is negative.
// Else, set array size to the smallest prime number larger than n
//   and re-hash all contents into the new array, delete the old array and return true.
bool HashTable::Resize(int n)
{
	if (n < this->size || n <= 0) { return false; }

	int newMaxsize = SmallestPrime(n);
	int oldMaxsize = this->maxsize;

	SLinkedList<UserAccount> *Oldtable = table;

	table = new SLinkedList<UserAccount> [newMaxsize];
	this->maxsize = newMaxsize;
	this->size = 0;

	vector<UserAccount> Vector;

	for (int i = 0; i < oldMaxsize; i++)
	{
		Vector = Oldtable[i].Dump();

		for (unsigned int v = 0; v < Vector.size(); v++)
		{
			this->Insert(Vector.at(v));
		}
	}

	for (int i = 0 ; i < oldMaxsize; i++){Oldtable[i].RemoveAll();}

	delete[] Oldtable;

	return true;
}


//--------------------------------------------Constructors-------------------------------------------------   

// default constructor
// creates an array of size 101
HashTable::HashTable()
{
	this->size = 0;
	this->maxsize = 101;
    table = new SLinkedList<UserAccount>[maxsize];
}

// parameterized constructor
// creates an array of size = smallest priame number > 2n
HashTable::HashTable(int n)
{
	this->size = 0;
	this->maxsize = SmallestPrime(2 * n);
	table = new SLinkedList<UserAccount>[maxsize];
}

// copy constructor
// Creates deep copy of sourceht
HashTable::HashTable(const HashTable& sourceht)
{
	table = new SLinkedList<UserAccount>[sourceht.MaxSize()];
	this->maxsize = sourceht.MaxSize();
	this->size = 0;

	vector<UserAccount> Vector;

	for (int i = 0; i < sourceht.MaxSize(); i++)
	{
		Vector = sourceht.table[i].Dump();

		for (unsigned int v = 0; v < Vector.size(); v++)
		{
			this->Insert(Vector.at(v));
		}
	}
}

// destructor
HashTable::~HashTable()
{
	for (int i = 0 ; i < this->maxsize; i++){table[i].RemoveAll();}

	delete[] table;

	table = NULL;
	this->size = 0;
	this->maxsize = 0;
}

// overloaded assignment operator
HashTable& HashTable::operator=(const HashTable& sourceht)
{
	if (sourceht.Size() == 0)
	{
		for (int i = 0 ; i < this->maxsize; i++){table[i].RemoveAll();}

		delete[] table;

		table = NULL;
		this->size = 0;
		this->maxsize = sourceht.MaxSize();
		
		table = new SLinkedList<UserAccount>[maxsize];

		return *this;
	}
	
	if (this != &sourceht)
	{
		for (int i = 0 ; i < this->maxsize; i++){table[i].RemoveAll();}
		
		this->Resize(sourceht.MaxSize());
		this->size = 0;
		this->maxsize = sourceht.MaxSize();

		vector<UserAccount> Vector;

		for (int i = 0; i < sourceht.MaxSize(); i++)
		{
			Vector = sourceht.table[i].Dump();

			for (unsigned int v = 0; v < Vector.size(); v++)
			{
				this->Insert(Vector.at(v));
			}
		}
	}

	return *this;
}

//------------------------------------------------MUTATORS---------------------------------------------   

// Insertion
// If item does not already exist, inserts at back of hashed list and returns true
//   otherwise returns false
// If load factor (before insertion) is above 2/3, expand into a new
//   table of smallest prime number size at least double the present table size
//   and then insert the item.
bool HashTable::Insert(UserAccount acct)
{
	if (this->Search(acct) == true) { return false; }

	if (LoadFactor() > 2.00/3.00){ this->Resize(2*this->maxsize);}
	
	this->size++;

	int index = Hash(acct.GetUsername());

	table[index].InsertBack(acct);

	return true;
}

// Removal
// If item exists, removes and returns true
//   otherwise returns false
bool HashTable::Remove(UserAccount acct)
{
	if (this->Search(acct) == false) { return false; }

	int index = Hash(acct.GetUsername());

	table[index].Remove(acct);

	this->size--;

	return true;
}

//--------------------------------------------ACCESSORS------------------------------------------------   

// Search
// Returns true if item exists, false otherwise
bool HashTable::Search(UserAccount acct) const
{
	int index = Hash(acct.GetUsername());

	if (table[index].Contains(acct) == true)
	{
		return true;
	}

	return false;
}

// Retrieval
// Returns a pointer to a UserAccount object inside the hash table (linked list)
//   if a matching parameter is found, otherwise return NULL
UserAccount* HashTable::Retrieve(UserAccount acct)
{
	UserAccount* value = NULL;

	int index = Hash(acct.GetUsername());

	if (table[index].Contains(acct) == true)
	{
		value = table[index].Retrieve(acct);

		return value;
	}

	return value;
}

// Returns the number of items stored in the hash table
int HashTable::Size() const
{
	return this->size;
}
// Returns the size of the underlying array
int HashTable::MaxSize() const
{
	return this->maxsize;
}

// Returns the load factor as size / maxsize.
// Note that due to separate chaining, load factor can be > 1.
double HashTable::LoadFactor() const
{
	double U = this->size;
	double L = this ->maxsize;

	return U / L;
}

