#ifndef BASIC_H
#define BASIC_H

#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <map>
#include <list>
#define BIT_NUM 256
#define BYTE_NUM 32
#define SLICE_NUM 32
#define RADIUS 96
using namespace std;

vector<pair<bitset<BIT_NUM>, string>* > readdata();
int getSliceHashCode(bitset<BIT_NUM> b, int begin);
list<list<int> > getCombinationPos(int m);
void recurGetCombination(int i, int m, list<int> temp, list<list<int> > &result);
list<int> getRNeighbourPos(int pos);

#endif