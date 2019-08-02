import pickle
import csv
import random

threshold = 0.9

base_dir = '/home/sourdip/Notes/Semester2/NLPProject/CodeBase/Output/'
ec_pickle_file = 'EligibilityCriteriaConcepts.p'
ec_csv_file = 'EligibilityCriteria.csv'
ec_concepts_file = 'EligibilityCriteriaConcepts.csv'

note_pickle_file = 'ClinicalNotesConcepts.p'
note_csv_file = 'ClinicalNotes.csv'
note_concepts_file = 'ClinicalNotesConcepts.csv'

output_file_approach3 = 'UMLSConceptsResults_threshold_min.csv'
output_file_approach4 = 'UMLSConceptsResultsSimilarity_threshold_min.csv'
output_filtered = 'output_filtered.csv'

lucene_output = 'LuceneResults_min.csv'

#CODE TO CREATE EC CONCEPTS CSV FILE

with open(base_dir + ec_pickle_file) as f:
	pickle_obj = pickle.load(f)


with open(base_dir + ec_concepts_file, 'w') as csv_file:
	writer = csv.writer(csv_file)
	with open(base_dir + ec_csv_file) as f:
		csv_reader = csv.reader(f, delimiter=',')
		lin_num = 0
		for row in csv_reader:
			lin_num += 1
			writer.writerow( [row[0], row[1], pickle_obj[lin_num]] )






#CODE TO CREATE NOTES CONCEPTS CSV FILE

with open(base_dir + note_pickle_file) as f:
	pickle_obj = pickle.load(f)

with open(base_dir + note_concepts_file, 'w') as csv_file:
	writer = csv.writer(csv_file)
	with open(base_dir + note_csv_file) as f:
		csv_reader = csv.reader(f, delimiter=',')
		lin_num = 0
		for row in csv_reader:
			lin_num += 1
			writer.writerow( [row[0], row[1], row[2], pickle_obj[lin_num]] )
			if lin_num %1000 == 0:
				print lin_num




#CODE TO COMPUTE OUTPUT CSV FILE - Approach 3

# with open(base_dir + output_file_approach3, 'w') as output:
# 	writer = csv.writer(output)


# 	with open(base_dir + ec_concepts_file) as ec_file:
# 		csv_reader_ec = csv.reader(ec_file, delimiter=',')
# 		for lin_num, row_ec in enumerate(csv_reader_ec):

# 			#print lin_num

# 			nctid, criteria_text, ec_concept_list = row_ec[0], row_ec[1], row_ec[2]

# 			prev_note_id = 0
# 			score_list = []

# 			print lin_num

# 			if lin_num == 200:
# 				break;

# 			with open(base_dir + note_concepts_file) as note_file:
# 				csv_reader_notes = csv.reader(note_file, delimiter=',')

# 				for row_note in csv_reader_notes:
# 					note_id, sentence_num, sentence_text, note_concept_list = int(row_note[0]), int(row_note[1]),row_note[2], row_note[3]
# 					#print note_id, prev_note_id, lin_num

# 					# New note started
# 					if note_id != prev_note_id:
# 						#DO JOB
						
# 						score_list.sort(reverse=True)
# 						score_list = [each for each in score_list if each[0] >= threshold]
# 						score_list = [each[1] for each in score_list]

# 						writer.writerow([nctid, criteria_text, prev_note_id, score_list])

# 						score_list = []
# 						prev_note_id = note_id


# 					if note_id == 500:
# 						break

# 					score = len(set(ec_concept_list).intersection(set(note_concept_list)))
# 					score = float(score) / float(len(ec_concept_list))
# 					score_list.append((score, sentence_num))


#length = 0


#CODE TO COMPUTE OUTPUT CSV FILE - Approach 4

with open(base_dir + output_file_approach4, 'w') as output:
	writer = csv.writer(output)


	with open(base_dir + ec_concepts_file) as ec_file:
		csv_reader_ec = csv.reader(ec_file, delimiter=',')
		for lin_num, row_ec in enumerate(csv_reader_ec):

			print lin_num

			nctid, criteria_text, ec_concept_list = row_ec[0], row_ec[1], row_ec[2]

			prev_note_id = 0
			score_list = []

			if lin_num == 200:
				break;


			with open(base_dir + note_concepts_file) as note_file:
				csv_reader_notes = csv.reader(note_file, delimiter=',')

				for row_note in csv_reader_notes:
					note_id, sentence_num, sentence_text, note_concept_list = int(row_note[0]), int(row_note[1]),row_note[2], row_note[3]
					#print note_id, prev_note_id, lin_num

					# New note started
					if note_id != prev_note_id:
						#DO JOB
						
						score_list.sort(reverse=True)
						# score_list = score_list[:5]
						# score_list = [each[1] for each in score_list]

						score_list = [each for each in score_list if each[0] >= threshold]
						score_list = [each[1] for each in score_list]

						#print(score_list)

						if len(score_list) > 5:
							writer.writerow([nctid, criteria_text, prev_note_id, score_list])
							length += 1

						score_list = []
						prev_note_id = note_id


					if note_id == 500:
						break

					score = len(set(ec_concept_list).intersection(set(note_concept_list)))
					score = float(score) / float(len(set(ec_concept_list).union(set(note_concept_list))))
					score_list.append((score, sentence_num))



length = 14032

with open(base_dir + lucene_output) as f:
	csv_reader = csv.reader(f, delimiter=',')
	rand_int = random.sample(range(length), 100)
	with open(base_dir + output_filtered, 'w') as o:
		writer = csv.writer(o)
		for ind,row in enumerate(csv_reader):
			if ind in rand_int:
				writer.writerow(row)





with open(base_dir + output_file_approach3) as f:
	csv_reader = csv.reader(f, delimiter=',')
	for i,row in enumerate(csv_reader):
		print row
		break

