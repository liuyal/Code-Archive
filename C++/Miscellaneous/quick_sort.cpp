/*quick sort algorithm */

#include <cstdlib>
#include <iostream>
#include <fstream> //To enable input file
#include <vector> // To enable vectors
using namespace std;

void print_array(int array[], int low, int hi)
{
	cout<< "quick sort partition steps: ";
	for (int j=low; j<=hi;j++)
		cout <<" "<< array[j];
	cout << endl;
}//end of print_array

void swap(int arr[], int i, int j)
{
	// temp to store arr[i]
	int temp = arr[i];
	arr[i] = arr[j];
	arr[j] = temp;

	return;
}// swap needs to be ontop of partition for identification

int partition (int arr[], int low, int hi)
{
	int pivot = arr[hi];
	int i = low;

    // To index between start and pivot and pivot and end
	for (int j = low; j<=hi-1; j++)
	{
		if (arr[j] <= pivot)
		{
			swap(arr, i, j);
			i++;
		}
	}
	// print_array(arr, low, hi); // test
	swap(arr, i, hi);
	return i;
}


void quick_sort(int arr[], int low, int high)
{
	int pivot; // missing break;

	if (low < high) // function parameters is high not hi
	{
		pivot = partition(arr, low, high);
		quick_sort(arr, low, pivot-1); //Between 0 and pivot sort
		quick_sort(arr, pivot+1, high); //between pivot and end sort
		//quick_sort is the functions missing _
	}

	return;
}

	int main()
	{
		//DECLARE ARRAY HERE?:
		int size;
		int value;
		vector<int> numbers;
		//initialize vector

		ifstream file;
		file.open("input.txt");
		//Open file input.txt

		if (file.eof())
        {
         cerr << "FILE IS EMPTY, TRY AGAIN" << endl;
        return 1;
        }//Check for file error.
        if (file.fail())
        {
         cerr << "FILE FAILED TO LOAD" << endl;

        return 2;
        }

		while (file >> value)
		{numbers.push_back(value);}
		size = numbers.size() - 1;
		//Insert numbers into vector

        if (size + 1 > 200)
        {
            cerr << "ERROR FILE HAS MORE THAN MAXIMUN 200 NUMBERS" << endl;

        return 3;
        }
        else if (size <= 0)
        {
            cerr << "FILE IS EMPTY, TRY AGAIN" << endl;

         return 4;
        }// limit of array


		int* array = &numbers[0];
		//Pointer array to vector

		file.close();

		//These functions has 3 different inputs/parameters
		print_array(array, 0, size);
		quick_sort(array, 0, size);
		print_array(array, 0, size);

		return 0;
	}//end of main
