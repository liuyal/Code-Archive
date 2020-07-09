
#include <iostream>
#include "Stack.h"

using namespace std; 

/*--------------------------------------------------------*/

//Default Constructor used to create an empty Stack object.
Stack::Stack() : top(NULL) //Setting the pointer to the top of the stack to NULL
{
	//purposefully empty
}

/*--------------------------------------------------------*/

//Destructor for Stack objects.
Stack::~Stack()
{
	string* next = NULL;
	StackFramePtr temp_ptr;

 	while (!empty())
	{
		delete top->str;
		temp_ptr = top;
		top = top->next;
		delete temp_ptr;
	}
}

/*--------------------------------------------------------*/

//PreCondition: Start with a Stack object.
//PostCondition: Add the string in a new frame at the top of the Stack.
void Stack::push(string& str) 
{
	StackFramePtr temp_ptr;
	temp_ptr = new StackFrame;

	temp_ptr->str = &str;
	temp_ptr->num_char = str.length();

	temp_ptr->next = top;
	top = temp_ptr;
}

/*--------------------------------------------------------*/

//PreCondition: Start with Stack object.
//PostCondition: Remove the top Stack Frame and return the string stored at the top.
//               of the Stack.
string Stack::pop()
{
	StackFramePtr temp_ptr;
	string* result = NULL;
	string str;
	
	if (empty())
	{
		cout << "Empty Stack! Cannot pop." << endl << endl;
		return "\0"; //Trying to return a NULL doesnt work!!!!!!!!!!! (only for pointers)
	}
	else if (top->str == NULL) //if the string is null
	{
		temp_ptr = top;
		top = top->next;
		delete temp_ptr;
		return "\0"; //Trying to return a NULL doesnt work!!!!!!!!!!! (only for pointers)
	}
	else
	{
		result = top->str;
		temp_ptr = top;
		top = top->next;
		delete temp_ptr;
		return(*result);
	}
}

/*--------------------------------------------------------*/

StackFramePtr Stack::remove_strings_length(int length)
{
	StackFramePtr NewStackPtr = NULL; //Soon to be the pointer to the top of a stack of removed strings
	StackFramePtr here = NULL; //current stack frame
	StackFramePtr before = NULL; //stack frame before current frame
	StackFramePtr temp_ptr = NULL;

	return Stack::Recursive_Search_and_Remove(length, NewStackPtr, here, before, temp_ptr); 
	//This function searches the stack until it finds a string of length "length" and
	//removes it then puts into into another stack with its top pointed to by NewStackPtr 
	//NewStackPtr will point to the top of the stack of removed strings  
}

/*--------------------------------------------------------*/

//Search the ENTIRE Stack and remove all frames that have a string of
//               length "length". All frames with strings of length "length" should 
//               be returned in a new stack where those frames that were closest to 
//               the top are still at the top of this new stack. Furthermore, the 
//               orignal Stack should be returned with these selected frames removed
//               and the relative ordering of the remaining frames unchanged.
StackFramePtr Stack::Recursive_Search_and_Remove(int length,  StackFramePtr NewStackPtr, StackFramePtr currentFrame, StackFramePtr before, StackFramePtr temp_ptr)
{
	int counter = 0; //to synchronize "before" to point to the stackframe before "here"

	if (top->num_char == length) //for when the string in the top stack frame has length "length"
	{
		temp_ptr = top;
		top = top->next;
		temp_ptr->next = NewStackPtr;
		NewStackPtr = temp_ptr;
		if (top == NULL) //stopping case
		{
			return NewStackPtr;
		}
		return Stack::Recursive_Search_and_Remove(length, NewStackPtr, currentFrame, before, temp_ptr);
	}
	else //for when the string in the first frame is not of length "length"
	{
		currentFrame = top; //current stack frame
		before = top; //Will become the frame before the current frame 

		if (currentFrame == NULL) 
		{
			return NULL; //for empty stack
		}
		else 
		{	//This while loop is used to search the stack for a frame where the string is of length "length"
			//And also sets up "before" to point to the frame before currentFrame 
			while (currentFrame->next != NULL && currentFrame->num_char != length)  
			{
				currentFrame = currentFrame->next; 
				if (counter >= 1)
				{
					before = before->next; //setting before to be the frame before current frame
				}
				counter++;
			}
			//Checking to make sure that the loop didn't stop because the next frame is NULL
			if (currentFrame->num_char == length)
			{
				before->next = currentFrame->next;

				temp_ptr = currentFrame;
				temp_ptr->next = NewStackPtr;
				NewStackPtr = temp_ptr;
				return Stack::Recursive_Search_and_Remove(length, NewStackPtr, currentFrame, before, temp_ptr);
			}
			else return NewStackPtr; //because the loop went through the whole stack all the way to NULL
		}
	}
}
/*--------------------------------------------------------*/

//Checks to see if the Stack is empty.  Returns true if empty, else returns false.
//Stack remains unchanged after function call.
bool Stack::empty()
{
	return (top == NULL);
}

/*--------------------------------------------------------*/

// Starting at the top of the stack and writes out each StackFrame on a separate line.
//Uses the format:
// "<string>" [<num_char>]
// "<string>" [<num_char>]
// "<string>" [<num_char>]
// ... (down to the bottom of the stack)
//Note the first printed entry should be from the top of the stack and the values in 
//the stack should remain unchanged.
ostream &operator << (ostream &output, Stack &Stack)
{
	StackFramePtr iter = Stack.top;
	if (iter == NULL) //for empty stack
	{
		output << "Empty Stack" << endl << endl;
	}
	for (iter = Stack.top; iter != NULL; iter = iter->next)
	{
		if (*iter->str == "\0")
		{
			output << "\0" << " " << NULL << endl;
		}
		else output << *iter->str << " " << iter->num_char << endl;
	}
	return output;
}

/*--------------------------------------------------------*/

//Reads in the value and stores it in a StackFrame at the top of the Stack.
istream &operator >> (istream &input, Stack &Stack) //extraction operator (input is already connected to a file)
{
	string* str_from_input = NULL;
	StackFramePtr temp_ptr = NULL;
	
	str_from_input = new string;
	input >> *str_from_input;
	Stack.push(*str_from_input);

	return input;
}