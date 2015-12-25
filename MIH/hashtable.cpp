#include "basic.h"
#include "hashtable.h"
HashTable::HashTable() {
	int m = BIT_NUM / SLICE_NUM;
	int tableSize = 1;
	while (m--) {
		tableSize <<= 1;
	}
	table = new vector<vector<pair<bitset<BIT_NUM>, string>*> >(tableSize);
	bucketNum = tableSize;
}
HashTable::~HashTable() {
	delete table;
}
void HashTable::addItem(pair<bitset<BIT_NUM>, string>* record, int pos) {
	pair<bitset<BIT_NUM>, string>* temp = record;
	(*table)[pos].push_back(temp);
}
vector<pair<bitset<BIT_NUM>, string>*> HashTable::getBucket(int pos) {
	return (*table)[pos];
}
int HashTable::size() {
	return bucketNum;
}