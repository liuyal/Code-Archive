// File:        cd.cpp
// Date:        2016-01-07
// Description: Implementation of a CD class to be used 

#include "cd.h"
 
// Default constructor
CD::CD() 
{
  artist = "AC/DC";
  albumtitle = "Back in Black";
}

// Parameterized constructor
CD::CD(string artistname, string title)
{
  artist = artistname;
  albumtitle = title;
}

// MUTATORS
// Methods for updating CD's private fields
// Update will only occur if parameter is not empty string
// Returns true if update is successful, false otherwise.
bool CD::UpdateArtist(string artistname)
{
  if (artistname != "")
  {
    artist = artistname;
    return true;
  }
  return false;
}

bool CD::UpdateAlbum(string title)
{
  if (title != "")
  {
    albumtitle = title;
    return true;
  }
  return false;
}

bool CD::Update(string artistname, string title)
{
  if (artistname != "" && title != "")
  {
    artist = artistname;
    albumtitle = title;
    return true;
  }
  return false;
}

// ACCESSORS
// Methods for retrieving CD information
string CD::GetArtist() const
{
  return artist;
}

string CD::GetAlbum() const
{
  return albumtitle;
}

// OVERLOADED OPERATORS
// equality is true if all fields match
// not-equals is true if any field does not match
bool CD::operator==(const CD& disc) const
{
  return (artist == disc.artist && albumtitle == disc.albumtitle);
}

bool CD::operator!=(const CD& disc) const
{
  return !(*this == disc);
}