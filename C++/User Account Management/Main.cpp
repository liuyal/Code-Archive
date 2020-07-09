// File:        Main.cpp
// Date:        March 26, 2016
// Description: Simple test driver and UI 
//http://pumpkinprogrammer.com/2014/06/21/c-tutorial-intro-to-hash-tables/

#define _CRTDBG_MAP_ALLOC
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

#include "slinkedlist.h"
#include "hashtable.h"

using namespace std;

// forward function declarations
void PrintMenu(bool loginstatus, int ulevel);
void LLTest();
void HTTest();
void TestF();

void Constructors();
void ListTestM();
void ListRemove();
void ListTestA();
void ListAssign();
void ListDump();

void HashConstructors();
void HashInsert();
void HashRemove();
void HashSearch();
void HashRetrive();
void HashAssign();
void HashAssign2();

// program entry point

int main()
{
	_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_WARN, _CRTDBG_FILE_STDOUT);
	_CrtSetReportMode(_CRT_ERROR, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_ERROR, _CRTDBG_FILE_STDOUT);
	_CrtSetReportMode(_CRT_ASSERT, _CRTDBG_MODE_FILE);
	_CrtSetReportFile(_CRT_ASSERT, _CRTDBG_FILE_STDOUT);

	cout << "Entering linked list test..." << endl;
	
	Constructors();
	ListTestM();
	ListRemove();
	ListTestA();
	ListAssign();
	ListDump();
	LLTest();
	
	cout << "Entering hash table test..." << endl;

	HashConstructors();
	HashInsert();
	HashRemove();
	HashSearch();
	HashRetrive();
	HashAssign();
	HashAssign2();
	HTTest();

	TestF();

	_CrtDumpMemoryLeaks();
	system("pause");
	return 0;
}

void LLTest()
{
	SLinkedList<int> lla;
	lla.Contains(5);

	vector<int> v1 = lla.Dump();
	lla.InsertBack(2);
	lla.InsertFront(1);
	lla.IsEmpty();
	lla.Remove(3);
	lla.Retrieve(1);
	lla.Size();

	SLinkedList<int> llb(lla);

	SLinkedList<int> llc = lla;

}

void HTTest()
{
	HashTable ht1;
	HashTable ht2(10);
	ht1.Size();
	ht1.MaxSize();
	ht1.ListAt(0);
	ht1.LoadFactor();
	ht1.Insert(UserAccount("admin", ADMIN_));
	ht1.Remove(UserAccount("bob", REGULAR_));
	ht1.Retrieve(UserAccount("bob", REGULAR_));
	ht1.Search(UserAccount("bob", ADMIN_));
	HashTable ht3 = ht1;
}

void TestF()
{
	int choice = 0;
	string inputchoice;
	string inputname = "";    // currently logged in user
	string inputnewname = ""; // for adding or removing user
	string inputoldpassword1 = "";
	string inputoldpassword2 = "";
	string inputnewpassword = "";
	bool passwordmismatch = true;
	string inputlevel = "";
	int ilevel = 1;

	bool loggedin = false;
	int level = REGULAR_;

	HashTable ht;
	// insert a default admin account
	ht.Insert(UserAccount("admin", ADMIN_));

	cout << "admin:password" << endl << endl;

	while (choice != 7)
	{
		PrintMenu(loggedin, level);
		// get the menu choice from standard input
		getline(cin, inputchoice);
		choice = atoi(inputchoice.c_str());

		switch (choice)
		{
		case 1:
			// log in, log out
			if (!loggedin)
			{
				cout << "Enter username: ";
				getline(cin, inputname);
				cout << "Enter password: ";
				getline(cin, inputoldpassword1);
				if (!ht.Search(UserAccount(inputname, 0)))
				{
					cout << "Invalid username.\n" << endl;
				}
				else
				{
					UserAccount* ua = ht.Retrieve(UserAccount(inputname, 0)); // will not return NULL
					if (inputoldpassword1 != ua->GetPassword())
					{
						cout << "Invalid password.\n" << endl;
					}
					else
					{
						loggedin = true;
						level = ua->GetUserLevel();
					}
				}
			}
			else
			{
				cout << "Logged out.\n" << endl;
				loggedin = false;
				level = REGULAR_;
				// clear local variables for next login
				inputname = "";
				inputnewname = "";
				inputoldpassword1 = "";
				inputoldpassword2 = "";
				inputnewpassword = "";
				passwordmismatch = true;
			}
			break;
		case 2:
			// change password
			if (loggedin)
			{
				passwordmismatch = true;
				while (passwordmismatch && inputoldpassword1 != "quit")
				{
					cout << "Enter old password or type quit to exit: ";
					getline(cin, inputoldpassword1);
					if (inputoldpassword1 != "quit")
					{
						cout << "Enter old password again: ";
						getline(cin, inputoldpassword2);
						passwordmismatch = (inputoldpassword1 != inputoldpassword2);
					}
					else
					{
						passwordmismatch = false;
					}
				}
				if (inputoldpassword1 != "quit")
				{
					cout << "Enter new password: ";
					getline(cin, inputnewpassword);
					if (ht.Retrieve(UserAccount(inputname, 0))->SetPassword(inputoldpassword1, inputnewpassword))
						cout << "Password updated.\n" << endl;
					else
						cout << "Error updating password.\n" << endl;
				}
			}
			break;
		case 3:
			// admin-only, add new user
			if (loggedin && level == ADMIN_)
			{
				cout << "Enter new username (lowercase only): ";
				getline(cin, inputnewname);
				cout << "Enter access level (0 = ADMIN, 1 = REGULAR): ";
				getline(cin, inputlevel);
				ilevel = atoi(inputlevel.c_str());
				if (ht.Insert(UserAccount(inputnewname, ilevel)))
					cout << "New user " << inputnewname << " added.\n" << endl;
				else
					cout << "Error adding user.\n" << endl;
			}
			break;
		case 4:
			// admin-only, reset user password
			if (loggedin && level == ADMIN_)
			{
				cout << "Enter username for password reset: ";
				getline(cin, inputnewname);
				if (!ht.Search(UserAccount(inputnewname, 0)))
				{
					cout << "Invalid username.\n" << endl;
				}
				else
				{
					UserAccount* uap = ht.Retrieve(UserAccount(inputnewname, 0));
					uap->SetPassword(uap->GetPassword(), "password");
					cout << "Password for user " << uap->GetUsername() << " reset to default.\n" << endl;
				}
			}
			break;
		case 5:
			// admin-only, edit user level
			if (loggedin && level == ADMIN_)
			{
				cout << "Enter username for access level edit: ";
				getline(cin, inputnewname);
				if (inputnewname == "admin")
				{
					cout << "Cannot edit access level of admin.\n" << endl;
				}
				else if (!ht.Search(UserAccount(inputnewname, 0)))
				{
					cout << "Invalid username.\n" << endl;
				}
				else
				{
					cout << "Enter new access level (0 = ADMIN, 1 = REGULAR): ";
					getline(cin, inputlevel);
					ilevel = atoi(inputlevel.c_str());
					UserAccount* uap = ht.Retrieve(UserAccount(inputnewname, 0));
					if (uap->SetUserLevel(ilevel))
						cout << "Access level for user " << uap->GetUsername() << " successfully changed.\n" << endl;
					else
						cout << "Error setting access level for user " << uap->GetUsername() << ".\n" << endl;
				}
			}
			break;
		case 6:
			// admin-only, remove user
			if (loggedin && level == ADMIN_)
			{
				cout << "Enter username to remove: ";
				getline(cin, inputnewname);
				if (inputnewname == "admin")
				{
					cout << "Cannot remove admin.\n" << endl;
				}
				else if (ht.Remove(UserAccount(inputnewname, 0)))
				{
					cout << "User " << inputnewname << " removed.\n" << endl;
				}
				else
				{
					cout << "Error removing user " << inputnewname << ".\n" << endl;
				}
			}
			break;
		case 7:
			// do nothing, causes while loop to exit
			break;
		case 8:
			ht.HashPrint();
			break;
		default:
			break;
		}
	}
}

void PrintMenu(bool loginstatus, int ulevel)
{
	if (!loginstatus)
	{
		cout << "****************************************************\n"
			<< "* Please select an option:                         *\n"
			<< "* 1. Login                     7. Quit             *\n"
			<< "****************************************************\n" << endl;
		cout << "Enter your choice: ";
	}
	else
	{
		if (ulevel == ADMIN_)
		{
			cout << "****************************************************\n"
				<< "* Please select an option:                         *\n"
				<< "* 1. Logout                    6. Remove a user    *\n"
				<< "* 2. Change password                               *\n"
				<< "* 3. Add a new user                                *\n"
				<< "* 4. Reset user password       8. Print            *\n"
				<< "* 5. Edit user level           7. Quit             *\n"
				<< "****************************************************\n" << endl;
			cout << "Enter your choice: ";
		}
		else
		{
			cout << "****************************************************\n"
				<< "* Please select an option:                         *\n"
				<< "* 1. Logout                    7. Quit             *\n"
				<< "* 2. Change password                               *\n"
				<< "****************************************************\n" << endl;
			cout << "Enter your choice: ";
		}
	}
}

void Constructors()
{
	cout << "--------------------------Constructors()---------------------------" << endl;

	cout << endl << "Create New List..." << endl;
	SLinkedList<int> List1;
	List1.InsertFront(1);
	List1.InsertBack(2);
	List1.InsertBack(3);
	List1.InsertBack(0);
	List1.InsertBack(7);
	List1.InsertBack(23);
	List1.InsertBack(8);
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Create Copy List..." << endl;
	SLinkedList<int> List2(List1);
	cout << "Size: " << List2.Size() << endl;
	List2.Print();

	cout << endl << "Create Empty List..." << endl;
	SLinkedList<int> ListE;
	cout << "Size: " << ListE.Size() << endl;
	ListE.Print();

	cout << "Create Copy Empty List..." << endl;
	SLinkedList<int> List2E(ListE);
	cout << "Size: " << List2E.Size() << endl;
	List2E.Print();

	cout << endl;
}

void ListTestM()
{
	cout << "--------------------------ListTestM()---------------------------" << endl;

	cout << endl << "Create New List..." << endl;
	SLinkedList<int> List1;
	List1.InsertFront(1);
	List1.InsertBack(2);
	List1.InsertBack(3);
	List1.InsertBack(0);
	List1.InsertBack(7);
	List1.InsertBack(23);
	List1.InsertBack(8);

	cout << "Insert 7..." << endl;
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Remove Front(1)..." << endl;
	List1.Remove(1);
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Remove Mid (0)..." << endl;
	List1.Remove(0);
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Remove Back(8)..." << endl;
	List1.Remove(8);
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Remove Not in List..." << endl;
	if (List1.Remove(999) == false) { cout << "Item Not Found..." << endl; }
	else { cout << "Item Remoeved..." << endl; }
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << endl << "Remove ALL..." << endl;
	List1.RemoveAll();
	cout << "Size: " << List1.Size() << endl;
	List1.Print();

	cout << "Create New List2..." << endl;
	SLinkedList<int> List2;
	List2.InsertFront(4);
	List2.InsertBack(2);
	List2.InsertBack(3);
	List2.InsertBack(5);
	List2.InsertBack(7);
	List2.InsertBack(4);
	List2.InsertBack(8);
	cout << "Size: " << List2.Size() << endl;
	List2.Print();

	cout << endl << "Remove (4)..." << endl;
	List2.Remove(4);
	cout << "Size: " << List2.Size() << endl;
	List2.Print();

	cout << endl;
}

void ListRemove()
{
	cout << "--------------------------ListRemove()---------------------------" << endl;

	cout << endl << "Create New ListA..." << endl;
	SLinkedList<int> ListA;
	ListA.InsertFront(1);
	ListA.InsertBack(2);
	ListA.InsertBack(3);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Remove Mid(2)..." << endl;
	ListA.Remove(2);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Remove Back(3)..." << endl;
	ListA.Remove(3);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Remove Front(1)..." << endl;
	ListA.Remove(1);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	ListA.RemoveAll();

	cout << "Create New ListB..." << endl;
	SLinkedList<int> ListB;
	ListB.InsertFront(1);
	ListB.InsertBack(2);
	ListB.InsertBack(3);
	cout << "Size: " << ListB.Size() << endl;
	ListB.Print();

	cout << endl << "Remove Mid(2)..." << endl;
	ListB.Remove(2);
	cout << "Size: " << ListB.Size() << endl;
	ListB.Print();

	cout << endl << "Remove Front(1)..." << endl;
	ListB.Remove(1);
	cout << "Size: " << ListB.Size() << endl;
	ListB.Print();

	cout << endl << "Remove Back(3)..." << endl;
	ListB.Remove(3);
	cout << "Size: " << ListB.Size() << endl;
	ListB.Print();


	ListB.RemoveAll();

	cout << endl;
}

void ListTestA()
{
	cout << "--------------------------ListTestA()---------------------------" << endl;

	cout << endl << "Create New List..." << endl;
	SLinkedList<string> ListS;
	ListS.InsertFront("Apple");
	ListS.InsertBack("Bee");
	ListS.InsertBack("Cake");
	ListS.InsertBack("Tree");
	ListS.InsertBack("Ball");
	ListS.InsertBack("Dog");
	ListS.InsertBack("Tosh");
	ListS.InsertBack("Atlas");
	ListS.InsertBack("Devil");
	ListS.InsertBack("Coin");
	cout << "Size: " << ListS.Size() << endl;
	ListS.Print();

	cout << endl << "Contain Test..." << endl;
	if (ListS.Contains("Cake") == true) { cout << "List Contain Cake" << endl; }
	else { cout << "List Does Not Contain Cake" << endl; }
	if (ListS.Contains("Atlas") == true) { cout << "List Contain Atlas" << endl; }
	else { cout << "List Does Not Contain Atlas" << endl; }
	if (ListS.Contains("Apple") == true) { cout << "List Contain Apple" << endl; }
	else { cout << "List Does Not Contain Apple" << endl; }
	if (ListS.Contains("Coin") == true) { cout << "List Contain Coin" << endl; }
	else { cout << "List Does Not Contain Coin" << endl; }
	if (ListS.Contains("Tosh") == true) { cout << "List Contain Tosh" << endl; }
	else { cout << "List Does Not Contain Tosh" << endl; }
	if (ListS.Contains("Omni") == true) { cout << "List Contain Omni" << endl; }
	else { cout << "List Does Not Contain Omni" << endl; }
	if (ListS.Contains("Knight") == true) { cout << "List Contain Knight" << endl; }
	else { cout << "List Does Not Contain Knight" << endl; }

	cout << endl << "Retrieve Test..." << endl;
	string *R = ListS.Retrieve("Apple");
	if (R == NULL) { cout << "Apple Not Found..." << endl; }
	else { cout << "Apple Found.." << endl; }
	string *R1 = ListS.Retrieve("Ball");
	if (R1 == NULL) { cout << "Ball Not Found..." << endl; }
	else { cout << "Ball Found.." << endl; }
	string *R2 = ListS.Retrieve("Coin");
	if (R2 == NULL) { cout << "Coin Not Found..." << endl; }
	else { cout << "Coin Found.." << endl; }
	string *R3 = ListS.Retrieve("Knight");
	if (R3 == NULL) { cout << "Knight Not Found..." << endl; }
	else { cout << "Knight Found.." << endl; }

	cout << endl << "Create New Empty List..." << endl;
	SLinkedList<string> ListS2;
	if (ListS2.Contains("Cake") == true) { cout << "List Contain Cake" << endl; }
	else { cout << "List Does Not Contain Cake" << endl; }
	string *RS = ListS2.Retrieve("Apple");
	if (RS == NULL) { cout << "Apple Not Found..." << endl; }
	else { cout << "Apple Found.." << endl; }
	string *RS2 = ListS2.Retrieve("Coin");
	if (RS2 == NULL) { cout << "Coin Not Found..." << endl; }
	else { cout << "Coin Found.." << endl; }

	cout << endl;
}

void ListAssign()
{
	cout << "--------------------------ListAssign()---------------------------" << endl;

	cout << endl << "Create New ListA..." << endl;
	SLinkedList<int> ListA;
	ListA.InsertFront(1);
	ListA.InsertBack(2);
	ListA.InsertBack(3);
	ListA.InsertBack(4);
	ListA.InsertBack(5);
	ListA.InsertBack(6);
	ListA.InsertBack(7);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Create New ListB..." << endl;
	SLinkedList<int> ListB;
	ListB.InsertFront(88);
	ListB.InsertBack(92);
	ListB.InsertBack(77);
	cout << "Size: " << ListB.Size() << endl;
	ListB.Print();

	cout << endl << "Assign B to A..." << endl;
	ListA = ListB;
	cout << "Size ListB: " << ListB.Size() << endl;
	ListB.Print();
	cout << "Size ListA: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Create Empty List..." << endl;
	SLinkedList<int> List2E;
	cout << "Size: " << List2E.Size() << endl;
	List2E.Print();

	cout << "Assign Empty to B & A..." << endl;
	ListA = List2E;
	ListB = List2E;
	cout << "Size ListB: " << ListB.Size() << endl;
	ListB.Print();
	cout << "Size ListA: " << ListA.Size() << endl;
	ListA.Print();

	cout << "";
}

void ListDump()
{
	cout << "--------------------------ListDump()---------------------------" << endl;

	cout << endl << "Create New ListA..." << endl;
	SLinkedList<int> ListA;
	ListA.InsertFront(1);
	ListA.InsertBack(2);
	ListA.InsertBack(3);
	ListA.InsertBack(4);
	ListA.InsertBack(5);
	ListA.InsertBack(6);
	ListA.InsertBack(7);
	ListA.InsertBack(8);
	ListA.InsertBack(9);
	ListA.InsertBack(10);
	cout << "Size: " << ListA.Size() << endl;
	ListA.Print();

	cout << endl << "Dump into Vector..." << endl;
	cout << "Print Vector: " << endl;
	vector<int> V = ListA.Dump();
	for (unsigned int i = 0; i < V.size(); ++i) { cout << V[i] << ' '; }

	cout << endl << endl << "Create New ListS..." << endl;
	SLinkedList<string> ListS;
	ListS.InsertFront("Apple");
	ListS.InsertBack("Bee");
	ListS.InsertBack("Cake");
	ListS.InsertBack("Tree");
	ListS.InsertBack("Ball");
	ListS.InsertBack("Dog");
	ListS.InsertBack("Tosh");
	ListS.InsertBack("Atlas");
	ListS.InsertBack("Devil");
	ListS.InsertBack("Coin");
	cout << "Size: " << ListS.Size() << endl;
	ListS.Print();

	cout << endl << "Dump ListS into Vector..." << endl;
	cout << "Print Vector: " << endl;
	vector<string> V2 = ListS.Dump();
	for (unsigned int i = 0; i < V2.size(); ++i) { cout << V2[i] << ' '; }

	cout << endl << endl;
}

void HashConstructors()
{
	cout << "--------------------------HashConstructors()---------------------------" << endl << endl;

	cout << "Create Hash TableS..." << endl;
	HashTable HashS(4);

	HashS.HashPrint();

	cout << "Hash Table Insert..." << endl;
	HashS.Insert(UserAccount("cat", 1));
	HashS.Insert(UserAccount("apple", 1));
	HashS.Insert(UserAccount("boat", 1));

	HashS.HashPrint();

	cout << "Create Copy Hash Table..." << endl;

	HashTable HashM(HashS);

	HashM.HashPrint();

	cout << "Create Empty Hash TableS..." << endl;
	HashTable HashE(2);
	HashE.HashPrint();

	cout << "Create Copy Empty Hash TableS..." << endl;
	HashTable HashCE(HashE);
	HashCE.HashPrint();

	cout << endl;
}

void HashInsert()
{
	cout << "--------------------------HashInsert()---------------------------" << endl;

	cout << endl << "Create Hash Table & Insert..." << endl;

	HashTable Hash(4);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));
	Hash.Insert(UserAccount("blue", 1));
	Hash.Insert(UserAccount("milk", 0));
	Hash.Insert(UserAccount("gum", 1));
	Hash.Insert(UserAccount("light", 0));

	Hash.HashPrint();

	cout << "Load Factor above 2/3 Increase Max size..." << endl;
	Hash.Insert(UserAccount("knight", 1));

	Hash.HashPrint();

	cout << "Insert More Items.." << endl << endl;;

	Hash.Insert(UserAccount("b", 1));
	Hash.Insert(UserAccount("m", 1));
	Hash.Insert(UserAccount("z", 1));
	Hash.Insert(UserAccount("ti", 1));
	Hash.Insert(UserAccount("fin", 1));

	if (Hash.Insert(UserAccount("onion", 1)) == false) { cout << "Repeated item not Inserted..." << endl; }
	else { cout << "Repeated item Inserted..." << endl; }

	Hash.HashPrint();

	cout << endl;
}

void HashRemove()
{
	cout << "--------------------------HashRemove()---------------------------" << endl;

	cout << endl << "Create Hash Table..." << endl;

	HashTable Hash(5);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));
	Hash.Insert(UserAccount("blue", 1));
	Hash.Insert(UserAccount("milk", 0));
	Hash.Insert(UserAccount("gum", 1));
	Hash.Insert(UserAccount("light", 0));
	Hash.Insert(UserAccount("knight", 1));
	Hash.Insert(UserAccount("boom", 1));
	Hash.Insert(UserAccount("m", 1));
	Hash.Insert(UserAccount("z", 1));
	Hash.Insert(UserAccount("ti", 1));
	Hash.Insert(UserAccount("fin", 1));

	Hash.HashPrint();

	cout << "Remove Items..." << endl;

	Hash.Remove(UserAccount("knight", 1));
	Hash.Remove(UserAccount("boom", 1));
	Hash.Remove(UserAccount("m", 1));
	Hash.Remove(UserAccount("z", 1));
	Hash.Remove(UserAccount("ti", 1));
	Hash.Remove(UserAccount("bravo", 1));
	Hash.Remove(UserAccount("blue", 1));
	Hash.Remove(UserAccount("milk", 0));

	Hash.HashPrint();

	cout << endl;
}

void HashSearch()
{
	cout << "--------------------------HashSearch()---------------------------" << endl;

	cout << endl << "Create Hash Table..." << endl;

	HashTable Hash(5);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));
	Hash.Insert(UserAccount("blue", 1));
	Hash.Insert(UserAccount("milk", 0));
	Hash.Insert(UserAccount("gum", 1));
	Hash.Insert(UserAccount("light", 0));
	Hash.Insert(UserAccount("knight", 1));
	Hash.Insert(UserAccount("boom", 1));
	Hash.Insert(UserAccount("mind", 0));
	Hash.Insert(UserAccount("zap", 1));
	Hash.Insert(UserAccount("timmy", 1));
	Hash.Insert(UserAccount("fin", 1));
	Hash.Insert(UserAccount("maple", 1));
	Hash.Insert(UserAccount("candy", 1));

	Hash.HashPrint();

	if (Hash.Search(UserAccount("fin", 1)) == true) { cout << "fin found" << endl; }
	else { cout << "fin not found" << endl; }
	if (Hash.Search(UserAccount("fin", 0)) == true) { cout << "fin found" << endl; }
	else { cout << "fin not found" << endl; }
	if (Hash.Search(UserAccount("onion", 1)) == true) { cout << "onion found" << endl; }
	else { cout << "fin not found" << endl; }
	if (Hash.Search(UserAccount("boom", 1)) == true) { cout << "boom found" << endl; }
	else { cout << "boom not found" << endl; }
	if (Hash.Search(UserAccount("zap", 1)) == true) { cout << "zap found" << endl; }
	else { cout << "zap not found" << endl; }
	if (Hash.Search(UserAccount("timmy", 1)) == true) { cout << "timmy found" << endl; }
	else { cout << "timmy not found" << endl; }
	if (Hash.Search(UserAccount("zero", 1)) == true) { cout << "zero found" << endl; }
	else { cout << "zero not found" << endl; }
	if (Hash.Search(UserAccount("dog", 1)) == true) { cout << "dog found" << endl; }
	else { cout << "dog not found" << endl; }

	cout << endl;
}

void HashRetrive()
{
	cout << "--------------------------HashRetrive()---------------------------" << endl;

	cout << endl << "Create Hash Table..." << endl;

	HashTable Hash(5);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));
	Hash.Insert(UserAccount("candy", 1));
	Hash.Insert(UserAccount("milk", 0));
	Hash.Insert(UserAccount("gum", 1));
	Hash.Insert(UserAccount("light", 0));
	Hash.Insert(UserAccount("knight", 1));
	Hash.Insert(UserAccount("boom", 1));
	Hash.Insert(UserAccount("cake", 0));

	Hash.HashPrint();

	cout << "Retrive Items and Change Name" << endl;

	UserAccount *UI = Hash.Retrieve(UserAccount("onion", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("night", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("bravo", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("candy", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("milk", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("gum", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("light", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("knight", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("boom", 1));
	UI->SetUsername("o");
	UI = Hash.Retrieve(UserAccount("cake", 1));
	UI->SetUsername("o");

	UserAccount *UI2 = Hash.Retrieve(UserAccount("evil", 1));
	UserAccount *UI3 = Hash.Retrieve(UserAccount("zero", 0));
	cout << "Search Item Not in List: " << UI2 << endl;
	cout << "Search Item Not in List: " << UI3 << endl;

	Hash.HashPrint();

	cout << endl;
}

void HashAssign()
{
	cout << "--------------------------HashAssign()---------------------------" << endl;

	cout << endl << "Create Hash Table..." << endl;

	HashTable Hash(5);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));

	Hash.HashPrint();

	cout << "Create Hash Table B..." << endl;
	cout << "Assign Hash to HashB..." << endl;

	HashTable HashB;

	HashB = Hash;
	HashB.HashPrint();

	cout << "Insert HashB..." << endl;
	HashB.Insert(UserAccount("nine", 1));
	HashB.Insert(UserAccount("candy", 1));

	HashB.HashPrint();

	cout << "Assign HashB to Hash..." << endl;

	Hash = HashB;
	Hash.HashPrint();

	cout << endl;
}

void HashAssign2()
{
	cout << "--------------------------HashAssign2()---------------------------" << endl;

	cout << endl << "Create Hash Table..." << endl;

	HashTable Hash(5);
	HashTable HashE(5);

	Hash.Insert(UserAccount("onion", 1));
	Hash.Insert(UserAccount("night", 1));
	Hash.Insert(UserAccount("bravo", 1));

	HashTable HashC(Hash);

	HashC.Insert(UserAccount("zero", 1));
	HashC.Insert(UserAccount("nest", 1));
	HashC.Insert(UserAccount("tea", 1));

	Hash.HashPrint();

	Hash = HashE;

	cout << "Assign Empty to Hash Table..."<< endl;
	Hash.HashPrint();

	cout << "Assign Hash to Empty Hash Table..." << endl;
	Hash = HashC;
	Hash.HashPrint();

	cout << "Assign Empty to Empty Hash" << endl;
	HashTable HashE2;

	HashE.HashPrint();
	HashE2.HashPrint();

	HashE2 = HashE;

	HashE.HashPrint();
	HashE2.HashPrint();

	cout << endl;
}
