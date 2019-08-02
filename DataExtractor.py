import csv
import re

eligibility_criteria_filename = 'cardio_data_final_14thOct.csv'
output_eligibility_criteria_filename = 'cardio_data_final_14thOct_output.csv'
output_result_filename = 'results.csv'
notes_data = 'clicr_data_plain_text/train_json_plain_text.txt'

regex = re.compile('inclusion criteria:(.*)')
regex1 = re.compile('(.*?)exclusion criteria')
regex2 = re.compile('1\. .*2\. .*')
lines = []
lines2 = []
'''
with open(output_eligibility_criteria_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if regex2.search(row[1]) is not None:
            lines.append(row)

with open('refined.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(lines)
'''

with open(eligibility_criteria_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count = 1
        else:
            ec = row[4]
            nctid = row[0]
            ec_split = []
            x = regex.search(ec)
            if x is not None:
                ec = x.group(1)
                x = regex1.search(ec)
                if x is not None:
                    ec = x.group(1)
                if regex2.search(ec) is not None:
                    lines2.append([nctid,ec])
                    continue
                ec_split = ec.split(' - ')
                if len(ec_split) <= 4:
                    continue
                for each in ec_split:
                    if each == '':
                        continue
                    lines.append([nctid,each])


with open(output_eligibility_criteria_filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(lines)

with open('refined.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(lines2)

'''
def find_word_overlap(sentence, ec):
    ec = ec.lower().split()
    ec = list(set(ec))
    sentence = sentence.lower().split()
    res = 0
    for word in ec:
        res += sentence.count(word)

    return float(res) / len(sentence) if len(sentence)>0 else 0


ec_list = []

with open(output_eligibility_criteria_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        nctid = row[0]
        ec = row[1]
        ec_list.append((nctid, ec))


print "Created eligibility criteria list"

sentence_list = []

with open(notes_data) as notes:
    for index,note in enumerate(notes):
        sentences = note.split('.')
        for sentence in sentences:
            sentence_list.append((index+1, sentence))

print "Created notes list"

with open(output_result_filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    for sentence in sentence_list:
        for ec in ec_list:
            res = find_word_overlap(sentence[1], ec[1])
            if res >= 0.7:
                writer.writerow([sentence[0], sentence[1], ec[0], ec[1], res])
'''

'''
indexer = engine.Indexer() 
indexer.set('name', stored=True) 
indexer.set('text', engine.Field.Text)

with open(notes_data) as notes:
    for index,note in enumerate(notes):
        sentences = note.split('.')
        for index1, sentence in enumerate(sentences):
            indexer.add(name=str(index)+'.'+str(index1), text=sentence)

indexer.commit()
hits = indexer.search('treatment with 75 mg aspirin once daily')
print len(hits), hits.count'''


set1 = []
with open(output_eligibility_criteria_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        set1.append(row[0])
    print len(set(set1))