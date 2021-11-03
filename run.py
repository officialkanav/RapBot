import os
import keras
import numpy as np
import sys
import json
from data.ScrapLyrics import ScrapLyrics
from data.PreprocessData import PreprocessData
from model.Model import Model

if __name__ == "__main__":
	model = None
	charsToInt = None
	intToChars = None
	
	if os.path.isfile('my_model.h5'):
		print('Model weights are already present')

		model = keras.models.load_model("my_model.h5")

		f = open('intToChars.json',)
		intToChars = json.load(f)

		f = open('charsToInt.json',)
		charsToInt = json.load(f)
	else:
		artist = str(input('Enter artist name: ')).lower()

		lyrics = ScrapLyrics(artist).create_lyrics_file()

		X_train, X_test, y_train, y_test, intToChars, charsToInt, num_classes = \
			PreprocessData().preprocess(lyrics)
		
		model = Model().train(X_train, X_test, y_train, y_test, num_classes)

		with open('intToChars.json', 'a',encoding="utf-8") as file:
			file.write(json.dumps(intToChars))
		with open('charsToInt.json', 'a',encoding="utf-8") as file:
			file.write(json.dumps(charsToInt))
	
	input_data = str(input('Give input string of around 20 characters: ')).lower()

	if len(input_data) > 20:
		input_data = input_data[0:20]
	else:
		input_data = input_data.ljust(20, ' ')

	for i in range(400):  
		start = [charsToInt[ch] for ch in input_data]
		start = np.asarray(start)
		start = start.reshape((1,20,1))
		start = start/30 
		next = model.predict(start)
		next = np.argmax(next)
		next_ch = intToChars[str(next)]
		if next_ch != '$':
			sys.stdout.write(next_ch)
		else:
			print('')
		input_data = input_data[1:]
		input_data = input_data + next_ch
