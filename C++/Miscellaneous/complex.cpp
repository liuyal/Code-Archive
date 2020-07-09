




/*
This programming module is to  Overloading operators
 member functions for Class Complex to define/overload the
     basic arithmetic operations   '+','-'.'*','/','!=','==','>','<' 
*/


#include <cmath>
#include <iostream>

using namespace std;



class Complex
{
public:
	Complex(float=1.0,float=1.0);
	void set_real_and_imag (float x, float y);
	void print_complex();
	void print_magnitude();  //Print the Magnitude of the Complex number.


	///////////////////OVER load of each operator for complex class////////////////////

	friend bool operator == (const Complex& x, const Complex& y);
	//Boolean function for if k = l

	friend bool operator != (const Complex& x, const Complex& y);
	//Boolean  function for if k not = to l

	friend bool operator > ( Complex& x, Complex& y);
	//Boolean  function for k bigger than l

	friend bool operator < ( Complex& x, Complex& y);
	//Boolean  function for k smaller than l

	friend Complex operator + (const Complex& x, const Complex& y);
	//Overload operator function for adding complex numbers k and l

	friend Complex operator - (const Complex& x, const Complex& y);
	//Overload operator function for subtracting complex numbers k and l

	friend Complex operator * (const Complex& x, const Complex& y);
	//Overload operator function for multiplying complex numbers k and l

	friend Complex operator / (const Complex& x, const Complex& y);
	//Overload operator function for dividing complex numbers k and l

	friend ostream &operator<<(ostream &, Complex &);
	friend istream &operator>>(istream &, Complex &);

  // CAN You OVERLOAD AN OPERATOR USING "friend" keyword ????

private:
	float real;       //Real part
	float imaginary;  //Imaginary part
	float calculate_magnitude();   //Returns the magnitude of the Complex number.

};


bool  operator == (const Complex &x, const Complex &y)
{
	if (x.real == y.real && x.imaginary == y.imaginary)
	{return true;}

	else
	{return 0;}
}
//Boolean function for if k = l
//Dectect if real part is equal and imaginary part is equal
//If both equals return true

bool  operator != (const Complex &x, const Complex &y)
{
	if (x.real != y.real || x.imaginary != y.imaginary)
	{return true;}

	else
	{return 0;}
}
//Boolean function for if k is not = l
//Dectect if real part is not equal and imaginary part is not equal
//If either the real or imaginart is differnt return true

bool  operator > ( Complex &x, Complex &y)
{

	if (x.real > y.real)
	{return true;}

	if (x.real == y.real && x.imaginary > y.imaginary)
	{return true;}

	else
	{return 0;}
}
//Boolean function for if k is bigger l
//Dectect if real part is bigger first, if it is return true
//If the real part is equal, then compare imaginary part
//Retrun true if imaginary part of k is bigger

bool  operator < (Complex &x, Complex &y)
{
	if (x.real < y.real)
	{return true;}
	
	else if (x.real == y.real && x.imaginary < y.imaginary)
	{return true;}
	
	else
	{return 0;}
}
//Boolean function for if k is smaller l
//Dectect if real part is smaller first, if it is return true
//If the real part is equal, then compare imaginary part
//Retrun true if imaginary part of k is smaller

Complex operator + (const Complex& x, const Complex& y)
{
	Complex temp;
	temp.real = x.real + y.real;
	temp.imaginary = x.imaginary + y.imaginary;

	return temp;
}
//Overload operator + for adding complex numbers k and l
//Add real part of k and l
//Then add imaginary part of k and l
//Return solution


Complex operator - (const Complex& x, const Complex& y)
{
	Complex temp;
	temp.real = x.real - y.real;
	temp.imaginary = x.imaginary - y.imaginary;

	return temp;
}
//Overload operator - for subtracting complex numbers k and l
//Subtract real part of k and l
//Then subtract imaginary part of k and l
//Return solution


Complex operator * (const Complex& x, const Complex& y)
{
	Complex temp;
	temp.real = (x.real * y.real) - (x.imaginary * y.imaginary);
	temp.imaginary = (x.real * y.imaginary) + (x.imaginary * y.real);

	return temp;
}
//Overload operator * for multiplting complex numbers k and l
//Mutiply real part of k to both parts of l
//Mutiply imaginay part of k to both parts of l
//Combine all like terms
//Return solution


Complex operator / (const Complex& x, const Complex& y)
{

	Complex temp;
	temp.real = ((x.real * y.real) + (x.imaginary * y.imaginary))/ ((y.real*y.real)+(y.imaginary*y.imaginary));
	temp.imaginary =  ((x.imaginary * y.real)-(x.real * y.imaginary)) / ((y.real*y.real) + (y.imaginary*y.imaginary));

	return temp;
}
//Overload operator / for dividing complex numbers k and l
//Multiply k and l by inverse of l
//Combin like terms
//Return solution


/////////////////////////////////////

float Complex :: calculate_magnitude()
{
	return sqrt(real*real + imaginary*imaginary);
}
//This member access real and imaginary and caluale the magnitude of complex number
//Magnitude of complex number is sqrt(a^2+b^2) if complex = a+j*b, where j is complex

void Complex::print_magnitude()
{
	cout << "Magnitude = " << calculate_magnitude() << endl;
}
//This member print out the magnitude calulated from calculate_magnitude();

/////////////////////////////////////


/*--------------------------------------------------------*/

Complex::Complex(float m, float n)
{
	set_real_and_imag(m,n);
}

/*--------------------------------------------------------*/

void Complex::set_real_and_imag(float x, float y)
{
	
	real = x;
	imaginary = y;

}

/*--------------------------------------------------------*/

void Complex::print_complex()
{
	cout<<real<<" + j"<<imaginary<<endl;
}

/*--------------------------------------------------------*/

ostream &operator<<(ostream &output, Complex &object)
{
	output<<object.real<<" + j"<<object.imaginary<<endl;
	return output;
}

/*--------------------------------------------------------*/

istream &operator>>(istream &input, Complex &object)
{
	cout<<"Enter real, imaginary:"<<endl;
	input>>object.real;
	input>>object.imaginary;
	return input;
}


/*--------------------------------------------------------*/


int main()
{
	Complex x(3,4),y(3,4),z1,z2,z3,z4;
	cout<<"x=";
	x.print_complex();
	x.print_magnitude();
	cout<<"y=";
	y.print_complex();
	y.print_magnitude();
	
	// Complex Numbers  k & l are of Class type Complex
	
	Complex k(3,4),l(1,3),z6,z7,z8,z9,z10;
	
	cin >> k;  // Input two Complex numbers k and l  , where k = 3 + j4 and l = 4 + j5

	if (!cin || cin.fail())
	{
		// user didn't input a number
		cin.clear(); // reset failbit
		cerr << "ERROR Please Enter a Number";
		return 0;
	}

	cin >> l;

	if (!cin || cin.fail())
	{
		// user didn't input a number
		cin.clear(); // reset failbit
		cerr << "ERROR Please Enter a Number";
		return 0;
	}

	if(k==l) //define '==' operation for this line to work
	{cout<<"These 2 complex numbers are equal."<<endl;}

	if(k!=l) //define '!=' operation for this line to work
	{cout<<"These 2 complex numbers are not equal."<<endl;}

    if(k>l) //define '>' operation for this line to work
	{cout<<"k is bigger than l."<<endl;}

	if(k<l) //define '<' operation for this line to work
	{cout<<"k is smaller than l."<<endl;}

	z6=k+l; //define '+' operation for this line to work

	z7=k-l; //define '-' operation for this line to work

	z8=k*l; //define '*' operation for this line to work

	z9=k/l; //define '/' operation for this line to work*/
	
	cout << "z6=" << z6;
	cout << "z7=" << z7;
	cout << "z8=" << z8;
	cout << "z9=" << z9;
	cout << "k=" << k;
	cout << "l=" << l;

	return(0);
}