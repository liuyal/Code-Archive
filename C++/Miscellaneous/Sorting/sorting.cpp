
// File:        sorting.cpp
// Author:      Ya Qi Liu
// Date:        2016-02-08

#include <iostream>


// Selection Sort
//Look for smallest element and swap to front
//Repeat for next smallest element
//Param: arr[] = array to be sorted, n = array size
//Post: arr[]  sorted, returns number of barometer operation
template <class T>
int SelectionSort(T arr[], int n)
{
	if (n < 0) { throw exception("n is Out of Range"); }

   int count = 0; //Counter for barometer operations
   int smallest = 0;
   T temp;

   for (int i = 0; i < n - 1; i++)
   {
	   smallest = i;

	   for (int j = i + 1; j < n; j++)
	   {
		   //Look for smallest element
		   if (arr[j] < arr[smallest])
		   {
			   smallest = j;
		   }
		    count++;
	   }
	   //swap elements
	   if (smallest != i)
	   {
		   temp = arr[i];
		   arr[i] = arr[smallest];
		   arr[smallest] = temp;
	   }
   }
   return count;
}



//Quicksort
//Param: arr[] = array to be sorted, n = array size
//Post: arr[]  sorted, returns number of barometer operation
template <class T>
int Quicksort(T arr[], int n)
{
	if (n < 0) { throw exception("n is Out of Range"); }

  int count = 0;

  QuicksortHelper(arr, 0, n-1, count);

  return count;
}

//Create partitions and pivot and subarrays
//Recursive sort subarrays
template <class T>
void QuicksortHelper(T arr[], int low, int high, int& counter)
{
	if (low < high)
	{
		int pivot = QSPartition(arr, low, high, counter);
		QuicksortHelper(arr, low, pivot - 1, counter);
		QuicksortHelper(arr, pivot + 1, high, counter);
	}
}

//Partition function
template <class T>
int QSPartition(T arr[], int low, int high, int& counter)
{
	int pivotindex = low;
	T pivot = arr[high];
	T temp = arr[low];

	for (int j = low; j <= high - 1; j++)
	{
		if (arr[j] <= pivot)
		{
			temp = arr[pivotindex];
			arr[pivotindex] = arr[j];
			arr[j] = temp;
			pivotindex++;
		}
		counter++;
	}

	temp = arr[pivotindex];
	arr[pivotindex] = arr[high];
	arr[high] = temp;

	return pivotindex;
}



// Randomized Quicksort
//Param: arr[] = array to be sorted, n = array size
//Post: arr[]  sorted, returns number of barometer operation
template <class T>
int RQuicksort(T arr[], int n)
{
	if (n < 0) { throw exception("n is Out of Range"); }

	int count = 0;

	RQuicksortHelper(arr, 0, n - 1, count);
	
	return count;
}

//Create partitions and pivot and subarrays
//Recursive sort subarrays
template <class T>
void RQuicksortHelper(T arr[], int low, int high, int& counter)
{
	if (low < high)
	{
		int pivot = RQSPartition(arr, low, high, counter);
		RQuicksortHelper(arr, low, pivot - 1, counter);
		RQuicksortHelper(arr, pivot + 1, high, counter);
	}
}

//Partition function
template <class T>
int RQSPartition(T arr[], int low, int high, int& counter)
{
	int pivotindex = low + rand() % (high - low + 1);
	T temp = arr[high];
	arr[high] = arr[pivotindex];
	arr[pivotindex] = temp;

	T pivot = arr[high];
	T temp2,temp3;
	int i = low - 1;

	for (int j = low; j <= high - 1; j++)
	{
		if (arr[j] <= pivot)
		{
			i++;
			temp2 = arr[i];
			arr[i] = arr[j];
			arr[j] = temp2;
		}
	 counter++;
	}

	temp3 = arr[i + 1];
	arr[i + 1] = arr[high];
	arr[high] = temp3;

	return i + 1;
}



//Mergesort
//Param: arr[] = array to be sorted, n = array size
//Post: arr[]  sorted, returns number of barometer operation
template <class T>
int Mergesort(T arr[], int n)
{
  if (n < 0) { throw exception("n is Out of Range"); }

  int count = 0;

  MergesortHelper(arr, 0, n - 1, n, count);

  return count;
}

//Sorts Array By:
// 1. Sorting the first half of the array
// 2. Sorting the second half of the array
// 3. Merging the two sorted halves
template <class T>
void MergesortHelper(T arr[], int low, int high, int n, int& counter)
{
	if (low < high)
	{
		int mid = (high + low) / 2;
		MergesortHelper(arr, low, mid, n, counter);
		MergesortHelper(arr, mid + 1, high, n, counter);
		Merge(arr, low, mid, high, n, counter);
	}
}

//Merge function combines the sorted subarrays
template <class T>
void Merge(T arr[], int low, int mid, int high, int n, int& counter)
{
	T *TempArray = new T[n];

	//Local variables to index subarray
	int low1 = low;
	int high1 = mid;
	int low2 = mid + 1;
	int high2 = high;

	int index = low1;

	//Subarrays are not empty
	//Cpoty smaller item into temporary array
	while ((low1 <= high1) && (low2 <= high2))
	{
		if (arr[low1] <= arr[low2])
		{
			TempArray[index] = arr[low1];
			low1++;
		}
		else
		{
			TempArray[index] = arr[low2];
			low2++;
		}
		index++;
	}
	//First subarray
	while (low1 <= high1)
	{
		TempArray[index] = arr[low1];
		low1++;
		index++;
	}
	//Second subarray
	while (low2 <= high2)
	{
		TempArray[index] = arr[low2];
		low2++;
		index++;
	}
	//Copy sorted back into original array
	for (index = low; index <= high; index++)
	{
		arr[index] = TempArray[index];
	}
	counter++;
}



//Shell Sort
//Algorithm From: Data Abstraction & Problem Solving with C++ - 6th (P332)
//Param: arr[] = array to be sorted, n = array size
//Post: arr[]  sorted, returns number of barometer operation
template <class T>
int ShellSort(T arr[], int n)
{
	if (n < 0) { throw exception("n is Out of Range"); }

	int count = 0;

	for (int j = n / 2; j > 0; j = j / 2)
	{
		for (int i = j; i < n; i++)
		{
			T Next = arr[i];
			int index = i;
			count++;
			while (index >= j && arr[index - j] > Next)
			{
				arr[index] = arr[index - j];
				index = index - j;
				count++;
					
			}
			arr[index] = Next;
		}
	}

  return count;
}



