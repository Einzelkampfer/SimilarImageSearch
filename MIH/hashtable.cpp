#include "basic.h"
#include "hashtable.h"
HashTable::HashTable() {
	int m = BIT_NUM / SLICE_NUM;
	int tableSize = 1;
	while (m--) {
		tableSize <<= 1;
	}
	table = new vector<vector<ImageData> >(tableSize);
	bucketNum = tableSize;
}
HashTable::~HashTable() {
	delete table;
}
void HashTable::addItem(ImageData record, int pos) {
	ImageData temp = record;
	(*table)[pos].push_back(temp);
}
vector<ImageData> HashTable::getBucket(int pos) {
	return (*table)[pos];
}
int HashTable::size() {
	return bucketNum;
}