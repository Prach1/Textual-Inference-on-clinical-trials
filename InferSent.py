#!/usr/bin/env python
# coding: utf-8

# In[4]:


import csv
import re

eligibility_criteria_filename = '../../cardio_data_final_14thOct.csv'
output_eligibility_criteria_filename = 'cardio_data_final_14thOct_output_exclusion.csv'

regex = re.compile('exclusion criteria:(.*)')
regex2 = re.compile('1\. .*2\. .*')
lines = []
lines2 = []

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


# In[2]:


import pandas as pd
from collections import defaultdict
import pickle
import os


# Load EC

# In[6]:


ec_datapath = "../EligibilityCriteria.csv"
ec_data = pd.read_csv(ec_datapath)


# Load Notes

# In[4]:


notes_datapath = "../ClinicalNotes.csv"
notes_data = pd.read_csv(notes_datapath)


# 

# In[7]:


exclusion_ec_filepath = "../cardio_data_final_14thOct_output_exclusion.csv"
exclusion_ec_data = pd.read_csv(exclusion_ec_filepath)


# # Reduce number of ec

# In[25]:


f = open('ec_filtered.txt' , 'w')
ec_dict = {}
for row in range(ec_data.shape[0]):
	try:
		trial_id = ec_data.iloc[row,0]
		ec = ec_data.iloc[row,1]
		f.write(trial_id + '::' + ec + '\n')
		if trial_id not in ec_dict:
			ec_dict[trial_id] = 1
			if len(ec_dict) == 50:
				break

	except UnicodeDecodeError:
		print row

ec_dict = None
f.close()


# Select ec

# # Reduce number of Notes

# In[26]:


f = open('notes_filtered.txt' , 'w')
notes_dict = {}
for row in range(notes_data.shape[0]):
	try:
		note_id = notes_data.iloc[row,0]
		note = notes_data.iloc[row,2]
		f.write(str(note_id) + '::' + note + '\n')
		if note_id not in notes_dict:
			notes_dict[note_id] = 1
			if len(notes_dict) == 100:
				break

	except UnicodeDecodeError:
		print row

notes_dict = None
f.close()


# FK reading

# In[11]:


f = open('notes_read_metrics.txt' , 'w')
notes_dict = {}
prev_note_id = None
sentences = []
for row in range(notes_data.shape[0]):
    try:
        note_id = notes_data.iloc[row,0]
        note = notes_data.iloc[row,2]
        
        if prev_note_id != note_id:
            if prev_note_id is not None:
                note_line = ' . '.join(sentences)
                print note_line
                sentences_num = len(sentences)
                words = note_line.split(' ')
                words = [x for x in words if x.strip()!='.' and x.strip()!='']
                words_num = len(words)
                letters_num = sum([len(x) for x in words])
                score = 206.835 - (1.015 * (float(words_num)/sentences_num)) - (84.6 * (float(letters_num)/words_num))
                #print words
                break
                print words_num,sentences_num,letters_num,words_num,score
                f.write(str(prev_note_id) + '::' + str(score) + '\n')
            sentences = []
            prev_note_id = note_id
        sentences.append(note)

    except UnicodeDecodeError:
        print row


f.close()


# In[5]:


f = open('notes_hist.csv' , 'w')
notes_dict = {}
prev_note_id = None
sentences = []
for row in range(notes_data.shape[0]):
    try:
        note_id = notes_data.iloc[row,0]
        note = notes_data.iloc[row,2]
        
        if prev_note_id != note_id:
            if prev_note_id is not None:
                f.write(str(prev_note_id) + ',' + str(len(sentences)) + '\n')
            sentences = []
            prev_note_id = note_id
        sentences.append(note)

    except UnicodeDecodeError:
        print row


f.close()


# In[8]:


f = open('ec_hist.csv' , 'w')
prev_trial_id = None
sentences = []
f.write('Trial id,length\n')
for row in range(ec_data.shape[0]):
    try:
        trial_id = ec_data.iloc[row,0]
        ec = ec_data.iloc[row,1]
        
        if prev_trial_id != trial_id:
            if prev_trial_id is not None:
                f.write(str(prev_trial_id) + ',' + str(len(sentences)) + '\n')
            sentences = []
            prev_trial_id = trial_id
        sentences.append(ec)

    except UnicodeDecodeError:
        print row


f.close()


# # Create input.txt and index.txt
# input.txt - <note>\t<ec>
# index.txt - <trial_id>\t<note_d>

# In[27]:


f_ec = open('ec_filtered.txt')
f_note = open('notes_filtered.txt')

out_f = open('input.txt', 'w')
out_fi = open('index.txt', 'w')
index = {}
count = 0
for line_ec in f_ec:
    if line_ec.strip() == '':
        continue
    trial_id, ec = line_ec.strip().split('::', 1)
    f_note = open('notes_filtered.txt')
    for line_note in f_note:
        if line_note.strip() == '':
            continue
        note_id, note = line_note.strip().split('::', 1)
        out_f.write(note + '\t' + ec + '\n')
        out_fi.write(trial_id + '\t' + note_id + '\n')
        
    f_note.close()
out_fi.close()
out_f.close()
f_ec.close()


# # Create files
# max line numbers in each file must be 100000
# 

# In[31]:


max_line_num = 100000
out_f = open('input.txt')
count = 0
f_num = 1
for line in out_f:
    line = line.strip()
    if count == 0:
        f = open('input/input_'+str(f_num)+'.txt' , 'w')
        f_num += 1
    count += 1
    f.write(line+'\n')
    if count == max_line_num:
        f.close()
        count = 0

out_f.close()


# In[12]:


input_dir = '../../30-03-2019/mednli/out/out'
output = open('../../30-03-2019/mednli/out/out.txt', 'w')
for i in range(1,37):
    f_name = input_dir + str(i)
    with open(f_name) as f:
        for line in f:
            res,_ = line.strip().split('::',1)
            output.write(res+'\n')
output.close()


# In[11]:


input_dir = '../../30-03-2019/mednli/input/input_'
output = open('../../30-03-2019/mednli/input/input.txt', 'w')
c = 0
for i in range(1,37):
    f_name = input_dir + str(i) + '.txt'
    with open(f_name) as f:
        for line in f:
            line = line.strip()
            output.write(line+'\n')
output.close()


# In[17]:


input_file_path = open('../../30-03-2019/mednli/input/input.txt')
output_file_path = open('../../30-03-2019/mednli/out/out.txt')
out = open('../../30-03-2019/mednli/result1.txt', 'w')
for line in input_file_path:
    note,ec = line.strip().split('\t')
    class_ = output_file_path.readline().strip()
    out.write(note+'$######$'+ec+'$######$'+class_+'\n')
out.close()
input_file_path.close()
output_file_path.close()


# In[18]:


result_file = open('../../30-03-2019/mednli/result1.txt')
index_file = open('index.txt')
out = open('../../30-03-2019/mednli/result.txt', 'w')

for line in result_file:
    line = line.strip()
    trial_id,note_id = index_file.readline().strip().split('\t',1)
    out.write(trial_id+'$######$'+note_id + '$######$' + line + '\n')

out.close()
result_file.close()
index_file.close()


# In[28]:


out = open('../../30-03-2019/mednli/ec_note_match.txt', 'w')
with open('../../30-03-2019/mednli/result.txt') as f:
    prev_trial_id_note_id = None
    ent_count = 0
    con_count = 0
    for line in f:
        line = line.strip()
        trial_id,note_id,note,ec,class_ = line.split('$######$')
        note_id = '0'*(8-len(note_id)) + note_id
        
        trial_id_note_id = trial_id+'$######$'+note_id
        if prev_trial_id_note_id != trial_id_note_id:
            if prev_trial_id_note_id is not None:
                out.write(prev_trial_id_note_id+'$######$'+str(float(ent_count)/(ent_count+con_count))+'\n')
            ent_count = 0
            con_count = 0
            prev_trial_id_note_id = trial_id_note_id
        if class_ == 'Entailment':
            ent_count += 1
        else:
            con_count+=1
if prev_trial_id_note_id == trial_id_note_id:
    out.write(prev_trial_id_note_id+'$######$'+str(float(ent_count)/(ent_count+con_count))+'\n')
out.close()


# In[30]:


out = open('../../30-03-2019/mednli/trial_note.txt', 'w')
with open('../../30-03-2019/mednli/ec_note_match_sorted.txt') as f:
    prev_trial_id_note_id = None
    count = 0
    summ = 0
    note_list = []
    for line in f:
        line = line.strip()
        trial_id,note_id,match = line.split('$######$')
        match = float(match)
        
        trial_id_note_id = trial_id + '$######$' + note_id
        if prev_trial_id_note_id != trial_id_note_id:
            if prev_trial_id_note_id is not None:
                out.write(prev_trial_id_note_id+'$######$'+str(float(summ)/count)+'\n')
            #note_list = []
            count = 0
            summ = 0
            prev_trial_id_note_id = trial_id_note_id
        count += 1
        summ += match
        #if match > THRESHOLD:
        #    note_list.append(note_id)
if prev_trial_id_note_id == trial_id_note_id:
    out.write(prev_trial_id_note_id+'$######$'+str(float(summ)/count)+'\n')
out.close()


# In[3]:


out = open('../../30-03-2019/mednli/trial_notelist_0.5.txt', 'w')
THRESHOLD = 0.6
with open('../../30-03-2019/mednli/trial_note.txt') as f:
    prev_trial_id = None
    note_list = []
    for line in f:
        line = line.strip()
        trial_id,note_id,match = line.split('$######$')
        match = float(match)
        
        if prev_trial_id != trial_id:
            if prev_trial_id is not None:
                note_list = [str(int(x)) for x in note_list]
                out.write(prev_trial_id+'::'+','.join(note_list)+'\n')
            note_list = []
            prev_trial_id = trial_id
        if match > THRESHOLD:
            note_list.append(note_id)
if prev_trial_id == trial_id:
    note_list = [str(int(x)) for x in note_list]
    out.write(prev_trial_id+'::'+','.join(note_list)+'\n')
out.close()


# In[9]:


in_file = open("../../30-03-2019/mednli/trial_notelist_0.5.txt")
ec_dict = {}
for line in in_file:
    trialid,note_id_list = line.strip().split("::",1)
    note_id_list = note_id_list.split(',')
    ec_dict[trialid] = note_id_list
in_file.close()


# In[13]:


out_file = open("../../30-03-2019/mednli/trial_notelist_0.5_hist.csv", 'w')
#ec_dict = {}
out_file.write('Trialid,Note id list\n')
for trialid in ec_dict:
    out_file.write(trialid + ',' + str(len(ec_dict[trialid]))+'\n')
out_file.close()


# In[21]:


f = open('ec_filtered_exclusion.txt' , 'w')

for row in range(exclusion_ec_data.shape[0]):
	try:
		trial_id = exclusion_ec_data.iloc[row,0]
		ec = exclusion_ec_data.iloc[row,1]
		if trial_id in ec_dict:
			f.write(trial_id + '::' + ec + '\n')
            
	except UnicodeDecodeError:
		print row

f.close()


# In[27]:


ec_file = open('ec_filtered_exclusion.txt')
f = open('note_filtered_exclusion.txt' , 'w')
f_i = open('exclusion_index.txt' , 'w')


for line in ec_file:
    trialid,ec = line.strip().split("::",1)
    note_list = ec_dict[trialid]
    note_file = open('notes_filtered.txt')
    for line_n in note_file:
        if len(line_n.strip())==0:
            continue
        note_id, sent = line_n.strip().split("::",1)
        if note_id in note_list:
            f.write(sent+'\t'+ec+'\n')
            f_i.write(trialid+'::'+note_id+'\n')
    note_file.close()
    
ec_file.close()
f.close()
f_i.close()


# In[28]:


max_line_num = 100000
out_f = open('note_filtered_exclusion.txt')
count = 0
f_num = 1
for line in out_f:
    line = line.strip()
    if count == 0:
        f = open('input/input_ec_'+str(f_num)+'.txt' , 'w')
        f_num += 1
    count += 1
    f.write(line+'\n')
    if count == max_line_num:
        f.close()
        count = 0

out_f.close()


# In[40]:


input_dir = '../../30-03-2019/mednli/out/out_ec_'
output = open('../../30-03-2019/mednli/out/out_ec.txt', 'w')
for i in range(1,5):
    f_name = input_dir + str(i)
    with open(f_name) as f:
        for line in f:
            res,_ = line.strip().split('::',1)
            output.write(res+'\n')
output.close()


# In[41]:


input_dir = '../../30-03-2019/mednli/input/input_ec_'
output = open('../../30-03-2019/mednli/input/input_ec.txt', 'w')
c = 0
for i in range(1,5):
    f_name = input_dir + str(i) + '.txt'
    with open(f_name) as f:
        for line in f:
            line = line.strip()
            output.write(line+'\n')
output.close()


# In[42]:


input_file_path = open('../../30-03-2019/mednli/input/input_ec.txt')
output_file_path = open('../../30-03-2019/mednli/out/out_ec.txt')
out = open('../../30-03-2019/mednli/result1_ec.txt', 'w')
for line in input_file_path:
    note,ec = line.strip().split('\t')
    class_ = output_file_path.readline().strip()
    out.write(note+'$######$'+ec+'$######$'+class_+'\n')
out.close()
input_file_path.close()
output_file_path.close()


# In[43]:


result_file = open('../../30-03-2019/mednli/result1_ec.txt')
index_file = open('exclusion_index.txt')
out = open('../../30-03-2019/mednli/result_ec.txt', 'w')

for line in result_file:
    line = line.strip()
    trial_id,note_id = index_file.readline().strip().split('::',1)
    out.write(trial_id+'$######$'+note_id + '$######$' + line + '\n')

out.close()
result_file.close()
index_file.close()


# In[45]:


out = open('../../30-03-2019/mednli/ec_note_match_exclusion.txt', 'w')
with open('../../30-03-2019/mednli/result_ec.txt') as f:
    prev_trial_id_note_id = None
    ent_count = 0
    con_count = 0
    for line in f:
        line = line.strip()
        trial_id,note_id,note,ec,class_ = line.split('$######$')
        note_id = '0'*(8-len(note_id)) + note_id
        
        trial_id_note_id = trial_id+'$######$'+note_id
        if prev_trial_id_note_id != trial_id_note_id:
            if prev_trial_id_note_id is not None:
                out.write(prev_trial_id_note_id+'$######$'+str(float(ent_count)/(ent_count+con_count))+'\n')
            ent_count = 0
            con_count = 0
            prev_trial_id_note_id = trial_id_note_id
        if class_ == 'Contradiction':
            ent_count += 1
        else:
            con_count+=1
if prev_trial_id_note_id == trial_id_note_id:
    out.write(prev_trial_id_note_id+'$######$'+str(float(ent_count)/(ent_count+con_count))+'\n')
out.close()


# In[46]:


out = open('../../30-03-2019/mednli/trial_note_exclusion.txt', 'w')
with open('../../30-03-2019/mednli/ec_note_match_exclusion_sorted.txt') as f:
    prev_trial_id_note_id = None
    count = 0
    summ = 0
    note_list = []
    for line in f:
        line = line.strip()
        trial_id,note_id,match = line.split('$######$')
        match = float(match)
        
        trial_id_note_id = trial_id + '$######$' + note_id
        if prev_trial_id_note_id != trial_id_note_id:
            if prev_trial_id_note_id is not None:
                out.write(prev_trial_id_note_id+'$######$'+str(float(summ)/count)+'\n')
            #note_list = []
            count = 0
            summ = 0
            prev_trial_id_note_id = trial_id_note_id
        count += 1
        summ += match
        #if match > THRESHOLD:
        #    note_list.append(note_id)
if prev_trial_id_note_id == trial_id_note_id:
    out.write(prev_trial_id_note_id+'$######$'+str(float(summ)/count)+'\n')
out.close()


# In[48]:


out = open('../../30-03-2019/mednli/trial_notelist_0.5_exclusion.txt', 'w')
THRESHOLD = 0.2
with open('../../30-03-2019/mednli/trial_note_exclusion.txt') as f:
    prev_trial_id = None
    note_list = []
    for line in f:
        line = line.strip()
        trial_id,note_id,match = line.split('$######$')
        match = float(match)
        
        if prev_trial_id != trial_id:
            if prev_trial_id is not None:
                note_list = [str(int(x)) for x in note_list]
                out.write(prev_trial_id+'::'+','.join(note_list)+'\n')
            note_list = []
            prev_trial_id = trial_id
        if match > THRESHOLD:
            note_list.append(note_id)
if prev_trial_id == trial_id:
    note_list = [str(int(x)) for x in note_list]
    out.write(prev_trial_id+'::'+','.join(note_list)+'\n')
out.close()


# In[ ]:


f_in = open('../../30-03-2019/mednli/trial_notelist_0.5.txt')
f_ex = open('../../30-03-2019/mednli/trial_notelist_0.5_exclusion.txt')
out = open('../../30-03-2019/mednli/result_final.txt', 'w')

f_in_dict = {}
for line in f_in:
    trial_id,note_list = line.strip().split('::',1)
    note_list = set()

