
#include "parserClasses.h"
#include <string>
 
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
	if (!iscomplete)
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
							iscomplete = true;
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
					if ((str->at(i + 1) == '-') && (i < strLength - 1) && (tokenLength == 0))//Detect '--'
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
					if ((str->at(i + 1) == '>') && (i < strLength - 1) && (tokenLength == 0))//Detect '=>'
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
					if ((str->at(i + 1) == '=') && (i < strLength - 1) && (tokenLength == 0))//Detect '<='
					{
						tokenLength = 2; //Length of '<='
					}
					if ((str->at(i + 1) == '>') && (i < strLength - 1) && (tokenLength == 0))//Detect '<>'
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
					if ((str->at(i + 1) == '=') && (i < strLength - 1) && (tokenLength == 0))//Detect '/=','>=','=='
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
					if ((str->at(i + 1) == '*') && (i < strLength - 1) && (tokenLength == 0))//Detect '**'
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
					while (i < strLength - 1 && !(str->at(i) != '--' && str->at(i + 1) == '\''))
					{
						i++;
					}
					tokenLength = i + 2 - offset;
					found = true;
					break;



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
		iscomplete = true; //return complete
	}
}//void



//Sets the current string to be tokenized
//Resets all Tokenizer state variables
//Calls Tokenizer::prepareNextToken() as the last statement before returning.
void Tokenizer::setString(string *input_str) 
{ 
	if (input_str->length() == 0) //Empty string is detected
	{
		iscomplete = true; //complete
	}
	else
	{	
		//Reinitilze characters for next token
		iscomplete = false;//Not complete

		offset = 0;
		tokenLength = 0;
		this -> str = input_str; // this points to private member str of tokenizer class

		prepareNextToken(); //calls as the last statement before returning for tokenize
		return;
	}
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
		iscomplete = true; //return complete
		return temp; // must return string ****
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


