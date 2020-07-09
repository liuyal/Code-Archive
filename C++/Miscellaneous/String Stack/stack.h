#ifndef STACK_H
#define STACK_H

// Title: stack.h 

//**************************************************************************************


//Objective: To create the basic member functions to be able to create
//           and manipulate a stack.



#include <iostream>
#include <string>
using namespace std;



struct StackFrame
{
	string* str; // Value(string?) stored at the node // Need to use dynamic memory for this // something like *str = new string 
	int num_char; //Stores the length of the string (excluding the termination character '/0'
	StackFrame * next; // Points to the next object/frame in the Stack.
};

typedef StackFrame* StackFramePtr; //Type defined as a pointer to a StackFrame structure

//A Stack with a pointer to the top of the stack.  All insertions and removals happen 
//at the top of the stack.
class Stack
{
public:
	
	Stack();
	//Default Constructor used to create an empty Stack object.

	~Stack();
	//Destructor for Stack objects.

	void push(string& str); 
	//PreCondition: Start with a Stack object.
	//PostCondition: Add the string in a new frame at the top of the Stack.


	string pop();
	//PreCondition: Start with Stack object.
	//PostCondition: Remove the top Stack Frame and return the string stored at the top.
	//               of the Stack.

	//HINT: This is easier if you use recursion =)	
	StackFramePtr remove_strings_length(int length);
	//PreCondition: Start with a Stack.
	//PostCondition: Search the ENTIRE Stack and remove all frames that have a string of 
	//               length "length". All frames with strings of length "length" should 
	//               be returned in a new stack where those frames that were closest to 
	//               the top are still at the top of this new stack. Furthermore, the 
	//               orignal Stack should be returned with these selected frames removed
	//               and the relative ordering of the remaining frames unchanged.

	bool empty();
	//Checks to see if the Stack is empty.  Returns true if empty, else returns false.
	//Stack remains unchanged after function call.


	friend ostream &operator<<(ostream &, Stack &);
	//Starting at the top of the stack and writes out each StackFrame on a separate line.
	//Uses the format:
	// "<string>" [<num_char>]
	// "<string>" [<num_char>]
	// "<string>" [<num_char>]
	// ... (down to the bottom of the stack)
	//Note the first printed entry should be from the top of the stack and the values in 
	//the stack should remain unchanged.

	friend istream &operator>>(istream &, Stack &);
	//Reads in the value and stores it in a StackFrame at the top of the Stack.
	//

private:
	StackFramePtr top; // Points to the top of the stack;

	StackFramePtr Recursive_Search_and_Remove(int length, StackFramePtr NewStackPtr, StackFramePtr here, StackFramePtr before, StackFramePtr temp_ptr);

};
#endif