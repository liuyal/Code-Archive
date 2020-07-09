

#include <iostream>
#include "Stack.h"


using namespace std;

void Test();


int main()
{
	Test();

	system("pause");
	return 0;
}


void Test()
{
	Stack<int> stack;

	stack.Push(2);
	stack.Push(20);
	stack.Push(51);
	stack.Push(32);
	stack.Push(2);
	stack.Push(20);

	cout << "Top: " << stack.Peek() << endl << "Size: " << stack.Size() << endl;

	stack.Print();

	Stack<int> stack2(stack);

	stack2.Push(500);
	stack2.Print();

	int x = stack2.Pop();
	cout << "POP: " << x << endl;

	stack2.Print();

	stack2.Push(77);
	stack2.Push(12);
	stack2.Push(0);

	stack = stack2;
	stack2.Print();
	stack.Print();

 	cout << endl;
}
