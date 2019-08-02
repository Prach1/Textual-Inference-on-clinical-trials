import pickle

file = open('incl_crit_list_3rdMarch.p', 'rb')
res = pickle.load(file)

for key in res:
	print key, res[key]