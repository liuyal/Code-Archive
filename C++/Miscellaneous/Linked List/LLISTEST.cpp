
#include <iostream>
#include <fstream>
#include "linkedlist.h" 

using namespace std;


int main()
{
	LinkedList list;


	cout << endl;
	cout << list.empty() << endl;

	list.remove_value(11);
	cout << "---------------------------------------------------" << endl;
	list.insert_beginning(20);
	list.insert_end(11);
	list.insert_end(52);
	list.insert_end(12);
	list.insert_end(5);
	list.insert_end(2);
	list.insert_end(8);
	list.insert_end(1);
	list.insert_end(11);

	cout << list.empty() << endl << endl;;
	cout << list;
	cout << endl;

	cout << "---------------------------------------------------" << endl;

	int size;
	cout << "Number of Inputs: ";
	cin >> size;

	for (int i = 0;i < size; i++)
	{cin >> list;}
	cout << endl << "New list" << endl;
	cout << list;

	cout << endl << "---------------------------------------------------" << endl;

	cout << "Sort list " << endl;
	list.sort_linkedlist();
	cout << list;

	cout << "---------------------------------------------------" << endl;

	cout << "remove Front" << endl;
	list.removefront();
	cout << list;

	cout << "---------------------------------------------------" << endl;

	cout << "Sort List" << endl;
	list.sort_linkedlist();
	cout << list;
	cout << endl;


	cout << "---------------------------------------------------" << endl;

	cout << "Remove Value [11]" << endl;
	list.remove_value(11);
	cout << endl;


	cout << "---------------------------------------------------" << endl;

	cout << list;
	cout << endl;



	cout << "---------------------------------------------------" << endl;
	ifstream infile;
	infile.open("input.txt");
	while (!infile.eof())
	{
		if (infile.eof())
		{
			break;
		}
     	infile >> list;
	}
	infile.close();
	cout << list <<"end of file" <<endl;

	cout << "---------------------------------------------------" << endl;

	cout << endl << "Input Value: ";
	cin >> list;
	cout << list;
	cout << endl << "---------------------------------------------------" << endl;

	cout << endl << "Sort list " << endl;
	list.sort_linkedlist();
	cout << list;

	cout << "---------------------------------------------------" << endl;

 	return 0;
}
