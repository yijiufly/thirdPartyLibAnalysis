import networkx as nx



def loadGraphFromFile(filepath, graph):	
	with open(filepath) as fp:  
		
		#cnt = 0
		while True:
			line = fp.readline()

			if not line:
				break

			nodeInfo = []
			line1 = line.strip() #node index
			index = int(line1)
			
			line = fp.readline()
			line2 = line.strip() #feature 1
			feature1 = line2

			line = fp.readline()
			line3 = line.strip() #feature 2
			if line3 == '\n':
				feature2 = line3
			else:
				feature2 = line3.split()

			line = fp.readline()
			line4 = line.strip() #feature 3
			if line4 == '\n':
				feature3 = line4
			else:
				feature3 = line4.split()

			nodeInfo.append(index)
			nodeInfo.append(feature1)
			nodeInfo.append(feature2)
			nodeInfo.append(feature3)
			
			#print "Node {}: {}".format(index, nodeInfo)
			
			graph.add_edge(0, index)
			graph.node[index]['v'] = nodeInfo
			#cnt += 1
		print ""


if __name__ == '__main__':

	graphDir = '/home/yduan/yueduan/thirdPartyLibAnalysis/graphs/'

	fileName = graphDir + 'db_3.0.6/com.dropbox.core.http.OkHttp3Requestor$AsyncCallback/void_<init>(OkHttp3Requestor$PipedRequestBody).cfg'
	g1 = nx.DiGraph()
	loadGraphFromFile(fileName, g1)


	fileName = graphDir + 'db_3.0.3/com.dropbox.core.http.OkHttp3Requestor$AsyncCallback/void_<init>().cfg'


	#com.dropbox.core.DbxAuthFinish_read(JsonParser).pdg'
	g2 = nx.DiGraph()
	loadGraphFromFile(fileName, g1)
