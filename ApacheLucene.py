from lupyne import engine
import lucene
import csv

base_dir = '/home/sourdip/Notes/Semester2/NLPProject/CodeBase/'
note_csv_file = 'ClinicalNotes.csv'
ec_csv_file = 'EligibilityCriteria.csv'

output_file_approach2 = 'LuceneResults_min.csv'

lucene.initVM()

# Create indexes - ONE TIME EXECUTION
indexer = engine.Indexer('clicr_index')
'''indexer.set('id', stored=True) 
indexer.set('text', engine.Field.Text)

with open(base_dir + note_csv_file) as notes:
	csv_reader = csv.reader(notes, delimiter=',')
	for row in csv_reader:
		if int(row[0]) == 500:
			break

		indexer.add(id=str(row[0])+'.'+str(row[1]), text=row[2])


indexer.commit()  
'''

print 'Committed'


ec_list = []
with open(base_dir + ec_csv_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for ind, row in enumerate(csv_reader):
    	if ind == 200:
    		break
        nctid = row[0]
        ec = row[1]
        ec_list.append((nctid, ec))

i = 0
index = 0


with open(base_dir + output_file_approach2, 'w') as csv_file:
	writer = csv.writer(csv_file)

	for nctid,ec in ec_list:
		i += 1
			

		ec = ec.replace('/','').replace(':','').replace('-','').replace('*','').replace('(','').replace(')','').replace('[','').replace(']','').replace('?','').replace('{','').replace('}','').replace('+','').replace('^','')
		print i,ec
		hits = indexer.search('text:'+ec)
		result = {}

		for hit in hits:
			doc_id, sentence_id = hit['id'].split('.')
			if doc_id not in result:
				result[doc_id] = [(hit.score, sentence_id)]
			else:
				result[doc_id].append((hit.score, sentence_id))


		for key in result:
			result[key] = list(set(result[key]))
			result[key].sort(reverse=True)
			result[key] = result[key][:5]
			
			result[key] = [int(each[1]) for each in result[key]]
			writer.writerow([nctid, ec, key, result[key]])



#if i != 0:
#	with open('output_result_lucene_'+index+'.csv', 'w') as csv_file:
#	    writer = csv.writer(csv_file)
#	    writer.writerows(output)
