#include <zmq.hpp>
#include "basic.h"
#include "hashtable.h"
#include "mih.h"

int main() {
	MihSearcher searcher;
	zmq::context_t context(1);
	zmq::socket_t socket (context, ZMQ_REP);
	socket.bind("tcp://*:5555");
	while (true) {
		zmq::message_t request;
		socket.recv(&request);
		std::cout << "Received request" << std::endl;
		string binCode = string(static_cast<char*>(request.data()), request.size());
		bitset<BIT_NUM> b(binCode);
		vector<SearchRecord> result = searcher.searchRecord(b);
		int l = result.size();
		string reply = "[";
		for (int i = 0; i < l; ++i) {
			reply += "'";
			reply += result[i].first;
			reply += "'";
			if (i != l - 1)
				reply += ",";
			// cout << result[i].first << "\t" << result[i].second << "\n";
		}
		reply += "]";
		//  Send reply back to client
		zmq::message_t rep(reply.size());
		memcpy ((void *)rep.data(), reply.c_str(), reply.size());
		socket.send(rep);
	}
	
	return 0;
}