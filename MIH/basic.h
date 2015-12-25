#ifndef BASIC_H
#define BASIC_H

#include <iostream>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <map>
#define BIT_NUM 256
#define BYTE_NUM 32
#define SLICE_NUM 32
#define RADIUS 96
using namespace std;
vector<pair<bitset<BIT_NUM>, string>* > readdata();
int getSliceHashCode(bitset<BIT_NUM> b, int begin);
#endif