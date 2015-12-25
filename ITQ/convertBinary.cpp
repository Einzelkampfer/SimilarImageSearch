#include <iostream>
#include <cstdio>
#include <fstream>
#include <bitset>
#define BIT_NUM 8
using namespace std;
int main(int argc, char **argv) {
	if (argc >= 2) {
		char* filename = argv[1];
		ifstream fin(filename);
		ofstream fout("../../hashcode.dat", ios_base::trunc | ios_base::out | ios_base::binary);
		char c;
		bitset<BIT_NUM> temp;
		int index = 0;
		int count = 0;
		while (fin.get(c)) {
			if (c != '\n' && c != ',') {
				temp.set(BIT_NUM - index - 1, c - '0');
				index++;
			}
			if (index == BIT_NUM) {
				unsigned char byte = static_cast<unsigned char>(temp.to_ulong());
				fout.put(byte);
				count++;
				index = 0;
			}
		}
		// cout << count << "\n";
		fin.close();
		fout.close();
	}
	return 0;
}