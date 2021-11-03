import numpy as np
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

batch = 20

class PreprocessData:
	def get_char_list(self, lyrics):
		lyrics = lyrics.lower()
		# $ represents new line
		lyrics = lyrics.replace('\n','$')
		char_list = []
		for i,x in enumerate(lyrics):
			if x.isdigit() or (x not in['$','?','.',' ',' \ '] and \
				not x.isalpha()):
				pass
			else:
				char_list.append(x)
		return char_list

	def preprocess(self, lyrics):
		print('Preprocessing data...')
		lyrics = self.get_char_list(lyrics)

		chars = sorted(list(set(lyrics)))
		num_classes = len(chars)
		intToChars = dict((i, c) for i, c in enumerate(chars))
		charsToInt = dict((i, c) for c, i in enumerate(chars))
		lyrics_size = len(lyrics)
		X = []
		y = []

		for i in range(0, lyrics_size - batch - 1):
			tempX = lyrics[i:(i+batch)]
			tempX = [charsToInt[ch] for ch in tempX]
			X.append(tempX)
			y.append(charsToInt[lyrics[i+batch]])
		
		X = np.reshape(X, (len(y),batch,1))
		y = np.reshape(y, (len(y),1))
		X = X/num_classes

		labels = np_utils.to_categorical(y, num_classes=num_classes, dtype='float32')
		
		X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.10)
		
		print('Preprocessing complete.')

		return X_train, X_test, y_train, y_test, intToChars, charsToInt, num_classes

