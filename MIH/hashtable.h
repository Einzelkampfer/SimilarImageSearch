#ifndef HASHTABLE_H
#define HASHTABLE_H

#include "basic.h"

class HashTable {
public:
	HashTable();
	~HashTable();
	void addItem(ImageData record, int pos);
	vector<ImageData> getBucket(int pos);
	int size();
private:
	vector<vector<ImageData> >* table;
	int bucketNum;
};

#endif