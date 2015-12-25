#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
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