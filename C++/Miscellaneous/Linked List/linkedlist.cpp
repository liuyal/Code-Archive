
#include "linkedlist.h"
#include <iostream>
#include <fstream> 

LinkedList :: LinkedList()
{
    front = NULL;
    back = NULL;
	//cout << "Object is being created" << endl << endl;
}
//Default Constructor used to create an empty list object.



LinkedList :: ~LinkedList()
{
	//cout << "Object is being destroyed" << endl << endl;

	ListNode* temp = front;
	while (temp != 0)
	{
		ListNode* next = temp->next;
		delete temp;
		temp = next;
	}
	front = 0;
}
//Destructor for LinkedList.




void LinkedList::insert_beginning(int value)
{
	ListNode *NewNode = new ListNode();   // create new Node
	NewNode->value = value;               // set value
	NewNode->next = front;			      // make node point to the next node.
	front = NewNode;                      //  Make head point at the new node.

}
//PreCondition: Start with LinkedList object.
//PostCondition: Add the "value" to position 1 in the list (at the front)
//               The position value of all other nodes needs to be adjusted
//               accordingly.






void LinkedList::insert_end(int value)
{
	ListNode*NextNode = new ListNode(); // create new Node
	NextNode->value = value;		    // set value
	NextNode->next = NULL;				// make node point to the next node.

	if (front == NULL)
	{
		front = NextNode;				//Front is empty then new node is front
	}
	else
	{
		ListNode*temp = front;			
		while (temp->next != NULL)
			temp = temp->next;
		temp->next = NextNode;
	}

}
//PreCondition: Start with LinkedList object.
//PostCondition: Add the "value" to position N+1 in the list (at the back),
//               where N is the number of nodes previously in LinkedList object.






ListNodePtr LinkedList::remove_value(int val)
{

	ListNode *tempNode = front;
	ListNode *prevNode = NULL;
	LinkedList Remove_list;
	int counter = 0;

	while (tempNode != NULL)
	{
		if (tempNode->value == val)
		{
			if (tempNode == front)
			{
				front = front -> next;
			}
			else
			{
				prevNode->next = tempNode->next;
			}
			counter = counter + 1;
		}
		else
		{
			prevNode = tempNode;
		}
		tempNode = tempNode->next;
	}

	for (int i = 1; i <= counter;i++)
	{
		if (front == NULL)
		{
			Remove_list.insert_beginning(val);
		}
		else
		{
			Remove_list.insert_end(val);
		}
	}
	cout << "Removed list from value [" << val  << "]: " << endl;


	if (Remove_list.empty() == 1)
	{
		cout << "Linked List is empty" << endl;
		cout << "Removed value list is empty" << endl << endl;
	}
	cout << Remove_list;

return tempNode;
}
//PreCondition: Start with LinkedList object.
//PostCondition: Find all objects with value "val" and 1) remove them from the
//               current list and 2) return them as their own linked list with the
//               position values correctly updated. Adjust the position value of all
//               the nodes in your LinkedList object accordingly.



int LinkedList::removefront()
{
	if (front == NULL)
	{
		cout << "The Linked List is empty" << endl;
		return -1;
	}
	else
		if (front->next == NULL)
		{
			front = NULL;
			cout << "The first node is deleted" << endl;
			cout << "The Linked List is empty" << endl;
			return 0;
		}

	ListNode *temp;
	temp = (ListNode*)malloc(sizeof(ListNode));
	//Allocates a block of size bytes of memory, returning a pointer to the beginning of the block
	temp = front;
	front = temp->next;
	free(temp);
	//free memory
	cout << "The first node is deleted" << endl;
	return 0;
}
//PreCondition: Start with LinkedList object.
//PostCondition: The node at the "front" of the original list has been removed and
//               its value has been returned by this function.  The positions of all
//               remaining nodes in the LinkedList object have been updated.



bool LinkedList::empty()
{
	if (front == NULL)
	{
		//cout << "Linked List is empty " << endl;
		return true;
	}
	else
	{
		//cout << "Linked List is not empty " << endl;
		return false;
	}
}
//Checks to see if the LinkedList is empty.  Returns true if empty, else returns false.
//LinkedList remains unchanged after function call.



void LinkedList::sort_linkedlist()
{
	ListNode * temp_front = front;
	//Size of list
	int temp;
	int counter = 0;

	while (temp_front)
	{
		temp_front = temp_front->next;
		counter++;
	}
	temp_front = front;

	for (int j = 0; j<counter; j++)
	{
		while (temp_front->next)
		{
			if (temp_front->value > temp_front->next->value)
			{
				temp = temp_front->value;
				temp_front->value = temp_front->next->value;
				temp_front->next->value = temp;

			}
			else
				temp_front = temp_front->next;
		}
		temp_front = front ;
	}
}
//PreCondition: Start with a LinkedList object (likely unsorted).
//PostCondition The LinkedList object will be updated so that it is now sorted with
//              the smaller values located at the front and the larger values located
//              at the back.


ostream &operator <<(ostream &output, LinkedList &object)
{
	//cout << "The list content is: " << endl;;
	ListNode * Current_Nodes = object.front;
	int place = 1;

	if (Current_Nodes == NULL)
	{
		cout << endl;
		cout << "List is empty";
	}
	while (Current_Nodes != NULL)
	{
		cout << place <<". " << Current_Nodes-> value <<endl;
		Current_Nodes = Current_Nodes->next;
		place++;
	}
	cout << endl;
	return output;
}
//Starting at the head of the list, writes out the LinkedList for each node in the
//list from front to back. Uses the format:
// <position>. <value>
// <position>. <value>
// <position>. <value>
// ... (until the end of the list)
//Note the "position" numbers should be sequential counting from 1 to N, where N is
//the number of nodes in the list.





istream &operator >> (istream &input, LinkedList &list)
{
	int in = 0;
	input >> in;
		if (list.front == NULL)
		{
			list.insert_beginning(in);
		}
		else
		{
			list.insert_end(in);
		}
return input;
}
//Reads in the "value" and stores it in the N+1 position in the
//linked List, given that there are currently N items in the LinkedList.

