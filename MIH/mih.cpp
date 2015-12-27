#include "basic.h"
#include "hashtable.h"
#include "mih.h"

MihSearcher::MihSearcher() {
	double dur;
	clock_t start,end;
	start = clock();
	vector<ImageData > data = readdata();
	int len = data.size();
	for (int i = 0; i < len; ++i) {
		for (int j = 0; j < SLICE_NUM; ++j) {
			int pos = getSliceHashCode(data[i] -> first, j * BIT_NUM / SLICE_NUM);
			hashtables[j].addItem(data[i], pos);
		}
	}
	int m = BIT_NUM / SLICE_NUM;
	int tableSize = 1;
	while (m--) {
		tableSize <<= 1;
	}
	rNeighbours = new vector<list<int> >(tableSize);
	for (int i = 0; i < tableSize; ++i) {
		(*rNeighbours)[i] = getRNeighbourPos(i);
	}
	end = clock();
	dur = (double)(end - start);
	cout << "Load Hash Table Time:" << dur/CLOCKS_PER_SEC << "\n";
}
MihSearcher::~MihSearcher() {
	delete rNeighbours;
}
vector<SearchRecord> MihSearcher::searchRecord(bitset<BIT_NUM> record) {
	double dur;
	clock_t start,end;
	start = clock();
	vector<SearchRecord> result;
	set<string> selected;
	for (int i = 0; i < SLICE_NUM; ++i) {
		int hashPos = getSliceHashCode(record, i * BIT_NUM / SLICE_NUM);
		for (list<int>::iterator it = (*rNeighbours)[hashPos].begin(); it != (*rNeighbours)[hashPos].end(); ++it) {
			vector<ImageData> targetBucket = hashtables[i].getBucket((*it));
			int len = targetBucket.size();
			for (int j = 0; j < len; ++j) {
				set<string>::iterator checkIt = selected.find(targetBucket[j] -> second);
				if (checkIt == selected.end()) {
					int dist = hammingDistance(targetBucket[j] -> first, record);
					selected.insert(targetBucket[j] -> second);
					if (dist <= RADIUS) {
						SearchRecord s(targetBucket[j] -> second, dist);
						result.push_back(s);
						// cout << dist << "\t" << targetBucket[j] -> second << "\n";
					}
				}
			}
		}
	}
	sort(result.begin(), result.end(), cmp);
	end = clock();
	dur = (double)(end - start);
	cout << "Lookup Time:" << dur/CLOCKS_PER_SEC << "\n";
	return result;
}