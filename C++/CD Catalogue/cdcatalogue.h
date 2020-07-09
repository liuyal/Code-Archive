// File:        cdcatalogue.h
// Date:        2016-01-07
// Description: Declaration of a CDCatalogue class to be used 

#pragma once
#include <string> 
#include <iostream>
#include "cd.h"
using namespace std; 

class CDCatalogue
{
  private:
    CD* cds;       // dynamic array stores collection of CD objects
    int numcds;    // number of CDs identified in the collection
    int maxsize;   // size of the underlying dynamic array

    // Helper method for copy constructor
    // Performs deep copy of dynamic array
    void CopyArray(const CDCatalogue& cat);

  public:

    ///////////////////////////////
    // Constructors / Destructor //
    ///////////////////////////////

    // Default constructor
    // Creates an empty CDCatalogue with default array size (4)
	 CDCatalogue();
    
    // Copy constructor
    // Creates a new CDCatalogue object,
    // performs a deep copy of the cat parameter's fields
    CDCatalogue(const CDCatalogue& cat);
    
    // Destructor
    // Releases all memory allocated to private pointer members
    ~CDCatalogue();

    //////////////////////////
    // Mutators / Accessors //
    //////////////////////////

    // Insert - performs a set insertion with the CD catalogue
    // Inserts CD and returns true if CD is not already in the catalogue
    // Does not insert and returns false if a CD with a matching artist and album name
    //   already exists in the registry
    // If the array is already filled before the insertion occurs, then
    //   first create a new dynamic array double the size of the old array,
    //   copy all CD objects from old array to new array,
    //   deallocate memory associated with the old array,
    //   and insert the new CD and return true.
    // POST:  catalogue contains CD
    // PARAM: disc = item to be inserted, its fields should not be empty string
    // NOTE:  since overloaded assignment operator has not been defined,
    //          "insertion" will mean updating all fields of the CD at the appropriate index
    bool Insert(CD disc);
    
    // Remove - performs a set removal with the CD catalogue
    // Removes a CD with all matching parameters if one exists in the catalogue
    // Returns false if a CD with the same parameters does not exist in the catalogue
    // POST:  catalogue does not contain CD
    // PARAM: disc = item to be removed, its fields should not be empty string
    // NOTE:  "removal" if successful will be done by updating the parameters of the
    //          CD at the appropriate index using the parameters of the CD in
    //          the last valid index of the collection; then decrements count and returns true;
    bool Remove(CD disc);
    
    // Locates the array index of a CD with matching parameters
    // Returns -1 if no CD with matching parameters exists in the catalogue
    // PARAM: disc = item to be located, its fields should not be empty string
    int Find(CD disc) const;

    // Removes all CDs from the catalogue with artist matching the provided argument
    // Returns false if there are not matching CDs or input is empty string,
    //   otherwise returns true if at least one CD is removed
    // Remaining items may appear in the array in any order, with the requirement that
    //   there are no "empty" spaces in the array (i.e. an array with 5 items must occupy indices 0-4)
    // POST:  catalogue contains no instances of CDs with the supplied artist name
    // PARAM: dontlikeanymore = name of artist whose CDs should be removed from the catalogue
    bool Boycott(string dontlikeanymore);
    
    // Returns the number of CDs in the catalogue
    int Count() const;

	//remove
	void get()const
	{
		for (int i = 0; i < numcds; i++)
		{
			cout << "[" << i << "] " << "Artist: " << cds[i].GetArtist() << " ";
			cout << "Album: " << cds[i].GetAlbum() << endl;
		}
	
		cout << endl;
	}//Testing only

    ////////////////////
    // Set operations //
    ////////////////////

    // Returns the set union of this and cat
    // POST: union contains CD of this and cat, with no duplicate CDs (both parameters matching).
	CDCatalogue Join(const CDCatalogue& cat) const;
    
    // Returns the set intersection of this and cat
    // POST: intersection contains CDs in both this and cat (both parameters matching).
	CDCatalogue Common(const CDCatalogue& cat) const;
    
    // Returns the set difference of this and cat
    // CDs in both catalogues must have a full set of matching parameters
    //   for a CD to be removed in the split.
    // POST: difference contains CDs in this but not also in cat
	CDCatalogue Split(const CDCatalogue& cat) const;
};