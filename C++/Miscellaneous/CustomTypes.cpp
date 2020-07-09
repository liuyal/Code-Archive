#include<iostream>
using namespace std;

/*
Find the size of these user defined types
*/

//19)
class UserDefinedType19
{
public:
	char value;
	int max_length;
};

//20)
class UserDefinedType20
{
public:
	char value;
	long partb;
	float fraction;
	double long_fraction;
};

//21)
class UserDefinedType21
{
private:
	char value;
	long partb;
	float fraction;
	double long_fraction;
};

//22)
struct UserDefinedType22
{
	char value;
	long partb;
	float fraction;
	double long_fraction;
    uint8_t value_2;
	uint16_t value3;
};

//23)
struct UserDefinedType23
{
	char value;
	long partb;
	float fraction;
	double long_fraction;
	uint8_t value_2;
	uint16_t value3;
	UserDefinedType22 other;
};

//24)
union UserDefinedType24
{
	char value;
	long partb;
	float fraction;
	double long_fraction;
	uint8_t value_2;
	uint16_t value3;
};

//25)
union UserDefinedType25
{
	char value;
	long partb;
	float fraction;
	double long_fraction;
	uint8_t value_2;
	uint16_t value3;
	UserDefinedType22 other;
};

//26)
union UserDefinedType26
{
	UserDefinedType22 varA;
	UserDefinedType23 varB;
};


// int main() produce the output of different types in c++ on a 64 bit OS
//
// Pointer (ie. int*) size depends on the OS, 32 bit = 4 bytes, 64 bit = 8 bytes
// Size of classes UserDefinedType depend of the size and order of the types in the classes
//
//
// For UserDefinedType19 byte ailgment
//
//   0   1   2   3   4   5   6   7
// +---+- - - - - -+---------------+
// | a | (unused)  | b             |
// +---+- - - - - -+---------------+
// 4 byte is allcated for a eventhough char is 1 byte so there are 3 unused bytes
// b is used by int since int is 4 bytes
//
//
//type void is empty it has size 0 but in this compiler is displayed as 1 byte

// Points on VS is half of ones on CB?


int main()
{
       cout << "short = " << sizeof(short) << " bytes" <<endl; //                                       1)
        cout << "int = " << sizeof(int) << " bytes" <<endl; //                                          2)
         cout << "long = " << sizeof(long) << " bytes" <<endl; //                                       3)
          cout << "float = " << sizeof(float) << " bytes" <<endl; //                                    4)
           cout << "double = " << sizeof(double) << " bytes" <<endl; //                                 5)

            cout << "uint8 = " << sizeof(uint8_t) <<" bytes" <<endl; //                                 6)
             cout << "uint16 = "  << sizeof(uint16_t) << " bytes" << endl; //                           7)
              cout << "char = " << sizeof(char) << " bytes" << endl; //                                 8)
               cout << "void = " << sizeof(void) << " bytes" << endl; //                                9)
                cout << "short* = " << sizeof(short*) << " bytes" << endl; //                          10)

                 cout << "int* = " << sizeof(int*) << " bytes" << endl; //                             11)
                  cout << "long* = " << sizeof(long*) << " bytes" << endl; //                          12)
                   cout << "float* = " << sizeof(float*) << " bytes" << endl; //                       13)
                    cout << "double* = " << sizeof(double*) << " bytes" << endl; //                    14)
                     cout << "uin8* = " << sizeof(uint8_t*) << " bytes" << endl; //                    15)

                      cout << "uint16* = " << sizeof(uint16_t) << " bytes" << endl; //                 16)
                       cout << "char* = " << sizeof(char*) << " bytes" << endl; //                     17)
                        cout << "void* = " << sizeof(void*) << " bytes" << endl; //                    18)

                         cout << "19 = " << sizeof(UserDefinedType19) << " bytes" << endl; //          19)
                          cout << "20 = " << sizeof(UserDefinedType20) << " bytes" << endl; //         20)
                           cout << "21 = " << sizeof(UserDefinedType21) << " bytes" << endl; //        21)
                            cout << "22 = " << sizeof(UserDefinedType22) << " bytes" << endl; //       22)
                             cout << "23 = " << sizeof(UserDefinedType23) << " bytes" << endl; //      23)

                              cout << "24 = " << sizeof(UserDefinedType24) << " bytes" << endl; //     24)
                               cout << "25 = " << sizeof(UserDefinedType25) << " bytes" << endl; //    25)
                                cout << "26 = " << sizeof(UserDefinedType26) << " bytes" << endl; //   26)


return 0;
}
