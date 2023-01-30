'''Q1 Create a function to read csv file and convert to python data structure (dict, list, set)
first_name, last_name,roll
John,Ken,11
Ronny,Baggs,12
Sam,Shone,13 '''
ef read_csv(dtype):
	file = open('data.csv','r')
	fh = file.readlines()
	fh = [str(i).split(',') for i in fh]
	if dtype=='list':
		return fh[1:]
	if dtype=='dict':
		heads=fh[0]
		ans=dict()
		for i in range(1,len(fh)):
			ans[i]=dict()
			for j in range(len(heads)):
				ans[i][heads[j]]=fh[i][j]
		return ans
	if dtype=='set':
		ans=set()
		for i in fh[1:]:
			ans.add(tuple(i))
		return ans