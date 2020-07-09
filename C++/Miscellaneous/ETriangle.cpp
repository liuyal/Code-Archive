
#include <iostream>    // using IO functions
using namespace std;

#define sqr_two  1.4142 // Please use this value of the square root of two in
// in your calculations.

#define sqr_three  1.7321 // Please use this value of the square root of 3 in
// in your calculations.



/////////////////////////////
class ETriangle //EQUILATERAL TRIANGLE CLASS
{

public:
	ETriangle(double s_length);
	//Precondition: User provides side_length.
	//Postcondition: Both side_length and height member variables are initialized.

	ETriangle();
	//Default Constructor: initializes the side_length to 1 and the height accordingly.

	double get_side_length();
	//Member Function: Accessor
	//Precondition: Object initialized.
	//Postcondition: Returns the side_length of the equilateral triangle.

	double get_height();
	//Member Function: Accessor
	//Precondition: Object initialized.
	//Postcondition: Returns the height of the equilateral triangle.

	double get_perimeter();
	//Member Function: Accessor
	//Precondition: Object initialized.
	//Postcondition: Returns the perimeter of the equilateral triangle.

	void set_side_length(double s_length);
	//Member Function: Mutator
	//Precondition: Object initialized.
	//Postcondition: Updates the side_length AND height according to the user input.

	double get_surface_area();
	//Member Function: Accessor
	//Precondition: Object initialized.
	//Postcondition: Returns the surface area of the equilateral triangle.

private:
	double height;      // Data member Variable
	double side_length; // Data member variable

};   // need to end the class declaration with a semi-colon

	 /////////////////////////////




	 

	 ////////////////// ETriangle Member Function Definitions ///////////////

//Precondition: User provides side_length.
//Postcondition: Both side_length and height member variables are initialized.
ETriangle::ETriangle(double s_length)
{
	side_length = s_length;
	height = (sqr_three / 2)*s_length;  ///ADD THE MISSING CALCULATION HERE./////////
}

//Default Constructor: initializes the side_length to 1 and the height accordingly.
ETriangle::ETriangle()
{
	side_length = 1;
	height = (sqr_three / 2)*side_length;  ///ADD THE MISSING CALCULATION HERE.////////
}

//Member Function: Accessor
//Precondition: Object initialized.
//Postcondition: Returns the side_length of the equilateral triangle.
double ETriangle::get_side_length()
{
	return side_length;
}

//Member Function: Accessor
//Precondition: Object initialized.
//Postcondition: Returns the height of the equilateral triangle.
double ETriangle::get_height()
{
	return height;
}

//Member Function: Accessor
//Precondition: Object initialized.
//Postcondition: Returns the perimeter of the equilateral triangle.
double ETriangle::get_perimeter()
{
	return 3 * side_length;
}

//Member Function: Mutator
//Precondition: Object initialized.
//Postcondition: Updates the side_length AND height according to the user input.

void ETriangle::set_side_length(double s_length)
{
	side_length = s_length;
	height = (sqr_three / 2)*side_length;  ///ADD THE MISSING CALCULATION HERE./////////
}

//Member Function: Accessor
//Precondition: Object initialized.
//Postcondition: Returns the surface area length of the equilateral triangle.
double ETriangle::get_surface_area()
{
	return  (side_length*height) / 2;
}
/////////////////////////////




/////////////////////////////

//EQUILATERAL Triangular Prism class with access to ETriangle's public
class ETriangularPrism : public ETriangle 
{

public:

	ETriangularPrism(double s_length, double length);
	//User provides side_length and length of prism.
	//Both side_length, length and height member variables are initialized.

	ETriangularPrism();
	//Default Constructor: initializes the side_length, length and the height to1.

	double get_side_length();
	//Member Function: Accessor
	//Access and Returns the side_length of the equilateral triangular prism.

	double get_height();
	//Member Function: Accessor
	//Access and Returns the height of the equilateral triangular prism.

	double get_length();
	//Member Function: Accessor
	//Access and Returns the length of the equilateral triangular prism.

	double get_perimeter();
	//Member Function: Accessor
	//Access and Returns the perimeter of the prism

	double get_surface_area();
	//Member Function: Accessor
	//Access and Resturens surface area of prism

	double get_volume();
	//Member Function: Accessor
	//Access and Returns volume of the prism

	void set_length(double in_length);
	//Member Function: Mutator
	//Update length of prism arrcording to user input;

private:

	double height;      // Data member Variable
	double side_length; // Data member variable
	double length;		// Data member variable
};
/////////////////////////////





/////////////// ETriangular Prism Member Function Definitions ///////////////////
ETriangularPrism::ETriangularPrism(double s_length, double in_length) :ETriangle(s_length)
{
	side_length = s_length;
	length = in_length;
	height = (sqr_three / 2)*s_length;
}
//User provides side_length and length of prism.
//Both side_length,length and height member variables are initialized.


ETriangularPrism::ETriangularPrism()
{
	length = 1;
	side_length = 1;
	height = (sqr_three / 2)*side_length;
}
//Default Constructor: initializes the side_length and height to 1 and the height accordingly.


double	ETriangularPrism :: get_side_length()
{
	return side_length;
}
//Member Function: Accessor
//Returns side_length of equilateral triangular prism.

double	ETriangularPrism::get_height()
{
	return height = (sqr_three / 2)*side_length;
}
//Member Function: Accessor
//Returns Height of equilateral triangular prism.

double ETriangularPrism::get_length()
{
	return length;
}
//Member Function: Accessor
//Returns length of equilateral triangular prism.

double  ETriangularPrism::get_perimeter()
{
	return 6*(side_length) + 3*(length);
}
//Member Function: Accessor
//Returns perimeter of equilateral triangular prism.


double ETriangularPrism:: get_surface_area()
{
	return  2*((side_length*height)/2) + 3*(side_length*length);
}
//Member Function: Accessor
//Returns surface area of equilateral triangular prism.


double ETriangularPrism::get_volume()
{
	return ((side_length*height)/2)*length;
}
//Member Function: Accessor
//Returns volume of equilateral triangular prism.


void ETriangularPrism::set_length(double in_length)
{
	length = in_length;
}
//Member Function: Mutator
//Updates the length according to the user input.

/////////////////////////////





/////////////////////////////

/* Create a new class called SquarePyramid  HERE*/

class SquarePyramid : public ETriangle
{

public:

	SquarePyramid(double s_length);
	//User provides side_length.
	//Both side_length,elevationn and height member variables are initialized.

	SquarePyramid();
	//Default Constructor: initializes the side_length to 1 and the height accordingly.

	double get_side_length();
	//Member Function: Accessor
	//Returns the side_length of the square pyramid

	double get_elevation();
	//Member Function: Accessor
	//Returns the elecation of the square pyramid

	double get_perimeter();
	//Member Function: Accessor
	//Returns the perimeter of the square pyramid

	double get_surface_area();
	//Member Function: Accessor
	//Returns surface area of the square pyramid

	double get_volume();
	//Member Function: Accessor
	//Returns the volume of the square pyramid

private:
	double height;      // Data member Variable
	double side_length; // Data member variable
	double elevation;   // Data member variable

};

//*
////////////////////////////





/////////////// Square Pyramid Member Function Definitions ///////////////
SquarePyramid::SquarePyramid(double s_length) : ETriangle(s_length)
{
	side_length = s_length;
	elevation = side_length / sqr_two;
	height = (sqr_three / 2)*s_length;
}
//User provides side_length and length of prism.
//Both side_length,elevationn and height member variables are initialized.

SquarePyramid::SquarePyramid()
{
	side_length = 1;
	elevation = side_length / sqr_two;
	height = (sqr_three / 2)*side_length;
}
//Default Constructor: initializes the side_length,elevation and height to 1

 double SquarePyramid:: get_side_length()
{
	return side_length;
}
 //Member Function: Accessor
 //Returns side_length of square pyramid.

 double SquarePyramid::get_elevation()
{
	return side_length / sqr_two;
}
 //Member Function: Accessor
 //Returns elevation of square pyramid.

 double SquarePyramid::get_perimeter()
 {
	 return 8 * (side_length);
 }
 //Member Function: Accessor
 //Returns perimeter of square pyramid.

 double SquarePyramid::get_surface_area()
 {
	 return 4 * ((side_length*height) / 2) + (side_length*side_length);
 }
 //Member Function: Accessor
 //Returns surface area of square pyramid.

 double SquarePyramid::get_volume()
 {

	 return (side_length*side_length*elevation)/3;
 }
 //Member Function: Accessor
 //Returns volume of square pyramid.

////////////////////////////




int main() 
{
	// +---+- - - - - -+---------------+
	// |                               |
	// |       		TEST   	  		   |
	// |                               |
	// +---+- - - - - -+---------------+
	/*
	// Construct a ETriangle instance
	ETriangle t1(10.0);
	cout << " side length = " << t1.get_side_length() << endl;
	cout << " height = " << t1.get_height() << endl;
	cout << " perimeter = " << t1.get_perimeter() << endl;
	cout << endl;

	// Create a new Object of Type Class ETriangularPrism and initialize it with
	// side_length = 15 and length = 20

	ETriangularPrism t2(15.0,20.0);
	cout << " side length = " << t2.get_side_length() << endl;
	cout << " height = " << t2.get_height() << endl;
	cout << " length = " << t2.get_length() << endl;
	cout << " surface area = " << t2.get_surface_area() << endl;
	cout << " volume = " << t2.get_volume() << endl;

	//-------------------------------------------------
	// INSERT CODE HERE  TO CALCULATE THE PERIMETER OF THE TRIANGLE-----
	//---  Try t2.get_perimeter();
	//---  Does it work ??? If yes, what perimeter value is calculated??
	//--------------------------------------------------
	cout << " perimeter = " << t2.get_perimeter() << endl << endl;

	// Create a new Object of Type Class SquarePyramid and initialize it with
	// side_length = 25
	SquarePyramid t3(25);
	cout << " side length = " << t3.get_side_length() << endl;
	cout << " height = " << t3.get_height() << endl;
	cout << " elevation = " << t3.get_elevation() << endl;
	cout << " surface area = " << t3.get_surface_area() << endl;
	cout << " volume = " << t3.get_volume() << endl;

	//-------------------------------------------------
	// INSERT CODE HERE  TO CALCULATE THE PERIMETER OF THE TRIANGLE-----
	//---  Try t3.get_perimeter();
	//---  Does it work ???
	// Report the Elevation of the pyramid here as well.
	//--------------------------------------------------
	cout << " perimeter = " << t3.get_perimeter() << endl << endl;
    */
	//-------------------------------------------------
	// INSERT CODE HERE
	// CALL THE MEMBER FUNCTIONS CREATED EARLIER to print the output of
	// Surface area and volume of the triangle prism and square pyramid-----
	//--------------------------------------------------


	// +---+- - - - - -+---------------+
	// |                               |
	// |     |
	// |                               |
	// +---+- - - - - -+---------------+


	double side;
	double in_length;

	cout << ">Enter side length of equilateral triangle: ";
	cin >> side;
	//User provid Input of side length used for all 3 classes

	if (side <= 0)
	{
		cerr << "ERROR Invalide side length";
		return 0;
	}
	else if (!cin || cin.fail())
	{
		// user didn't input a number
		cin.clear(); // reset failbit
		cerr << "ERROR Please Enter a Number";
		return 0;
	}
	//Detect any input errors
	//End process if ant error occurs

	cout << ">Enter length of triangular prism : ";
	cin >> in_length;
	cout << endl;
	//User provides length of triangular prism

	if (in_length <= 0)
	{
		cerr << "ERROR Invalide length";

		return 0;
	}
	else if (!cin || cin.fail())
	{
		// user didn't input a number
		cin.clear(); // reset failbit
		cerr << "ERROR Please Enter a Number";
		return 0;
	}
	//Detect any input errors
	//End process if ant error occurs

	ETriangle t1(side);
	ETriangularPrism t2(side, in_length);
	SquarePyramid t3(side);

	cout << t1.get_height() << endl;		  //Height of the ETriangle object
	cout << t1.get_perimeter() << endl;		  //Perimeter of the ETriangle object
	cout << t1.get_surface_area() << endl;	  //Surface area of the ETriangle object

	cout << t2.get_surface_area() << endl;    //Surface area of the ETrianglePrism object
	cout << t2.get_volume() << endl;		  //Volume of the ETrianglePrism object

	cout << t3.get_surface_area() << endl;	  //Surface area of the SquarePyramid object
	cout << t3.get_volume() << endl;		  //Volume of the SquarePyramid object
	cout << t3.get_elevation() << endl;	      //Elevation of the SquarePyramid object

	return 0;
}

