//Use only the following three libraries:
#include "parserClasses.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <sstream>

using namespace std;

int error_end_if(const TokenList &tokenList, const TokenList &tokenList2);
int error_then(const TokenList &tokenList, const TokenList &tokenList2);
int error_else(const TokenList &tokenList, const TokenList &tokenList2);

int error_type(const TokenList &tokenList, const TokenList &tokenList2);
int error_width(const TokenList &tokenList, const TokenList &tokenList2);
int error_head_LIB(const TokenList &tokenList, const TokenList &tokenList2);

int error_colon(const TokenList &tokenList, const TokenList &tokenList2);
int error_semi_col(const TokenList &tokenList, const TokenList &tokenList2);
int error_bracket(const TokenList &tokenList, const TokenList &tokenList2);


//Example Test code for interacting with your Token, TokenList, and Tokenizer classes
//Add your own code to further test the operation of your Token, TokenList, and Tokenizer classes
int main() {
	ifstream sourceFile;
	TokenList tokens;
	TokenList lines;
    cout <<"run" << endl;
	//Lists for types of tokens
	TokenList operatorTokens;
	TokenList identifierTokens;
	TokenList literalTokens;
	TokenList commentBodyTokens;
	TokenList otherTokens;

	Tokenizer tokenizer;

	int Num = 0;
	string Result;
	//Read in a file line-by-line and tokenize each line
	sourceFile.open("test.vhd");
	if (!sourceFile.is_open())
	{
		cout << "Failed to open file" << endl;
		return 1;
	}

	while (!sourceFile.eof())
	{
		string line;
		getline(sourceFile, line);

		Num++;
		ostringstream convert;
		convert << Num;
		Result = convert.str();

		tokenizer.setString(&line);
		while (!tokenizer.isComplete())
		{
			lines.append(Result);
			tokens.append(tokenizer.getNextToken());
		}
	}

    /*Test your tokenization of the file by traversing the tokens list and printing out the tokens*/

	cout << "[--------------------MASTER LIST----------------------]" << endl;

	Token *m = tokens.getFirst();
	Token *m2 = lines.getFirst();

	int Num_tokens = 1;

	while (m && m2)
	{
		cout << Num_tokens << "  [" << m2->getStringRep() << "] ";
		cout << " [" << m->getStringRep() << "] " << endl;

		m = m->getNext();
		m2 = m2->getNext();

		Num_tokens++;
	}

	cout << endl;

   /* For your testing purposes only*/

	cout << "[--------------------- findAndSetTokenDetails -----------------------]" << endl;

	string temp1;
	int wide = 0;

	Token *w = tokens.getFirst();
	while (w)
	{
		tokens.findAndSetTokenDetails(w);
		string type;
		if (w->getTokenType() == 0)
		{
			type = "ID";
			identifierTokens.append(w->getStringRep());
		}
		else if (w->getTokenType() == 1)
		{
			type = "Op";
			operatorTokens.append(w->getStringRep());
		}
		else if (w->getTokenType() == 2)
		{
			type = "Lt";
			literalTokens.append(w->getStringRep());
		}
		else if (w->getTokenType() == 3)
		{
			type = "Com";
			commentBodyTokens.append(w->getStringRep());
		}
		else if (w->getTokenType() == 4)
		{
			type = "OTH";
			otherTokens.append(w->getStringRep());
		}

		if (w->getTokenDetails() == NULL)
		{
			 temp1 = "NA";
			 wide = 0;
		}
		else
		{
			 temp1 = w->getTokenDetails()->type;
			 wide = w->getTokenDetails()->width;
		}

		cout << "[" << w->getStringRep() << "]   " << endl;
		cout << "            Type: " << type <<
		setw(10) << left << "  Details: " << temp1 << "  " << wide <<
		setw(20) << right << "Key Word: " << w->isKeyword();

		cout  << endl;
		w = w->getNext();
	}



	cout << endl << "[-------------------- findAllConditionalExpressions ---------------------]" << endl;

	TokenList *Conditional = new TokenList();
	Conditional = findAllConditionalExpressions(tokens);

	int conditional_numbers = 1;

	Token *C = Conditional->getFirst();

	while (C)
	{
		if (C->getStringRep() == "\n")
		{
			conditional_numbers++;
		}
		cout << C->getStringRep();
		C = C->getNext();
	}

	cout << endl;

	cout << endl << "[-------------------------- ERROR CHECK ----------------------------]" << endl << endl;

	cout << "verbose:" << endl << endl;

	int end_if = error_end_if(tokens, lines);
	int then = error_then(tokens, lines);
	int else_ = error_else(tokens, lines);

	int type = error_type(tokens, lines);
	int wides = error_width(tokens, lines);
	int headL = error_head_LIB(tokens, lines);

	int colon = error_colon(tokens, lines);
	int semi_col = error_semi_col(tokens, lines);
	int brac = error_bracket(tokens, lines);


	cout << endl << "non-verbose:" << endl << endl;

	cout << "Number of Tokens: " << Num_tokens << endl;
	cout << "Number of Conditional Expressions: " << conditional_numbers-1 << endl;

	cout << "Number of Missing \"end if\": " << end_if << endl;
	cout << "Number of Missing \"then\": " << then << endl;
	cout << "Number of Missing \"else\": " << else_ << endl;

	cout << "Number of Type mismatch: " << type << endl;
	cout << "Number of Width mismatch: " << wides << endl;
	cout << "Missing head Library: " << headL << endl;

	cout << "Number of Missing colon: " << colon << endl;
	cout << "Number of Missing semi-colon: " << semi_col << endl;
	cout << "Number of Missing bracket: " << brac << endl;

	return 0;
}


//check for missing endif after if
int error_end_if(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_endif = 0;
	int if_count = 0;
	int end_count = 0;

	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
		//Missing end if for if +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		if (current->getStringRep() == "if" && current->getPrev()->getStringRep() != "end")
		{
			for (temp = current->getNext(); temp != NULL; temp = temp->getNext())
			{
				if (temp->getStringRep() == "if" && temp->getPrev()->getStringRep() == "end")
				{
					break;
				}
				if (temp->getStringRep() == "if" && temp->getPrev()->getStringRep() != "end")
				{
					cout << "ERROR missing \"end if\" on line: " << numbers->getStringRep() << endl;
					miss_endif++;
					break;
				}
				if (temp->getNext() == NULL)
				{
					cout << "ERROR missing \"end if\" on line: " << numbers->getStringRep() << endl;
					miss_endif++;
					break;
				}
			}
		}
        //count all if
		if (current->getStringRep()=="if" && current->getPrev()->getStringRep() != "end")
		{
		if_count++;
		}
		//count all end if
		if (current->getStringRep() == "end" && current->getNext()->getStringRep() == "if")
        {
         end_count++;
        }

		numbers = numbers->getNext();
		current = current->getNext();
	}
    // check differnec
	int mis_end_if_count = abs(if_count-end_count);

	return mis_end_if_count;
}

// checks for missing then after if or elsif
int error_then(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_then = 0;

	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
	//finds if
		if (current->getStringRep() == "if" && current->getPrev() != NULL &&
			current->getPrev()->getStringRep() != "end")
		{
			for (temp = current; temp != NULL; temp = temp->getNext())
			{
			//not found then before elsif or else or end
				if (temp->getNext()->getStringRep() == "elsif" || temp->getStringRep() == "else" || temp->getStringRep() == "end")
				{
					cout << "ERROR missing \"then\" on line: " << numbers->getStringRep() << endl;
					miss_then++;
					break;
				}
				//found then
				else if (temp->getStringRep() == "then")
				{
					break;
				}
			}
		}

        //checks for elsif and then after
		if (current->getStringRep() == "elsif")
		{
			for (temp = current->getNext(); temp != NULL; temp = temp->getNext())
			{
			//found then
				if (temp->getStringRep() == "then")
				{
					break;
				}
				//found elsif or else or end before then
				else if (temp->getStringRep() == "elsif" || temp->getStringRep() == "else" || temp->getStringRep() == "end")
				{
					cout << "ERROR missing \"then\" on line: " << numbers->getStringRep() << endl;
					miss_then++;
					break;
				}
			}
		}
		numbers = numbers->getNext();
		current = current->getNext();
	}
	return miss_then;
}
//check for missing else after when
int error_else(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_else = 0;
	Token *current = new Token;
	Token *numbers = new Token;

	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{   //detect when
		if (current->getStringRep() == "when")
		{
			for (temp = current->getNext(); temp != NULL; temp = temp->getNext())
			{   //finds else
				if (temp->getStringRep() == "else" || temp->getStringRep() == ";")
				{
					break;
				}
				//not found else before when
				else if (temp->getStringRep() == "when" || temp->getNext() == NULL)
				{
					cout << "ERROR missing \"else\" on line: " << numbers->getStringRep() << endl;
					miss_else++;
					break;
				}

			}
		}
		numbers = numbers->getNext();
		current = current->getNext();
	}

	return miss_else;
}

//check for mismatch type
int error_type(const TokenList &tokenList, const TokenList &tokenList2)
{
	int mis_type = 0;

	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
	// find a operator and look at surrounding tokens
		if (current->getTokenType() == T_Identifier && current->getTokenDetails() != NULL &&
			current->getNext()->getTokenType() == T_Operator && current->getNext()->getNext()->getTokenDetails() != NULL &&
			current->getNext()->getNext()->getTokenType() != T_Literal)
		{
			string temp_typeA = current->getTokenDetails()->type;
			string temp_typeB = current->getNext()->getNext()->getTokenDetails()->type;
            //if details of type are not the same
			if (temp_typeA != temp_typeB)
			{
				cout << "ERROR mismatch type on line: " << numbers->getStringRep() << endl;
				mis_type++;
			}
		}
		numbers = numbers->getNext();
		current = current->getNext();
	}
	return mis_type;
}
//checks for width mismatch
int error_width(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_width = 0;
	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
	// find a operator and look at surrounding tokens one has to be literal
		if (current->getTokenType() == T_Identifier && current->getTokenDetails() != NULL &&
			current->getNext()->getTokenType() == T_Operator && current->getNext()->getNext()->getTokenDetails() != NULL &&
			current->getNext()->getNext()->getTokenType() != T_Literal)
		{
			int temp_widA = current->getTokenDetails()->width;
			int temp_wideB = current->getNext()->getNext()->getTokenDetails()->width;
            //finds width missmatch
			if (temp_widA != temp_wideB)
			{
				cout << "ERROR mismatch width on line: " << numbers->getStringRep() << endl;
				miss_width++;
			}
		}

        //find a operator and look at surrounding tokens one has to be literal
		if (current->getTokenType() == T_Identifier && current->getTokenDetails() != NULL &&
			current->getNext()->getTokenType() == T_Operator && current->getNext()->getNext()->getTokenDetails() != NULL &&
			current->getNext()->getNext()->getTokenType() == T_Literal)
		{
			int temp_widA = current->getTokenDetails()->width;
			int temp_wideB = current->getNext()->getNext()->getTokenDetails()->width;
			// //finds width missmatch
			if (temp_widA != temp_wideB)
			{
				cout << "ERROR mismatch width on line: " << numbers->getStringRep() << endl;
				miss_width++;
			}
		}
		numbers = numbers->getNext();
		current = current->getNext();
	}
	return miss_width;
}
//checks for head library
int error_head_LIB(const TokenList &tokenList, const TokenList &tokenList2)
{
	Token *current = new Token;
	Token *numbers = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();
    //file does not start with library
	if (current->getPrev() == NULL && current->getStringRep() != "library")
	{
		cout << "Missing Head Library" << endl;
		return 1;
	}
	else
	{
		return 0;
	}
}

//find missing colons betweed id and type(std_logic...etc)
int error_colon(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_colon = 0;
	Token *current = new Token;
	Token *numbers = new Token;

	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
		//need adding ?
		//finds : before out and in
		if (current->getStringRep() == "out" || current->getStringRep() == "in")
		{
			if (current->getPrev() !=NULL && current->getPrev()->getStringRep() != ":")
			{
				cout << "ERROR missing colon on line: " << numbers->getStringRep() << endl;
				miss_colon++;
			}

		}
        //find : after signal varialbe and constant
		if (current->getStringRep() == "signal" || current->getStringRep() == "variable" || current->getStringRep() == "constant")
		{
			if (current->getNext()->getNext()->getStringRep() != ":")
			{
				cout << "ERROR missing colon on line: " << numbers->getStringRep() << endl;
				miss_colon++;

			}
		}

		numbers = numbers->getNext();
		current = current->getNext();
	}
	return miss_colon;
}


//need adding
//check for missing semi col
int error_semi_col(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_semi_col = 0;
	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();

	while (current && numbers)
	{
        // missing semi colon at end of file
		if (current->getNext() == NULL && current->getStringRep() != ";" && current->getTokenType() != 3)
		{
			cout << "ERROR missing semi-colon on line: " << numbers->getStringRep() << endl;
			miss_semi_col++;
		}
		// missing semi colon at before after end if
		if (current->getStringRep() == "end" && current->getNext()->getNext() != NULL &&
			current->getNext()->getStringRep() == "if" && current->getNext()->getNext()->getStringRep() != ";")
		{
			cout << "ERROR missing semi-colon on line: " << numbers->getStringRep() << endl;
			miss_semi_col++;
		}
		// missing semi colon at before after end if
		if (current->getPrev() != NULL && current->getStringRep() == "end" && current->getNext()->getStringRep() != "if" &&
			current->getPrev()->getStringRep() != ";")
		{
			cout << "ERROR missing semi-colon on line: " << numbers->getStringRep() << endl;
			miss_semi_col++;
		}
		// missing semi colon at before after elsiof and else
		if (current->getPrev() != NULL && (current->getStringRep() == "elsif" || current->getStringRep() == "else") &&
			current->getPrev()->getStringRep() != ";")
		{
			cout << "ERROR missing semi-colon on line: " << numbers->getPrev()->getStringRep() << endl;
			miss_semi_col++;
		}
        // missing semi colon at before signal and varriabel
		if (current->getStringRep() == "signal" || current->getStringRep() == "variable")
		{
			if (current->getPrev() != NULL && current->getPrev()->getStringRep() != "is" &&
				current->getPrev()->getStringRep() != ";")
			{
				cout << "ERROR missing semi-colon on line: " << numbers->getPrev()->getStringRep() << endl;
				miss_semi_col++;
			}

		}

		if (current->getStringRep() == "begin" && current->getPrev() != NULL && current->getPrev()->getStringRep() != ";")
		{
			cout << "ERROR missing semi-colon on line: " << numbers->getPrev()->getStringRep() << endl;
			miss_semi_col++;
		}

		numbers = numbers->getNext();
		current = current->getNext();
	}

	return miss_semi_col;
}
//check for missing bracket
int error_bracket(const TokenList &tokenList, const TokenList &tokenList2)
{
	int miss_brac = 0;
	Token *current = new Token;
	Token *numbers = new Token;
	Token *temp = new Token;

	current = tokenList.getFirst();
	numbers = tokenList2.getFirst();
	while (current && numbers)
	{
	//if ( appears twice in a role
		if (current->getStringRep() == "(" && current->getPrev() != NULL && current->getPrev()->getStringRep() != "port")
		{
			for (temp = current->getNext(); temp != NULL; temp = temp->getNext())
			{
				if (temp->getStringRep() == ")")
				{
					break;
				}
				if (temp->getStringRep() == "(" || temp->getStringRep() == ";")
				{
					cout << "ERROR missing bracket on line: " << numbers->getStringRep() << endl;
					miss_brac++;
					break;
				}

			}
		}
		//if ) appears twice in a role
		if (current->getStringRep() == ")" && current->getPrev() != NULL)
		{
			for (temp = current->getPrev(); temp != NULL; temp = temp->getPrev())
			{
				if (temp->getStringRep() == "(")
				{
					break;
				}
				else if ((temp->getStringRep() == ")" && temp->getNext()->getNext()->getStringRep() != ";") ||
					temp->getStringRep() == ";")
				{
					cout << "ERROR missing bracket on line: " << numbers->getStringRep() << endl;
					miss_brac++;
					break;
				}

			}
		}

		numbers = numbers->getNext();
		current = current->getNext();
	}

	return miss_brac;
}
