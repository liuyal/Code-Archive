#include <iostream>
#include <string>
#include <fstream>

#include "Stack.h"

using namespace std; 

int main()
{
	ifstream infile;
	ofstream outfile;

	Stack Stack1;
	Stack Stack_removed;
	Stack Stack2;

	string popped_string;
	string popped_string2;
	string str = "\0";
	string str1;
	string str2;

	StackFramePtr NewStack;
	StackFramePtr temp_ptr;

	infile.open("2.txt");
	outfile.open("output.txt");


	while (!infile.eof())
	{
		infile >> Stack1;
	}

    cout << "input first string: ";
	cin >> Stack1;
	cout << "input second string: ";

	cin >> Stack2;
	cout << endl;

	str1 = Stack2.pop();


	cout << str1 << endl << endl;
	Stack1.push(str1);

	outfile << Stack1 << endl << endl;

	Stack1.push(str);

	str2 = Stack1.pop();

	cout << str2 << endl << endl;

	cout << Stack1 << endl << endl;


	popped_string = Stack1.pop();

	popped_string2 = Stack1.pop();

	cout << popped_string << endl << endl;
	cout << Stack1 << endl << endl;



	NewStack = Stack1.remove_strings_length(5);

	cout << Stack1 << endl <<endl;

	while (NewStack != NULL)
	{
		cout << *NewStack->str << endl;
		temp_ptr = NewStack->next;
		NewStack = temp_ptr;
	}

	cout << endl << endl;

	Stack1.~Stack();

	cout << Stack1 << endl << endl;

	str = Stack1.pop();

	cout << Stack1;

	return 0;
}
