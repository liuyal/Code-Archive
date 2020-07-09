// File:        stocksystem.cpp
// Date:        2016-02-28
// Description: implementation of a StockSystem class 

#include <math.h>
#include <sstream>

#include "stockitem.h"
#include "stocksystem.h"
#include "redblacktree.h"


//----------------------------------------------CONSTRUCTOR------------------------------------------------------

// default constructor;
// begin with a balance of $100,000.00
StockSystem::StockSystem()
{
	RedBlackTree<StockItem> *records = new  RedBlackTree<StockItem>;
	balance = 100000.00;
}

//------------------------------------------------ACCESSORS------------------------------------------------------

// returns the balance member
double StockSystem::GetBalance()
{
	return this->balance;
}

//------------------------------------------------MUTATORS------------------------------------------------------


// Add a new SKU to the system. Do not allow insertion of duplicate sku
bool StockSystem::StockNewItem(StockItem item)
{
	if (records.Search(item) == true)
	{
		return false;
	}

	if (item.GetSKU() < 10000 || item.GetSKU() > 99999)
	{
		return false;
	}

	//int number = item.GetStock()+1;
	//item.SetStock(number);
	records.Insert(item);

	return true;
}


// Locate the item with key itemsku and update its description field.
// Return false if itemsku is not found.
bool StockSystem::EditStockItemDescription(int itemsku, string desc)
{
	if (desc == "") {return false;}
	int size = records.Size();
	StockItem* arr = records.Dump(size);

	for (int i = 0; i < size; i++)
	{
		if (arr[i].GetSKU() == itemsku)
		{
			StockItem *item = records.Retrieve(arr[i]);
			item->SetDescription(desc);
			delete[] arr;
			return true;
		}
	}
	delete[] arr;
	return false;
}


// Locate the item with key itemsku and update its description field.
// Return false if itemsku is not found or retailprice is negative.
bool StockSystem::EditStockItemPrice(int itemsku, double retailprice)
{
	if (retailprice < 0) {return false;}

	int size = records.Size();
	StockItem* arr = records.Dump(size);

	for (int i = 0; i < size; i++)
	{
		if (arr[i].GetSKU() == itemsku)
		{
			StockItem *item = records.Retrieve(arr[i]);
			item->SetPrice(retailprice);
			delete[] arr;
			return true;
		}
	}
	delete[] arr;
	return false;
}


// Purchase quantity of item at unitprice each, to reach a maximum (post-purchase) on-hand stock quantity of 1000.
// Return false if balance is not sufficient to make the purchase,
//   or if SKU does not exist, or if quantity or unitprice are negative.
// Otherwise, return true and increase the item's on-hand stock by quantity,
//   and reduce balance by quantity*unitprice.
bool StockSystem::Restock(int itemsku, int quantity, double unitprice)
{
	int size = records.Size();
	StockItem* arr = records.Dump(size);

	if (quantity < 0 || unitprice < 0) {return false;}
	if (quantity >= 1000){quantity = 1000;}
	if ((quantity*unitprice) > balance) {return false;}

	for (int i = 0; i < size; i++)
	{
		if (arr[i].GetSKU() == itemsku)
		{
			StockItem *item = records.Retrieve(arr[i]);
			if(item->GetStock() >= 1000){return false;}

			int number = item->GetStock() + quantity;
			if(number >= 1000){quantity = 1000 - item->GetStock(); number = 1000;}

			item->SetStock(number);
			this->balance = balance - (quantity*unitprice);
			delete[] arr;
			return true;
		}
	}
	delete[] arr;
	return false;
}


// Sell an item to a customer, if quantity of stock is available and SKU exists.
// Reduce stock by quantity, increase balance by quantity*price, and return true if stock available.
// If partial stock (less than quantity) available, sell the available stock and return true.
// If no stock, sku does not exist, or quantity is negative, return false.
bool StockSystem::Sell(int itemsku, int quantity)
{
	int size = records.Size();
	StockItem* arr = records.Dump(size);

	if (quantity < 0) { return false; }

	for (int i = 0; i < size; i++)
	{
		if (arr[i].GetSKU() == itemsku)
		{
			StockItem *item = records.Retrieve(arr[i]);

			int number = item->GetStock() - quantity;
			if (number <= 0) { number = 0; }
			if (item->GetStock() <= 0) { return false; }

			if (number == 0)
			{
				this->balance = balance + ( item->GetStock()*item->GetPrice());
			}
			else
			{
				this->balance = balance + (quantity*item->GetPrice());
			}
			delete[] arr;
			item->SetStock(number);
			return true;
		}
	}
	delete[] arr;
	return false;
}









