#ifndef BASIC_H
#define BASIC_H

#include <python2.7/Python.h>
#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <list>
#include <set>
#include <algorithm>

#define BIT_NUM 256
#define BYTE_NUM 32
#define SLICE_NUM 16
#define RADIUS 80
using namespace std;
typedef pair<bitset<BIT_NUM>, string>* ImageData;
typedef pair<string, int> SearchRecord;

bool cmp(SearchRecord s1, SearchRecord s2);
vector<ImageData> readdata();
int getSliceHashCode(bitset<BIT_NUM> b, int begin);
list<list<int> > getCombinationPos(int m);
void recurGetCombination(int i, int m, list<int> temp, list<list<int> > &result);
list<int> getRNeighbourPos(int pos);
int hammingDistance(bitset<BIT_NUM> b1, bitset<BIT_NUM> b2);

#endif