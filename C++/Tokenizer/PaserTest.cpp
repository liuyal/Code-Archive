
#include "parserClasses.h"
#include <iostream>
#include <fstream> 

#include "parserClasses.cpp"//I dont like to put it in a project

using namespace std;




int main() {
	ifstream sourceFile;
	TokenList tokens;
	Tokenizer tokenizer;

	//Read in a file line-by-line and tokenize each line
	sourceFile.open("test.vhd");
	if (!sourceFile.is_open())
	{
		cout << "Failed to open file" << endl;
		return 1;
	}

	while(!sourceFile.eof())
	{
		string lineA, lineB;

		getline(sourceFile, lineA);

		//while the current line ends with a line-continuation \
		//append the next line to the current line
		while(lineA.length() > 0 && lineA[lineA.length()-1] == '\\')
		{
			lineA.erase(lineA.length()-1, 1);
			getline(sourceFile, lineB);
			lineA += lineB;
		}

		tokenizer.setString(&lineA);

		while(!tokenizer.isComplete())
		{
			tokens.append(tokenizer.getNextToken());
		}
		//Re-insert newline that was removed by the getline function
		tokens.append("\n");
	}



   Token *b = tokens.getFirst();
	while(b)
	{
		cout << b->getStringRep() << " ";//  << endl; // remove endl for submission
		b = b->getNext();
	}



	cout << endl << "----------------------------------------------"<< endl<< endl;



	removeComments(tokens);




	/*Test your tokenization of the file by traversing the tokens list and printing out the tokens*/
	Token *t = tokens.getFirst();

	while(t)
	{
		cout << t->getStringRep() << " ";//  << endl; // remove endl for submission
		t = t->getNext();
	}

	return 0;
}
