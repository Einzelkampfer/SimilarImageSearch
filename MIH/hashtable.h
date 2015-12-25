#ifndef HASHTABLE_H
#define HASHTABLE_H
#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <map>
#include "basic.h"
class HashTable {
public:
	HashTable();
	~HashTable();
	void addItem(pair<bitset<BIT_NUM>, string>* record, int pos);
	vector<pair<bitset<BIT_NUM>, string>*> getBucket(int pos);
	int size();
private:
	vector<vector<pair<bitset<BIT_NUM>, string>*> >* table;
	int bucketNum;
};

#endif