// File:        a1simpledriver.cpp
// Author:      Ya Qi Liu 
// Date:        2016-01-08
// Description: Basic test driver
//              This file tests some functions of the CDCatalogue class 
//              Note that only functions which are called will be compiled, therefore must
//                ensure that every function in CDCatalogue class is called at least once.
//              In general, Ensure that test:
//               1. invalid parameter(s)
//               2. valid parameter(s), boundary case
//               3. valid parameter(s), general case

#include <iostream>
#include <string> 

#include "cd.h" 
#include "cdcatalogue.h"

using namespace std;

// forward function declarations
void TestFunc1();
void TestFunc2();
void TestFunc3();
void PrintMenu();


// program entry point
int main()
{
  // CDCatalogue object will be instantiated within a function call
  //  and thus will be local to that function.
  // Destructor will be called automatically when the function returns
  cout << "Entering test function 1: " << endl;
  TestFunc1();

  cout << "Returned from test function 1.\nEntering test function 2: " << endl;
  TestFunc2();

  cout << "Returned from test function 2.\nEntering interactive test function: " << endl;
  TestFunc3();

  return 0;
}

// test function code
void TestFunc1()
{
  // call default constructor
  CDCatalogue cat1;

  // remove some non-existent item
  cat1.Remove(CD("Wham!", "Make It Big"));

  // insert some item
  cat1.Insert(CD("KISS", "Destroyer"));

  // display collection size
  cout << "Number of discs in collection: " << cat1.Count() << endl;
}



void TestFunc2()
{
  CDCatalogue cat1;
  cat1.Insert(CD("1", "1"));
  cat1.Insert(CD("3", "3"));
  cat1.Insert(CD("4", "4"));
  cat1.Insert(CD("5", "5"));
  cat1.Insert(CD("5", "6"));
  cout << "-----1------" << endl;
  cat1.get();
  
  // copy constructor
  //CDCatalogue cat2(cat1);
  CDCatalogue cat2;

  // remaining function calls
  cat2.Boycott("Aqua");
  cat2.Insert(CD("2", "2"));
  cat2.Insert(CD("3", "3"));
  cat2.Insert(CD("4", "4"));

  cout << "-----2------" << endl;
  cat2.get();

  int index = cat1.Find(CD("New Kids on the Block", "Hangin' Tough"));

  // set function calls
  CDCatalogue catjoin(cat1.Join(cat2));
  cout << "-----J------" << endl;
  catjoin.get();

  CDCatalogue catcommon(cat1.Common(cat2));
  cout << "-----C------" << endl;
  catcommon.get();

  CDCatalogue catsplit(cat1.Split(cat2));
  cout << "-----S------" << endl;
  catsplit.get();

  }



void TestFunc3()
{
  // local variables for interaction
  int choice = -1;
  string inputchoice;
  string inputartist;
  string inputalbum;
  int findindex;
  bool boycottresult;

  CDCatalogue mycat;

  while (choice != 6)
  {
    PrintMenu();
    // get the menu choice from standard input
    getline(cin, inputchoice);
    choice = atoi(inputchoice.c_str());
    
    switch (choice)
    {
      case 1: // Add a CD
        cout << "\nEnter the artist name: ";
        getline(cin, inputartist);
        cout << "\nEnter the album name: ";
        getline(cin, inputalbum);
        if (mycat.Insert(CD(inputartist, inputalbum)))
          cout << "CD added to collection." << endl;
        else
          cout << "You already have this CD." << endl;
        break;
      case 2: // Remove a CD
        cout << "\nEnter the artist name: ";
        getline(cin, inputartist);
        cout << "\nEnter the album name: ";
        getline(cin, inputalbum);
        if (mycat.Remove(CD(inputartist, inputalbum)))
          cout << "CD removed from collection." << endl;
        else
          cout << "You don't own this CD." << endl;
        break;
      case 3: // Display collection size
        cout << "Collection contains " << mycat.Count() << " CDs." << endl;
        break;
      case 4: // Find a CD index
        cout << "\nEnter the artist name: ";
        getline(cin, inputartist);
        cout << "\nEnter the album name: ";
        getline(cin, inputalbum);
        findindex = mycat.Find(CD(inputartist, inputalbum));
        if (findindex >= 0)
          cout << "CD found at index " << findindex << "." << endl;
        else
          cout << "CD not found." << endl;
        break;
      case 5: // Boycott an artist
        cout << "\nEnter the artist name: ";
        getline(cin, inputartist);
        boycottresult = mycat.Boycott(inputartist);
        if (boycottresult)
          cout << "All CDs by " << inputartist << " have been dumped on craigslist." << endl;
        else
          cout << "No eligible CDs to dump." << endl;
        break;
      case 6: // Quit
        // no need to do anything, will cause while loop to break
        break;
	  case 7: // list			
		  mycat.get();
			  // no need to do anything, will cause while loop to break
		  break;
      default:
        cout << "Invalid choice." << endl;
        break;
    }
  }
}



void PrintMenu()
{
  cout << "********************************************************\n"
       << "* Please select an option:                             *\n"
       << "* 1. Add a CD                  5. Boycott an artist    *\n"
       << "* 2. Remove a CD                                       *\n"
       << "* 3. Display collection size   6. Quit                 *\n"
       << "* 4. Find a CD index           7. List Catalogue       *\n"
       << "********************************************************\n" << endl;
  cout << "Enter your choice: ";
}