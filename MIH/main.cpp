#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <map>
#include "basic.h"
#include "hashtable.h"
int main() {
	HashTable hashtables[SLICE_NUM];
	vector<pair<bitset<BIT_NUM>, string>* > data = readdata();
	int len = data.size();
	for (int i = 0; i < len; ++i) {
		for (int j = 0; j < SLICE_NUM; ++j) {
			int pos = getSliceHashCode(data[i] -> first, j * BIT_NUM / SLICE_NUM);
			hashtables[j].addItem(data[i], pos);
		}
	}
	// for (int i = 0; i < hashtables[31].size(); ++i) {
	// 	vector<pair<bitset<BIT_NUM>, string>*> bucket = hashtables[31].getBucket(i);
	// 	len = bucket.size();
	// 	cout << len << "\n";
	// }
	
	vector<pair<bitset<BIT_NUM>, string>*> bucket = hashtables[31].getBucket(0);
	for (int i = 0; i < len; ++i) {
		cout << bucket[i] -> first << "\n";
	}
	return 0;
}