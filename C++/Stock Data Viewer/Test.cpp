

#include <iostream>
#include <fstream>
#include <sstream>

#include <cstdlib>
#include <string>
#include <vector>

#include "Stock.h"
#include "DLinkedList.h"

using namespace std;


int main()
{

	Stock Google("GOOG", "GOOG.csv");

	cout << "Set" << endl;

	DLinkedList<int> list;

	list.InsertFront(1);
	list.InsertFront(2);
	list.InsertFront(3);


	system("pause");

	return 0;
}