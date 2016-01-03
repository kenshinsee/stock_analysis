import random,pprint

file_dir = 'D:\\workspace\\Stock\\test_file'
file_names = ['file1.csv', 'file2.csv']

def gen_ids(range, num):
	#id,ver
	dataset = {}
	start_point = range[0]
	end_point = range[1]
	iter = 1
	while iter <= num:
		id = random.randint(start_point, end_point)
		if id in dataset:
			dataset[id].append(max(dataset[id]) + 1)
		else:
			dataset[id] = [1]
		iter += 1
	return dataset


if __name__ == "__main__":
	datasets = []
	mergeset = {}
	# generate data
	for file in file_names:
		dataset = gen_ids([1,10000],100000)
		datasets.append(dataset)
		print "start to write to " + file
		fh = open(file_dir + '\\' + file, "w")
		for id in dataset:
			for ver in dataset[id]:
				fh.write(str(id) + "," + str(ver) + "\n")
		fh.close()
	
	# merge data into dict
	data1 = datasets[0]
	data2 = datasets[1]
	
	for id in data1:
		mergeset[id] = {}
		for ver in data1[id]:
			mergeset[id][ver] = []
			mergeset[id][ver].append("data1")
	
	for id in data2:
		if not id in mergeset:
			mergeset[id] = {}
		for ver in data2[id]:
			if not ver in mergeset[id]:
				mergeset[id][ver] = []
			mergeset[id][ver].append("data2")
			
	# pprint.pprint(data1)
	# pprint.pprint(data2)
	# pprint.pprint(mergeset)
	
	# compare data
	for id in mergeset:
		for ver in mergeset[id]:
			if len(mergeset[id][ver]) == 2: 
				continue
			else:
				print "id:" + str(id) + " | ver:" + str(ver) + " only exists in " + mergeset[id][ver][0]
				
				