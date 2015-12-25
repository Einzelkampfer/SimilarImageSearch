#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <list>
#include <map>
#include "basic.h"
using namespace std;

vector<pair<bitset<BIT_NUM>, string>* > readdata() {
	ifstream hashin("../../hashcode.dat", ios_base::binary);
	ifstream imgin("../../trainImgList.txt");
	char buff[BYTE_NUM];
	vector<pair<bitset<BIT_NUM>, string>* > data;
	while (hashin.read(buff, BYTE_NUM)) {
		string imgPath;
		getline(imgin, imgPath);
		bitset<BIT_NUM> temp;
		for (int i = 0; i < BYTE_NUM; ++i) {
			bitset<8> byte(buff[i]);
			for (int j = 0; j < 8; ++j) {
				temp[BIT_NUM - (i * 8 + j) - 1] = byte[8 - j - 1];
			}
		}
		pair<bitset<BIT_NUM>, string>* temppair = new pair<bitset<BIT_NUM>, string>(temp, imgPath);
		data.push_back(temppair);
	}
	return data;
}

int getSliceHashCode(bitset<BIT_NUM> b, int begin) {
	int m = BIT_NUM / SLICE_NUM;
	bitset<BIT_NUM / SLICE_NUM> slice;
	for (int i = begin; i < begin + m; ++i) {
		slice[m - i  + begin - 1] = b[BIT_NUM - i - 1];
	}
	return slice.to_ulong();
}
void recurGetCombination(int i, int m, list<int> temp, list<list<int> > &result) {
	int len = temp.size();
	if (len == m) {
		list<int> combination;
		for (list<int>::iterator it = temp.begin(); it != temp.end(); ++it) {
			// cout << (*it) << " ";
			combination.push_back(*it);
		}
		// cout << '\n';
		result.push_back(combination);
	} else {
		if (i >= BIT_NUM / BYTE_NUM)
			return;
		if (m - temp.size() > BIT_NUM / BYTE_NUM - i)
			return;
		// cout << "take " << i << '\n';
		temp.push_back(i);
		recurGetCombination(i + 1, m, temp, result);
		// cout << "not take " << i << "\n";
		temp.pop_back();
		recurGetCombination(i + 1, m, temp, result);
	}
	return;
}

list<list<int> > getCombinationPos(int m) {
	list<list<int> > result;
	list<int> temp;
	recurGetCombination(0, m, temp, result);
	return result;
}

list<int> getRNeighbourPos(int pos) {
	int r = RADIUS / SLICE_NUM;
	list<int> result;
	for (int k = 0; k <= r; ++k) {
		list<list<int> > posCombination = getCombinationPos(k);
		cout << k << ":\n";
		for (list<list<int> >::iterator it1 = posCombination.begin(); it1 != posCombination.end(); it1++) {
			bitset<BIT_NUM / SLICE_NUM> b(pos);
			for (list<int>::iterator it2 = (*it1).begin(); it2 != (*it1).end(); it2++) {
				b.flip(BIT_NUM / SLICE_NUM - (*it2) - 1);
			}
			int temp = b.to_ulong();
			result.push_back(temp);
		}
	}
	return result;
}

