

#include "Stock.h"

#include <iostream>
#include <fstream>
#include <sstream>

#include <cstdlib>
#include <string>
#include <vector>

Stock::Stock()
{
	count = 0;
	string name = "";
	string path = "";
	vector<string> date;
	vector<double> Price;
}

Stock::Stock(string name, string csv_path)
{
	this->count = 0;
	this->name = name;
	this->path = csv_path;

	string line;
	string arr[7];
	double temp = 0.0;
	ifstream myfile(csv_path);

	if (myfile.is_open())
	{
		while (getline(myfile, line))
		{
			string str = line;

			for (unsigned int i = 1; i < str.length(); i++)
			{
				if (str[i] == ',') { str[i] = ' '; }
				stringstream ss(str);
				for (int j = 0; j < 7; j++) { ss >> arr[j]; }
			}

			if (count > 0)
			{
				this->date.push_back(arr[0]);
				temp = stod(arr[6]);
				this->Price.push_back(temp);
			}
			count++;
		}

		myfile.close();
	}
}

Stock::~Stock()
{
};
