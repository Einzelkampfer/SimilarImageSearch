#include <iostream>
#include <fstream>

using namespace std;
int main(int argc, char **argv) {
	if (argc >= 2) {
		char* filename = argv[1];
		fstream fout(filename);
		cout << "fuck";
		fout.close();
	}
	return 0;
}