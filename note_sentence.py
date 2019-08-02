import pickle
import csv

file = '/home/sourdip/Notes/Semester2/NLPProject/clicr_data_plain_text/train_json_plain_text.txt'
filename = 'note_sentence_dictionary' 
i = 0
patient_note = {}

with open(file,'r') as f:
	for row in f:
		patient_note[i] = row
		patient_note[i] = patient_note[i].split(".") 
		i = i + 1
		print i
#		if(i == 1):
#			break

#print('  '.join(patient_note[0]).encode('utf-8'))

with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in patient_note.items():
    	for ind,v in enumerate(value):
		if v.strip() != '':
	       		writer.writerow([key,ind,v])

with open(filename, 'wb') as file:
    file.write(pickle.dumps(patient_note))
    file.close()
