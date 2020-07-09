/* Strict Requirement --- Valid data values must be either zero or greater -
no negative numbers allowed. */

/*
Concepts: Sorting and swapping values in a static array. Using file I/O
1. In the main function, read the numbers from the file "input.txt" and insert
the elements into the array. The terminating "character" for the data in the array
is -1.
*/


#include <iostream>
#include <cstdlib> //to use exit()
#include <fstream> //for I/O
using namespace std;

//Defines the Max Array size- DO NOT change this value.
#define MAX_ARRAY_SIZE 201
const int TERMINATING_CHAR = -1;

//A Searchable Array Class
class S_Array
{
public:

	S_Array();
	//Default Constructor

	void set_array(ifstream& infile);
	//Address of the infile stream to read in values into data_array
	//PostCondition: filled data_array using the values inside input.txt
	//If an illegal number is inside input.txt, the program will skip that value

	int number_of_data_points();
	//PreCondition: Initialized data_array.
	//PostCondition: Returns the number of data points in the array.


	int search_and_remove(int value, int number_of_data_points);
	//PreCondition: Initialized data_array and a valid "value" (i.e. zero or a positive Number.
	//PostCondition: Any occurrences of "value" have been removed from data_array.
	//Then return value indicates how many times "value" was found in data_array.


	//void print_array(); //DELETE THIS BEFORE SUBMISSION. ONLY TO HELP DEBUG. Prints the new array after search_and_remove

private:

	// HELPER FUNCTIONS

	int next;
	int data_array[MAX_ARRAY_SIZE];
};

/*
void S_Array::print_array()
{
	next = 0;
	while (data_array[next] != TERMINATING_CHAR)
	{
		cout << data_array[next] << " ";
		next++;
	}
}
//Prints the new array after search_and_remove*/


//Default Constructor
S_Array::S_Array()
{
	next = 0;               //New array, next data insertion point is at the beginning.
	data_array[next] = -1;  //Used to indicate that there is no valid data in the array yet.
}

//PreCondition: Initialized data_array.
//PostCondition: Returns the number of data points in the array.
int S_Array::number_of_data_points()
{
	int number_of_data_points = 0;

	while (data_array[number_of_data_points] != TERMINATING_CHAR)
	{
		number_of_data_points++;
	}
	return number_of_data_points;
}

//PreCondition: Initialized data_array and a valid "value" (i.e. zero or a positive Number.
//PostCondition: Any occurrences of "value" have been removed from data_array.
//Then return value indicates how many times "value" was found in data_array.
int S_Array::search_and_remove(int value, int number_of_data_points)
{
	int number_of_occurrences = 0;
	for (next = 0; next <= number_of_data_points; next++)
	{
		if (data_array[next] == value)
		{
			int counter = next; //value of next placed inside counter so that the value of next doesn't change
			next--; //decrement to cancel increment of for loop because a new value will be placed inside the current index (next)
			do
			{
				data_array[counter] = data_array[counter + 1];
				counter++;
			} while (counter < number_of_data_points);
			number_of_occurrences++;
		}
	}
	return number_of_occurrences;
}

//PreCondition: Empty data_array, address of the infile to read
//PostCondition: Filled data_array with terminating char -1
//Program will terminate if negative number present in input.txt
void S_Array::set_array(ifstream& infile)
{
	int value; //only present in this function to fill data_array
	next = 0;
	while (infile >> value && next < MAX_ARRAY_SIZE)
	{
		if (value >= 0)
		{
			data_array[next] = value;
			next++;
		}
		else
		{
			cerr << "Error: Unexpected value (must be >= 0)";
		}
	}
	data_array[next] = TERMINATING_CHAR;
}


int main()
{
	S_Array my_array;
	// Here is pseudocode for main():
	// 1) open the file input.txt
	// 2) Read the numbers in sequentially from the input.txt file and store them in
	//    my_array.
	// 3) use number_of_data_points to tell the user how many data points were in the file.
	// 4) Search for the value(s) listed in search.txt and tell the user how many times
	//    each of these values occurred using the format:
	//    >Search Value ?? occurred ?? times.
	// 5) End the program when  done searching for values.

	// INSERT YOUR CODE HERE
	int value;
	int number_of_data_points;
	ifstream infile;

	infile.open("input.txt");
	if (infile.fail())
	{
		cerr << "Input file failed opening.\n";
		exit(1);
	}

	my_array.set_array(infile); //fill the array with allowed values

	infile.close();
	infile.open("search.txt");
	if (infile.fail())
	{
		cerr << "Input file failed opening.\n";
		exit(1);
	}
	number_of_data_points = my_array.number_of_data_points();

	while (infile >> value)
	{
		if (value >= 0)
		{
			cout << "Search Value " << value << " occurred " << my_array.search_and_remove(value, number_of_data_points) << " times." << endl;
		}
		else if (value == TERMINATING_CHAR)
		{
			//do nothing
		}
		else
		{
			cerr << "Invalid value to search for.\n" << endl;
			exit(1);
		}
	}
	//my_array.print_array(); // This function is to help debug the program

    infile.close();

	return 0;
}

