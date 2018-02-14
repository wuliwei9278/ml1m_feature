import math
import sys
import gensim
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# this line doesn't load the trained model 
from gensim.models.keyedvectors import KeyedVectors

#words = ['access', 'aeroway', 'airport']

path_to_model = "GoogleNews-vectors-negative300.bin"
# this is how you load the model
model = KeyedVectors.load_word2vec_format(path_to_model, binary=True)

# to extract word vector
print(model[words[0]])  #access

def words2vec(model, words):
	res = np.zeros(300) # embedding dim is 300
	cnt = 0
	for word in words:
		try:
			word_v = model[word]
		except:
			continue
		# normalize word vector 
		word_norm = np.sqrt(np.sum(np.square(word_v)))
		word_v = word_v / word_norm
		# can verify that np.linalg.norm(word_v) close to 1
		res += word_v
		cnt += 1
	res /= cnt
	return res 

# store dictionary with movie_id as key and features as list of vec
d = {}
with open("movies.dat") as f:
	for line in f:
		#print(line)
		l = line.split('::')
		movie_id = l[0]
		words_l = l[1].split()
		words = []
		for i in range(len(words_l) - 1):
			words.append(words_l[i])
		year = words_l[-1][-5:-1] #'(1995)'
		themes = l[2].strip().split('|')
		words_v = words2vec(model, words)
		themes_v = words2vec(model, themes)
		d[movie_id] = [words_v, themes_v, year, 0, 0]


with open("ratings.dat") as f:
	for line in f:
		l = line.split('::')
		movie_id = l[1]
		d[movie_id][3] += 1
		d[movie_id][4] += int(l[2])

cnt_max = 0
for movie in d:
	cnt_max = max(d[movie][3], cnt_max)

for movie in d:
	try:
		d[movie][4] /= float(d[movie][3])
		d[movie][4] /= 5
		d[movie][3] /= float(cnt_max)
	except:
		continue

import cPickle as cp
with open("movies_feature.cp", 'wb') as f:
	cp.dump(d, f)

with open("movies_feature.cp", 'rb') as f:
	d = cp.load(f)
#from keras.utils import to_categorical
years = set()
for movie in d:
	years.add(d[movie][2])

# Dimension is too high, has to implement myself
# encoded = to_categorical(np.array(years))
# cc = 0
# for movie in d:
# 	d[movie][2] = encoded[cc]
# 	cc += 1

encoder = {}
cc = 0
for year in years:
	encoder[year] = np.zeros(len(years))
	encoder[year][cc] = 1.0
	cc += 1
for movie in d:
	d[movie][2] = encoder[d[movie][2]]


	



