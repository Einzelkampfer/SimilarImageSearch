#ifndef MIH_H
#define MIH_H

#include "basic.h"
#include "hashtable.h"

class MihSearcher {
public:
	MihSearcher();
	~MihSearcher();
	vector<SearchRecord> searchRecord(bitset<BIT_NUM> record);
private:
	HashTable hashtables[SLICE_NUM];
	vector<list<int> >* rNeighbours;
};

#endif