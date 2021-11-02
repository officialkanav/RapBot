from data.ScrapLyrics import ScrapLyrics
from data.PreprocessData import PreprocessData
from model.Model import Model

if __name__ == "__main__":
	# artist = str(input('Enter artist name')).lower()
	# lyrics = ScrapLyrics(artist).create_lyrics_file()
	# X_train, X_test, y_train, y_test, intToChars, num_classes = \
	# 	PreprocessData().preprocess(lyrics)
	# model = Model().train(X_train, X_test, y_train, y_test, num_classes)
	import tensorflow as tf
	print(tf.config.list_physical_devices('GPU'))


