
//Use only the following libraries:
#include "parserClasses.h"
#include <string>
//#include <iostream>//////remove


/////////////////////////////////////////////////////////////////////////////////////////
//****Token class function definitions*****
/////////////////////////////////////////////////////////////////////////////////////////

//Set's the tokenDetails given a string type and optional vector width
//Allocates tokenDetails if it doesn't already exist
//void Token::setTokenDetails(const string &type, int width = 0)
//set details type and width of avabile tokens
void Token::setTokenDetails(const string &type, int width)
{
	if (details == NULL)
	{
		details = new tokenDetails;
	}
	details->type = type;
	details->width = width;
}

//Creat New token with operator =
void Token::operator = (const Token& token)
{
	next = token.getNext();
	prev = token.getPrev();
	details = token.getTokenDetails();

    //check for details first
	if (details == NULL)
	{
		details = new tokenDetails;
		details->type = token.details->type;
		details->width = token.details->width;
	}
	else
	{
        //if details not set
		details = token.getTokenDetails();
	}

	stringRep = token.getStringRep();
	_isKeyword = token.isKeyword();
	type = token.getTokenType();
}


/////////////////////////////////////////////////////////////////////////////////////////
//****TokenList class function definitions******
// function implementations for append have been provided and do not need to be modified
/////////////////////////////////////////////////////////////////////////////////////////

//Creates a new token for the string input, str
//Appends this new token to the TokenList
//On return from the function, it will be the last token in the list
void TokenList::append(const string &str)
{
	Token *token = new Token(str);
	append(token);
}

//Appends the token to the TokenList if not null
//On return from the function, it will be the last token in the list
void TokenList::append(Token *token)
{
	if (!head)
	{
		head = token;
		tail = token;
	}
	else
	{
		tail->setNext(token);
		token->setPrev(tail);
		tail = token;
	}
}


//input token and find nearby tokens for properties
void TokenList::findAndSetTokenDetails(Token *token)
{
	Token *current = token;
	Token *iter;
	Token *iter2;

	string N = token->getStringRep();
	//string temp for user defined types
	string cus_type, cus_iter,cus_type2 = "\0";
	string cus_type3;
	string _unsigned, _signed, _std_vector, _std, _int, _real = "\0";

	long long first;
	long long last;
	long long width;

    //size of arryas holding keywords,ids, and operators
	size_t KW_size = KW_size = sizeof(Keywords) / sizeof(Keywords[0]); //Keywords array size
	size_t ID_size = ID_size = sizeof(Identifiers) / sizeof(Identifiers[0]); //Identifier array size
	size_t OP_size = OP_size = sizeof(Operators) / sizeof(Operators[0]); // Operator array size


	//initialize TokenType to T_Other
	if (token->type != T_Identifier)
	{
		token->setTokenType(T_Other);
	}

	//[--------------------------------------------Keywords--------------------------------------------------]
	for (size_t i = 0; i < KW_size; i++)
	{
		if (N == Keywords[i])
		{
			token->setKeyword();
		}
	}//Keywords

	 //[--------------------------------------------boolean--------------------------------------------------]
	if (N == "true" || N == "false")
	{
		token->setTokenDetails("boolean", 0);
		token->setTokenType(T_Identifier);
	}//boolean

	//[--------------------------------------------Identifier--------------------------------------------------]
	for (int i = 0; i < ID_size; i++)
	{
		if (N == Identifiers[i])
		{
			token->setTokenType(T_Identifier);
			return;
		}
	}

	//Entity*************************************************************************
	if (token->getPrev() != NULL && token->getPrev()->getStringRep() == "entity" && token->getNext()->getStringRep() == "is")
	{
		token->setTokenType(T_Identifier);
		return;
	}
	else if (token->getPrev() != NULL && token->getPrev()->getPrev() != NULL && token->getPrev()->getStringRep() == "entity" && token->getPrev()->getPrev()->getStringRep() == "end")
	{
		token->setTokenType(T_Identifier);
		return;
	}
	else if (token->getPrev() != NULL && token->getPrev()->getStringRep() == "end")
	{
		token->setTokenType(T_Identifier);
		return;
	}
	//Architecutre*************************************************************************
	if (token->getPrev() != NULL && token->getPrev()->getStringRep() == "architecture" && token->getNext()->getStringRep() == "of")
	{
		token->setTokenType(T_Identifier);
		return;
	}
	if (token->getPrev() != NULL && token->getPrev()->getStringRep() == "of" && token->getNext()->getStringRep() == "is")
	{
		token->setTokenType(T_Identifier);
		return;
	}

	//Input output *************************************************************************
	if (token->next != NULL && token->next->next != NULL && token->next->next->next != NULL &&
		(token->next->stringRep == ":") &&
		(token->next->next->stringRep == "out" || token->next->next->stringRep == "in"))
	{
		token->setTokenType(T_Identifier);
		//std_logic input/output
		if (token->next->next->next->stringRep == "std_logic")
		{
			token->setTokenDetails("std_logic", 1);
			_std = token->stringRep;
			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_std != "\0" && iter->stringRep == _std) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("std_logic", 1);
				}
			}
			return;
		}

		//std_logic_vector input/output
		else if (token->next->next->next->stringRep == "std_logic_vector")
		{
			first = atoi(token->next->next->next->next->next->stringRep.c_str());
			last = atoi(token->next->next->next->next->next->next->next->stringRep.c_str());
			if (last == 0)
			{width = abs(first - last) + 1;}
			else{width = abs(first - last);}

			token->setTokenDetails("std_logic_vector", width);

			_std = token->stringRep;
			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_std != "\0" && iter->stringRep == _std) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("std_logic_vector", width);
				}
			}
			return;
		}

		//signed width == 1 input/output
		else if (token->next->next->next->stringRep == "signed" && token->next->next->next->next->stringRep == ";")
		{
			token->setTokenDetails("signed", 1);
			_signed = token->stringRep;

			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_signed != "\0" && iter->stringRep == _signed) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("signed", 1);
				}
			}
			return;
		}
		//signed vector input/output
		else if (token->next->next->next->stringRep == "signed" && token->next->next->next->next->stringRep != ";")
		{
			first = atoi(token->next->next->next->next->next->stringRep.c_str());
			last = atoi(token->next->next->next->next->next->next->next->stringRep.c_str());
			if (last == 0)
			{width = abs(first - last) + 1;}
			else { width = abs(first - last); }
			token->setTokenDetails("signed", width);
			_signed = token->stringRep;

			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_signed != "\0" && iter->stringRep == _signed) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("signed", width);
				}
			}
			return;
		}

		//unsigned widthre == 1 input/output
		else if (token->next->next->next->stringRep == "unsigned" && token->next->next->next->next->stringRep == ";")
		{
			token->setTokenDetails("unsigned", 1);
			_unsigned = token->stringRep;

			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_unsigned != "\0" && iter->stringRep == _unsigned) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("unsigned", 1);
				}
			}
			return;
		}
		//unsigned vector input/output
		else if (token->next->next->next->stringRep == "unsigned" && token->next->next->next->next->stringRep != ";")
		{
			first = atoi(token->next->next->next->next->next->stringRep.c_str());
			last = atoi(token->next->next->next->next->next->next->next->stringRep.c_str());
			if (last == 0)
			{width = abs(first - last) + 1;}
			else { width = abs(first - last); }
			token->setTokenDetails("unsigned", width);

			_unsigned = token->stringRep;
			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_unsigned != "\0" && iter->stringRep == _unsigned) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("unsigned", width);
				}
			}
			return;
		}

	}//Input output end


	//SINGal or Variable width == 1 *************************************************************************
	//std_logic
	if (token->prev != NULL &&
	   (token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		token->next->next->stringRep == "std_logic")
	{
		token->setTokenType(T_Identifier);
		token->setTokenDetails("std_logic", 1);

		_std = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_std != "\0" && iter->stringRep == _std) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("std_logic", 1);
			}
		}
		return;
	}
	//signed
	 if (token->prev != NULL &&
		(token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		 token->next->next->stringRep == "signed" && token->next->next->next->stringRep == ";")
	{
		token->setTokenType(T_Identifier);
		token->setTokenDetails("signed", 1);

		_signed = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_signed != "\0" && iter->stringRep == _signed) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("signed", 1);
			}
		}
		return;
	}
	 //unsigned
	if (token->prev != NULL &&
	   (token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		token->next->next->stringRep == "unsigned" && token->next->next->next->stringRep == ";")
	{
		token->setTokenType(T_Identifier);
		token->setTokenDetails("unsigned", 1);

		_unsigned = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_unsigned != "\0" && iter->stringRep == _unsigned) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("unsigned", 1);
			}
		}
		return;
	}
	//width of 1 end



	//SINGal or Variable Vectors*************************************************************************
	//STD_LOGIC_VECTOR
	if (token->prev != NULL &&
	   (token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		token->next->next->stringRep == "std_logic_vector")
	{
        //check width by looking at (7 downto 0)
		first = atoi(token->next->next->next->next->stringRep.c_str());
		last = atoi(token->next->next->next->next->next->next->stringRep.c_str());

		width = abs(first - last) + 1;

		token->setTokenType(T_Identifier);
		token->setTokenDetails("std_logic_vector", width);

		_std_vector = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_std_vector != "\0" && iter->stringRep == _std_vector) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("std_logic_vector", width);
			}
		}
		return;
	}//STD_LOGIC_VECTOR end

	//Signed VECTOR
	if (token->prev != NULL &&
	   (token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		token->next->next->stringRep == "signed" && token->next->next->next->stringRep != ";")
	{
        //check width by looking at (7 downto 0)
		first = atoi(token->next->next->next->next->stringRep.c_str());
		last = atoi(token->next->next->next->next->next->next->stringRep.c_str());

		width = abs(first - last) + 1;

		token->setTokenType(T_Identifier);
		token->setTokenDetails("signed", width);

		_signed = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_signed != "\0" && iter->stringRep == _signed) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("signed", width);
			}
		}
		return;
	}//signed VECTOR end

	 //unsigned vector
	if (token->prev != NULL &&
	   (token->prev->stringRep == "signal" || token->prev->stringRep == "variable") &&
		token->next->next->stringRep == "unsigned" && token->next->next->next->stringRep != ";")

	{   //check width by looking at (7 downto 0)
		first = atoi(token->next->next->next->next->stringRep.c_str());
		last = atoi(token->next->next->next->next->next->next->stringRep.c_str());

        width = abs(first - last) + 1;

		token->setTokenType(T_Identifier);
		token->setTokenDetails("unsigned", width);

		_unsigned = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (_unsigned != "\0" && iter->stringRep == _unsigned) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails("unsigned", width);
			}
		}
		return;
	}//unsigned VECTOR end


	 //[--------------------------------------------Operators--------------------------------------------------]
	for (size_t i = 0; i < OP_size; i++)
	{
		if (token->getStringRep() == Operators[i])
		{
			token->setTokenType(T_Operator);
			return;
		}
	}//Operators



	//[--------------------------------------------Literals--------------------------------------------------]

	//std_logic type
	//Not lowercased for std_logics
	if (N == "'1'" || N == "'0'" || N == "'Z'" || N == "'U'" ||
		N == "'X'" || N == "'W'" || N == "'L'" || N == "'H'")
	{
		token->setTokenType(T_Literal);
		token->setTokenDetails("std_logic", 1);
		return;
	}

	//integer check
	if (N.find("0") == 0 || N.find("1") == 0 || N.find("2") == 0 || N.find("3") == 0 ||
		N.find("4") == 0 || N.find("5") == 0 || N.find("6") == 0 || N.find("7") == 0 ||
		N.find("8") == 0 || N.find("9") == 0)
	{
		token->setTokenType(T_Literal);
		token->setTokenDetails("integer", 0);
		return;
	}

	//binary
	if (N.find_first_of("\"") == 0)
	{
		int next = N.find("\"", 1);
		token->setTokenType(T_Literal);
		token->setTokenDetails("binary", next - 1); //width of a binary
		return;
	}
	if (N.find_first_of("b") == 0 && N.find_first_of("\"") == 1)
	{
		int next = N.find_last_of("\"");
		token->setTokenType(T_Literal);
		token->setTokenDetails("binary", next-2);
		return;
	}
	//oct decimal ckeck
	if (N.find_first_of("o") == 0 && N.find_first_of("\"") == 1)
	{
		int next = N.find_last_of("\"");
		token->setTokenType(T_Literal);
		token->setTokenDetails("octal", (next-2) * 3 );
		return;
	}
	//hexadecimal check
	if (N.find("x") == 0 && N.find("\"") == 1)
	{
		int next = N.find_last_of("\"");
		token->setTokenType(T_Literal);
		token->setTokenDetails("hexidecimal", (next - 2) * 4);
		return;
	}

	 //[--------------------------------------------Comment--------------------------------------------------]
	if (current != head && current->getPrev()->getStringRep() == "--")
	{
		token->setTokenType(T_CommentBody);
		return;
	}//Comment


	 //[--------------------------------------------Other--------------------------------------------------]
	if (current->getStringRep() == ":" || current->getStringRep() == ";" ||
		current->getStringRep() == "--" || current->getStringRep() == "(" ||
		current->getStringRep() == ")" || current->getStringRep() == "," ||
		current->getStringRep() == ".")
	{
		token->setTokenType(T_Other);
		return;
	}//Other


	//Bonus
	//[--------------------------------------------UserDefine--------------------------------------------------]
	if (token->prev != NULL && current->prev->stringRep == "type" && current->next->stringRep == "is")
	{
		cus_type3 = current->getStringRep();
		cus_type = current->stringRep;
		token->setTokenType(T_Identifier);
		token->setTokenDetails(cus_type, 0);

		cus_type2 = token->stringRep;
		for (iter = token; iter != NULL; iter = iter->next)
		{
			if (cus_type2 != "\0" && iter->stringRep == cus_type2) //identifier is used again later in the file
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails(cus_type, 0);
			}
		}
        //find all user defined identifiers and set type to user defined type
		for (iter = token; iter != NULL; iter = iter->next)
		{
			//If id is bewtown "(" and "," ie (m,
			if (iter->prev->stringRep == "(" && iter->next->stringRep == ",")
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails(cus_type,0);

				cus_iter = iter->stringRep;
				iter2 = token;
				//Check for same id in later file
				while (iter2->getNext() != NULL)
				{
					if (iter2->stringRep == cus_iter)
					{
						iter2->setTokenType(T_Identifier);
						iter2->setTokenDetails(cus_type, 0);
					}
					iter2 = iter2->getNext();
				}
			}
			//If id is bewtown "," and "," ie ,m,
			else if (iter->prev->stringRep == "," && iter->next->stringRep == ",")
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails(cus_type, 0);

				cus_iter = iter->stringRep;
				iter2 = token;
				//Check for same id in later file
				while (iter2->getNext() != NULL)
				{
					if (iter2->stringRep == cus_iter)
					{
						iter2->setTokenType(T_Identifier);
						iter2->setTokenDetails(cus_type, 0);
					}
					iter2 = iter2->getNext();
				}

			}
			//If id is bewtown "," and ")" ie ,m)
			else if (iter->prev->stringRep == "," && iter->next->stringRep == ")")
			{
				iter->setTokenType(T_Identifier);
				iter->setTokenDetails(cus_type, 0);

				cus_iter = iter->stringRep;
				iter2 = token;
				//Check for same id in later file
				while (iter2->getNext() != NULL)
				{
					if (iter2->stringRep == cus_iter)
					{
						iter2->setTokenType(T_Identifier);
						iter2->setTokenDetails(cus_type, 0);
					}
					iter2 = iter2->getNext();
				}
			}
			//End of type define by user
			if (iter->stringRep == "signal" || iter->stringRep == ";")
			{
				break;
			}

		}

	}

	//Constant
	if (token->prev != NULL && current->getPrev()->getStringRep() == "constant")
	{
		if (current->next->next->stringRep == "integer")
		{
			current->setTokenType(T_Identifier);
			current->setTokenDetails("integer", 0);
			_int = token->stringRep;
			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_int != "\0" && iter->stringRep == _int) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("integer", 0);
				}
			}
			return;
		}
		else if (current->next->next->stringRep == "real")
		{
			current->setTokenType(T_Identifier);
			current->setTokenDetails("real", 0);
			_real = token->stringRep;
			for (iter = token; iter != NULL; iter = iter->next)
			{
				if (_real != "\0" && iter->stringRep == _real) //identifier is used again later in the file
				{
					iter->setTokenType(T_Identifier);
					iter->setTokenDetails("real", 0);
				}
			}
			return;
		}

	}

	return;
} // end of setIdentifierValue


////////////////////////////////////////////////////////////////////
//Complete the implementation of the following member functions:
//****Tokenizer class function definitions******
////////////////////////////////////////////////////////////////////

//Computes a new tokenLength for the next token
//Modifies: size_t tokenLength, and bool complete
//(Optionally): may modify offset
//Does NOT modify any other member variable of Tokenizer
void Tokenizer::prepareNextToken()
{

	if (str->length() == 0)
    //Empty string is detected
	{
		complete = true; //complete
	}

    //trim white spaces
	if (!complete && !comment)
	{
		TWS();
	}

	if (!complete)
	{
		//Initialize variables
		int strLength = str->length();
		int i = offset;
		bool found = false;//find tokens for each case

		if (comment)//Comment case
		{
			tokenLength = strLength - offset;
			//Everything after '--' is a token
		}

		else
		{
			while (i < strLength && !found)
			{
				switch (str->at(i))
				{

				//Case of space and a tab
				case ' ':
				case '\t':
					tokenLength = i - offset;
					if (tokenLength == 0)
					{
						if (i == strLength)
						{
							complete = true;
							found = true;
						}
						else
						{
							offset++;
							i++;
							found = false;
						}
					}
					found = true;
					break;


				case '-':
					tokenLength = i - offset;
					if ((i < strLength - 1) && (str->at(i + 1) == '-') && (tokenLength == 0))//Detect '--'
					{
						tokenLength = 2;
					}
					if (!comment && tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;


				case '=':
					tokenLength = i - offset;
					if ((i < strLength - 1) && (str->at(i + 1) == '>') && (tokenLength == 0))//Detect '=>'
					{
						tokenLength = 2; //Length of '=>'
					}
					else if (tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;


				case '<':
					tokenLength = i - offset;
					if ( (i < strLength - 1) && (str->at(i + 1) == '=') && (tokenLength == 0))//Detect '<='
					{
						tokenLength = 2; //Length of '<='
					}
					if ((i < strLength - 1) && (str->at(i + 1) == '>') && (tokenLength == 0))//Detect '<>'
					{
						tokenLength = 2; //Length of '<>'
					}
					else if (tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;


				case '/':
				case '>':
				case ':':
					tokenLength = i - offset;
					if ((i < strLength - 1) && (str->at(i + 1) == '=') && (tokenLength == 0))//Detect '/=','>=','=='
					{
						tokenLength = 2;
					}
					else if (tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;


				case '*':
					tokenLength = i - offset;
					if ((i < strLength - 1) && (str->at(i + 1) == '*') && (tokenLength == 0))//Detect '**'
					{
						tokenLength = 2; //Length of '**'
					}
					else if (tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;


				case '"':
					while (i < strLength - 1 && !(str->at(i) != '--' && str->at(i + 1) == '"'))
					{
						i++;
					}
					tokenLength = i + 2 - offset;
					found = true;
					break;


				case '\'':
					if ((i < strLength - 1) && (str->at(i + 2) != '\'') && (tokenLength == 0))
					{
                    tokenLength = 1;
                    offset = i;
					}
					else if((i < strLength - 1) && (str->at(i + 2) == '\'') && (tokenLength == 0))
					{
						tokenLength = 3;
					}

					found = true;
					break;


				case ',':
				case '.':
				case '+':
				case '&':
				case '|':
				case ';':
				case '#':
				case '(':
				case ')':

					tokenLength = i - offset;
					if (tokenLength == 0)
					{
						tokenLength = 1;
					}
					found = true;
					break;

				default:
					i++;

				}//SWITCH STATMENT

			}//while (i < strLength && !found)

		}//ELSE

		if (i == strLength)
		{
			tokenLength = strLength - offset;
		}

	}//if (!iscomplete)

	if (offset == str->length()) //At end of lsit
	{
		complete = true; //return complete
	}
}//void


//Sets the current string to be tokenized
//Resets all Tokenizer state variables
//Calls Tokenizer::prepareNextToken() as the last statement before returning.
void Tokenizer::setString(string *input_str)
{
	if (input_str->length() == 0) //Empty string is detected
	{
		complete = true; //complete
	}
	else
	{
		//Reinitilze characters for next token
		complete = false;//Not complete

		offset = 0;
		tokenLength = 0;
		this -> str = input_str; // this points to private member str of tokenizer class

		prepareNextToken(); //calls as the last statement before returning for tokenize
		return;
	}


	return;
}


//////////////////////////////////////////////////////////////////////////////////////
//Returns the next token. Hint: consider the substr function
//Updates the tokenizer state
//Updates offset, resets tokenLength, updates processingABC member variables
//Calls Tokenizer::prepareNextToken() as the last statement before returning.
//////////////////////////////////////////////////////////////////////////////////////
string Tokenizer::getNextToken()
{
	string temp = str->substr(offset, tokenLength);
	//Use sub String function to returns a new string of length at point

	if (offset == str->length()) //At end of lsit
	{
		complete = true; //return complete
		return temp; // must return string ****
	}
    //Skips these character since they are case sensivtive
	if (temp == "'Z'" || temp == "'U'" || temp == "'X'" ||
		temp == "'W'" || temp == "'L'" || temp == "'H'")
	{
		//NOTHING BOIIII!!!
	}
	else
	{
		for (size_t i = 0; i < tokenLength; i++)
		{
			temp[i] = char(tolower(temp[i]));
		}
	}

	offset = offset + tokenLength;//move to the new positio
	tokenLength = 0; //Reset length token

	//Check for comment '--'
	//A comment on a line every character after is a commet
	if (comment)
	{
		comment = false;
	}
	if (temp == "--")
	{
		comment = true;
	}
	prepareNextToken();
	return temp;
}


void Tokenizer::TWS() //Trim white space
{
	if (offset == str->length())
	{
		complete = true;
		return;
	}
	//skips white space and tab and return characters
	while ((str->at(offset) == ' ' || str->at(offset) == '\t' || str->at(offset) == '\r') && offset <= str->length())
	{
		offset++;
		if (offset == str->length())
		{
			complete = true;
			return;
		}
	}
}


//Removes the token from the linked list if it is not null
//Deletes the token
//On return from function, head, tail and the prev and next Tokens (in relation to the provided token) may be modified.
void TokenList::deleteToken(Token *token)
{
	if (token)
	{
		Token *current = token;
		Token *next;
		Token *previous;

		if (head == token && tail == token)
		{
			delete current;
			head = NULL;
			tail = NULL;
			//only one token in list
		}
		else if (token->getPrev() == NULL)
		{
			head = head->getNext();
			head->setPrev(NULL);
			delete current;
			//token in head of the list
		}
		else if (token->getNext() == NULL)
		{
			tail = token->getPrev();
			tail->setNext(NULL);
				delete current;
			//token in tail of the list
		}
		else {
			next = token->getNext();
			previous = token->getPrev();
			previous->setNext(next);
			next->setPrev(previous);
			delete current;
			//token in the middle of the list
		}

	}
	else
	{
		// do nothing
	}
}


//Removes all comments from the tokenList including the -- marker
//Returns the number of comments removed
int removeComments(TokenList &tokenList)
{
	int count = 0;
	Token* current = tokenList.getFirst();//initialized current to the first token

		while (current) //this loop run till end of the list
		{

			if (current->getStringRep() == "--")
			{
				count++; //count comment to remove
				Token* remove_first = current;//make a pointer to remove '--'

				if (current->getNext() != NULL)
				{
					Token* remove_second = current->getNext();
					//check comment on the last line
					current = remove_second->getNext();
					tokenList.deleteToken(remove_first);
					tokenList.deleteToken(remove_second);
				}
				else
				{
					delete current;
				}
			}
			else
			{
				current = current->getNext();
			}
		}

	return count; //Returns the number of comments removed
}

//remove token of given type
int removeTokensOfType(TokenList &tokenList, tokenType type)
{
	int count = 0;

	Token* current = tokenList.getFirst();//initialized current to the first token

	while (current) //this loop run till end of the list
	{
		if (current->getTokenType() == type)
		{
			count++;
			Token* remove_first = current;

			if (current->getNext() != NULL)
			{
				tokenList.deleteToken(remove_first);
			}
			else
			{
				delete current;
			}
		}
		else
		{
			current = current->getNext();
		}
	}

	return count;
}


TokenList* findAllConditionalExpressions(const TokenList &tokenList)
{
	TokenList *Condition_List = new TokenList();
	Token *current = new Token;

	current = tokenList.getFirst();

	while (current)
	{
		//If conditional statements with prev not end
		if (current->getStringRep() == "if" && current->getPrev() != NULL
			&& current->getPrev()->getStringRep() != "end")
		{   //search for then after is
			while (current && current->getStringRep() != "then" && current->getStringRep() != ";" && current->getNext() != NULL)
			{
				if (current->getStringRep() == "if")
				{
					current = current->getNext();
				}
                //append everying in between
				Condition_List->append(current->getStringRep());

				if (current->getNext()->getStringRep() == "then")
				{
					Condition_List->append("\n");
					break;
				}
				current = current->getNext();
			}
		}//If conditional statements


		 //elsIf conditional statements
		if (current->getStringRep() == "elsif")
		{   //search for then after a elsif
			while (current && current->getStringRep() != "then" && current->getStringRep() != ";" && current->getNext() != NULL)
			{
				if (current->getStringRep() == "elsif")
				{
					current = current->getNext();
				}
                //append everying in between
				Condition_List->append(current->getStringRep());

				if (current->getNext()->getStringRep() == "then")
				{
					Condition_List->append("\n");
					break;
				}
				current = current->getNext();
			}
		} //elsIf conditional statements


		//when conditional statements
		if (current->getStringRep() == "when")
		{
            //search for a else statment after when
			while (current && current->getStringRep() != "else" && current->getStringRep() != ";" && current->getNext() != NULL)
			{
				if (current->getStringRep() == "when")
				{
					current = current->getNext();
				}
                 //append everying in between
				Condition_List->append(current->getStringRep());

				if (current->getNext()->getStringRep() == "else")
				{
					Condition_List->append("\n");
					break;
				}

				current = current->getNext();
			}
		}//when conditional statements

		current = current->getNext();
	}

	return Condition_List;
}


