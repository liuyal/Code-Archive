// File:        cdcatalogue.cpp
// Date:        2016-01-07
// Description: Implementation of a CDCatalogue class to be used 

#include "cdcatalogue.h" 
#include <string> 

/////////////////////////////////////////////////////////////////////////////////////////
//****CDCatalogue class function definitions******
/////////////////////////////////////////////////////////////////////////////////////////

// Helper method for copy constructor
// Performs deep copy of dynamic array
void CDCatalogue::CopyArray(const CDCatalogue& cat)
{
	numcds = cat.numcds;
	maxsize = cat.maxsize;
	cds = new CD[maxsize];

	for (int i = 0; i < maxsize; i++)
	{
		cds[i] = cat.cds[i];
	}
}


// Default constructor
// Creates an empty CDCatalogue with default array size (4)
CDCatalogue :: CDCatalogue()
{
	numcds = 0;
	maxsize = 4;
	cds = new CD[maxsize];
}


// Copy constructor
// Creates a new CDCatalogue object,
// performs a deep copy of the cat parameter's fields
CDCatalogue :: CDCatalogue(const CDCatalogue& cat)
{
	//CDCatalogue tempCata;
	//tempCata.CopyArray(cat);
	numcds = cat.numcds;
	maxsize = cat.maxsize;
	cds = new CD[maxsize];

	for (int i = 0; i < maxsize; i++)
	{
		cds[i] = cat.cds[i];
	}
}


// Destructor
// Releases all memory allocated to private pointer members
CDCatalogue :: ~CDCatalogue()
{
	delete[] cds;
}


// Insert - performs a set insertion with the CD catalogue
// Inserts CD and returns true if CD is not already in the catalogue
// Does not insert and returns false if a CD with a matching artist and album name
bool CDCatalogue::Insert(CD disk)
{
	//Temperary strings for disk members
	string ArtName = disk.GetArtist();
	string AlbName = disk.GetAlbum();


	if (ArtName == "" || AlbName == "" )
	{
		return false;
	}

	for (int i = 0; i < numcds; i++)
	{
		//DUPLICATE ENTRY
		if (ArtName == cds[i].GetArtist() && AlbName == cds[i].GetAlbum())
		{
			return false;
		}
	}

	//UPDATE ARRAY IF EXCEED MAXSIZE
	if (numcds >= maxsize-1)
	{
		//Create array to hold old catalogue
		CD *oldCata = cds;
		maxsize = maxsize * 2;
		//Create new array of double maxsize
		cds = new CD[maxsize];

		//copy process
		for (int i = 0; i < numcds; i++)
		{
			cds[i] = oldCata[i];
		}
		//Free memory
		delete[] oldCata;
	}

	//INSERT DISK TO CATALOGE
	cds[numcds] = disk;
	numcds++;

	return true;
}


// Remove - performs a set removal with the CD catalogue
// Removes a CD with all matching parameters if one exists in the catalogue
// Returns false if a CD with the same parameters does not exist in the catalogue
bool CDCatalogue::Remove(CD disk)
{
	int found = Find(disk);

	if (found != -1)
	{
		for (int i = found; i < numcds; i++)
		{
			//Move index of all cd after up by 1
			cds[i] = cds[i + 1];
		}

		//Count of cd decrease by 1
		numcds--;
		return true;
	}
	else
	{
		return false;
	}

	return false;
}


// Locates the array index of a CD with matching parameters
// Returns -1 if no CD with matching parameters exists in the catalogue
// PARAM: disc = item to be located, its fields should not be empty string
int CDCatalogue::Find(CD disk)const
{
	string ArtName = disk.GetArtist();
	string AlbName = disk.GetAlbum();


	if (ArtName == "" || AlbName == "")
	{
		return -1;
	}

	for (int i = 0; i < maxsize; i++)
	{
		//Check for artist and album name of disk in catalogue
		if (ArtName == cds[i].GetArtist() && AlbName == cds[i].GetAlbum())
		{
			//return index at i
			return i;
		}
		else
		{
			continue;
		}
	}

	return -1;
}


// Removes all CDs from the catalogue with artist matching the provided argument
// Returns false if there are not matching CDs or input is empty string,
//   otherwise returns true if at least one CD is removed
bool CDCatalogue::Boycott(string dontlikeanymore)
{
	string ArtName = dontlikeanymore;

	//Detect empty Catalogue or empty input
	if (numcds == 0 || dontlikeanymore == "")
	{
		return false;
	}
	else
	{
		//Find CD with Artist name
		for (int i = 0; i < numcds; i++)
		{
			if (cds[i].GetArtist() == dontlikeanymore)
			{
				//Remove CD
				Remove(cds[i]);
				i--;
			}
		}
		return true;
	}
}


// Returns the number of CDs in the catalogue
int CDCatalogue::Count() const
{
	return numcds;
}



// Returns the set union of this and cat
// POST: union contains CD of this and cat, with no duplicate CDs (both parameters matching).
CDCatalogue CDCatalogue :: Join(const CDCatalogue& cat) const
{
	//Create new Catalogue
	CDCatalogue new_CDCatalogue;

	for (int i = 0; i < this->numcds; i++)
	{
		new_CDCatalogue.Insert(cds[i]);
	}

	for (int i = 0; i < cat.numcds; i++)
	{
		new_CDCatalogue.Insert(cat.cds[i]);
	}

	return new_CDCatalogue;
}



// Returns the set intersection of this and cat
// POST: intersection contains CDs in both this and cat (both parameters matching).
CDCatalogue CDCatalogue::Common(const CDCatalogue& cat) const
{
	//Create new Catalogue
	CDCatalogue new_CDCatalogue;
	CDCatalogue DummyCatalogue;
	bool Check = true;

	//Insert into dummy catalogue
	for (int i = 0; i < this->numcds; i++)
	{
		Check = DummyCatalogue.Insert(cds[i]);
	}
	//check if disk from cat exist in dummy catalogue
	for (int i = 0; i < cat.numcds; i++)
	{
		Check = DummyCatalogue.Insert(cat.cds[i]);
		
		//If disk exist then insert function returns false
		//Common CD is added to new catalogue
		if (Check == false)
		{
			new_CDCatalogue.Insert(cat.cds[i]);
		}
	
	}

	return new_CDCatalogue;
}



// Returns the set difference of this and cat
// CDs in both catalogues must have a full set of matching parameters
//   for a CD to be removed in the split.
// POST: difference contains CDs in this but not also in cat
CDCatalogue CDCatalogue::Split(const CDCatalogue& cat) const
{
	//Create new Catalogue
	CDCatalogue new_CDCatalogue;
	CDCatalogue DummyCatalogue;

	bool Check = false;

	//REVERSE OF COMMON
	//Insert into dummy catalogue
	for (int i = 0; i < cat.numcds; i++)
	{
		Check = DummyCatalogue.Insert(cat.cds[i]);
	}

	//check if disk from cat exist in dummy catalogue
	for (int i = 0; i < this->numcds; i++)
	{
		Check = DummyCatalogue.Insert(cds[i]);

		//If disk don't exist then insert function returns true
		//Differnt CD is added to new catalogue
		if (Check == true)
		{
			new_CDCatalogue.Insert(cds[i]);
		}
	}

	return new_CDCatalogue;
}
