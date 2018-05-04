import networkx as nx
import dlib
import distance
import loadGraph
import sys

debug = False

# This function is used to calcuate the similarity between two given graphs
def calSim(g1,g2):
	sim = calSimByedit(g1, g2)
	return sim



def calSimByedit(g1, g2):
	matrix = []
	
	# This list stores the similarities based on feature 1 only
	matrix_string = []

	# this list stores all the statements that can be matched perfectly (similarity == 1 && the only match)
	# perfectMatch = []
	
	matrix_len = max(len(g1), len(g2))
	#visited = {}
	for i in xrange(matrix_len):
		row = []
		row_string = []
		for j in xrange(matrix_len):
			#first compare statements using feature 1 (statement string)
			sim = calSimBB(i, j, g1, g2, 1)
			row_string.append(sim)
			# We have used the string to compare statements. 
			# In case a statement has more than one identical match (similarity == 1)
			# we should use other features to distinguish.
# 			if sim == 1:
# 				sim += calSimBB(i, j, g1, g2, 2)
# 				sim += calSimBB(i, j, g1, g2, 3)

			row.append(sim)
			#visited[(i,j)] = sim
		
		matrix.append(row)
		matrix_string.append(row_string)
	cost = dlib.matrix(matrix)

	mapping = dlib.max_cost_assignment(cost)
	
	for i in xrange(matrix_len):
		if matrix[i][mapping[i]] != 1.0:
			if i < len(g1):
				n1 = g1.node[i]['v'][0:2]
			else:
				n1 = "[-1,'']"
	
			if mapping[i] < len(g2):
				n2 = g2.node[mapping[i]]['v'][0:2]
			else:
				n2 = "[-1,'']"
			print "{}{}".format(n1, n2)
	
	# any mapping that is not 1.0 shall be considered as diff
# 	for i in xrange(matrix_len):
# 		if matrix_string[i][mapping[i]] == 1.0:
# 			continue
# 
# 		if debug:
# 			print i
# 			if i < len(g1):
# 				print g1.node[i]['v']
# 			else:
# 				print "['',0,0]"
# 
# 			if mapping[i] < len(g2):
# 				print g2.node[mapping[i]]['v']
# 			else:
# 				print "['',0,0]"
# 			
# 			print matrix[i][mapping[i]]
# 			print matrix_string[i][mapping[i]]
# 			print "\n"
# 		print mapping
# 		print ""


	sim = caldistance(mapping, matrix)
	return sim


# the parameter (featureNum) means the used feature index. Right now we have three features
def calSimBB(src_id, dst_id, src_g, dst_g, featureNum):

	# take [1:] because the first element is the index, second element is the orignal stmt
	try:
		src_vec = src_g.node[src_id]['v'][1:]
	except:
		src_vec = ['',[],[]]
	try:
		dst_vec = dst_g.node[dst_id]['v'][1:]
	except:
		dst_vec = ['',[],[]]

	if featureNum == 1:
		dst = float(distance.levenshtein(src_vec[0], dst_vec[0])) / max(len(src_vec[0]), len(dst_vec[0]))
		d_BB = 1 - dst
	else:
		# print src_vec[featureNum - 1]
		# print dst_vec[featureNum - 1]
		dst = 0 #(src_vec[featureNum - 1] == dst_vec[featureNum - 1]) and 0 or abs(src_vec[featureNum - 1] - dst_vec[featureNum - 1])
		# print "dst: {}".format(dst)
		d_BB = 1 - dst
		# print "d_BB: {}".format(d_BB)
		# print "\n"

	return d_BB



def caldistance(mapping, node_matrix):
	cost = []
	for i in xrange(len(mapping)):
		cost.append(node_matrix[i][mapping[i]])
	distance = sum(cost) / len(mapping)
	#if distance > 1:
	#	pdb.set_trace()
	return round(distance,4)


# Total of 2 additional arguments
# First argument: path to g1
# Second argument: path to g2
def startDiffing(path1, path2):
	
	g1 = nx.DiGraph()
	loadGraph.loadGraphFromFile(path1, g1)
	
	g2 = nx.DiGraph()
	loadGraph.loadGraphFromFile(path2, g2)

	#print "start comparing!"
	return calSim(g1,g2)

if __name__ == '__main__':

	if len(sys.argv) != 3:
		print "Wrong format!"
		print "This program takes two arguments"
		exit


# 	graphDir_303 = '/home/yduan/yueduan/thirdPartyLibAnalysis/graphs/db_3.0.3/'
# 	graphDir_306 = '/home/yduan/yueduan/thirdPartyLibAnalysis/graphs/db_3.0.6/'
# 
# 	oldFile = graphDir_303 + 'com.dropbox.core.http.OkHttp3Requestor$AsyncCallback/void_<init>().cfg'
# 	newFile = graphDir_306 + 'com.dropbox.core.http.OkHttp3Requestor$AsyncCallback/void_<init>(OkHttp3Requestor$PipedRequestBody).cfg'
	
	oldFile = sys.argv[1]
	newFile = sys.argv[2]

# 	print "Comparing: {} with {}".format(oldFile, newFile)
	ret = startDiffing(oldFile, newFile)
	print "{}".format(ret)
	

