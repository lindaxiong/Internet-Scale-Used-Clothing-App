from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "Recommended Items")

data = sc.textFile("/tmp/data/logs.txt", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split(";"))   # tell each worker to split each line of its partition at ";"

pages = pairs.map(lambda pair: (pair[1],pair[0])).distinct()    # re-layout log data to swap itemid and userid columns -> (user id, item id)

# view_list = pages.reduceByKey(lambda x,y: x+" " + y + " ")			# groups data into pairs of (user id, list of item ids clicked on)
# coview_list = view_list.map(lambda pair: (pair[0], pair[1].split()))   # split list of item ids


coview_list = pages.join(pages).distinct().filter(lambda pair: int(pair[1][0])!=int(pair[1][1]))  # groups data into pairs of (user id, pairs of coviewed items)

user_list = coview_list.map(lambda pair: (pair[1], pair[0])).reduceByKey(lambda x,y: x+" "+y+" ")	# switches data columns into (pairs of coviewed items, user id) 
user_list = user_list.map(lambda pair: (pair[0], pair[1].split()))									
user_count = user_list.filter(lambda pair: len(pair[1])>=3).map(lambda pair: (pair[0], len(pair[1])))		# filters out pairs of items with less than 3 users who co-clicked, 
#																											   transforms data into pairs of (coviewed pair, count of users who coviewed)


output = user_count.collect()					# print for debugging purposes
for coviewed_pair, user_count in output:
	print ("coviewed_pair %s user_count %s" % (coviewed_pair, user_count))
print("Co-view list done")
sc.stop()