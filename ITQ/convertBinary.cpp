#include <iostream>
#include <fstream>
#include <bitset>
#define BIT_NUM 8
using namespace std;
int main(int argc, char **argv) {
	if (argc >= 2) {
		char* filename = argv[1];
		ifstream fin(filename);
		ofstream fout("../../hashcode.dat", ios::binary);
		char c;
		bitset<BIT_NUM> temp;
		int index = 0;
		while (fin.get(c)) {
			if (c != '\n' && c != ',') {
				temp.set(index++, c - '0');
			}
			if (index == BIT_NUM) {
				char byte = (char)temp.to_ulong();
				fout.put(byte);
				index = 0;
			}
		}
		fin.close();
		fout.close();
	}
	return 0;
}