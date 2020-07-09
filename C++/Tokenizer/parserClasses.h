#ifndef PARSERCLASSES_H_
#define PARSERCLASSES_H_

 
using namespace std;

//Declare variables for storing delimiters here:
//VHDL delimiters

const char delimiters[] = { '<>', '=', '/=', '>=', '<=', ':=', '=>', '<', '>', '\"',
						'\'', '.', ':', '+', '-', '/', '*', '**', '&', '|', ';', '#', '(', ')','--' };

//Token class for a doubly-linked list of string tokens
class Token 
{
private:
	Token *next; //Next pointer for doubly linked list
	Token *prev; //Previous pointer for doubly linked list
	string stringRep; //Token value
	 
  //Allow TokenList class to access Token member variables marked private
  //https://en.wikipedia.org/wiki/Friend_class
 
	friend class TokenList;

public:
	//Default Constructor, pointers initialized to NULL
	Token() : next(nullptr), prev(nullptr) {}

	//Constructor with string initialization, pointers initialized to NULL
	Token(const string &stringRep) : next(nullptr), prev(nullptr), stringRep(stringRep) {}

	//Returns the Token's *next member 
	Token* getNext () const {  return next; }

	//Sets the Token's *next member
	void setNext (Token* next ) { this->next = next; }

	//Returns the Token's *prev member 
	Token* getPrev () const { return prev; }

	//Sets the Token's *prev member
	void setPrev (Token* prev ){ this->prev = prev; }

	//Returns a reference to the Token's stringRep member variable
	const string& getStringRep () const { return stringRep; }

	//Sets the token's stringRep variable
	void setStringRep (const string& stringRep ) { this->stringRep = stringRep; }
};


//A doubly-linked list class consisting of Token elements
class TokenList 
{
private:
	Token *head; //Points to the head of the token list (doubly linked)
	Token *tail; //Points to the tail of the function list (doubly linked)
	
public:
	//Default Constructor, Empty list with pointers initialized to NULL
	TokenList() : head(nullptr), tail(nullptr) {}
	

	//Returns a pointer to the head of the list
	Token* getFirst() const {return head;}


	//Returns a pointer to the tail of the list
	Token* getLast() const { return tail; }


	//Creates a new token for the string input, str
	//Appends this new token to the TokenList
	//On return from the function, it will be the last token in the list
	void append(const string &str); 


	//Appends the token to the TokenList if not null
	//On return from the function, it will be the last token in the list
	void append(Token *token);

    //Removes the token from the linked list if it is not null
	//Deletes the token
	//On return from function, head, tail and the prev and next Tokens (in relation to the provided token) may be modified.
	void deleteToken(Token *token);


};

//A class for tokenizing a string of VHDL  code into tokens
class Tokenizer
{
private:
	/*State tracking variables for processing a single string*/
	bool iscomplete; //True if finished processing the current string
	
	size_t offset; //Current position in string
	size_t tokenLength; //Current token length
	string *str; //A pointer to the current string being processed

	//Include any helper functions here
	//e.g. trimming whitespace, comment processing


	bool comment;//Comment case with '--'         i.e --This is VHDL comment
	//check for context clause [Liberay] and [Use]


	//Computes a new tokenLength for the next token
	//Modifies: size_t tokenLength, and bool complete
	//(Optionally): may modify offset
	//Does NOT modify any other member variable of Tokenizer
	void prepareNextToken();
	
public:
	///////////////////////////////////////////////////////////////////////
	//Default Constructor- YOU need to add the member variable initializers.
	///////////////////////////////////////////////////////////////////////
	Tokenizer()
	{
		offset = 0;
		tokenLength = 0;
		str = NULL;
		comment = false;
	}

	//Sets the current string to be tokenized
	//Resets all Tokenizer state variables
	//Calls Tokenizer::prepareNextToken() as the last statement before returning.
	void setString(string *input_str);

	//Returns true if all possible tokens have been extracted from the current string (string *str)
	bool isComplete() const 
	{
		return iscomplete;
	}

	//Returns the next token. Hint: consider the substr function
	//Updates the tokenizer state
	//Updates offset, resets tokenLength, updates processingABC member variables
	//Calls Tokenizer::prepareNextToken() as the last statement before returning.
	string getNextToken();


	/*
	friend ostream &operator << (ostream &output, Tokenizer &object)
	{
		output << object.offset;
		return output;
	}
	*/


};

//Removes all comments from the tokenList including the -- marker
//Returns the number of comments removed
int removeComments(TokenList &tokenList);

#endif /* PARSERCLASSES_H_ */
