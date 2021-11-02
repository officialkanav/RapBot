from keras.models import Sequential
from keras.layers import Dense, LSTM, CuDNNLSTM, Bidirectional
from keras.layers import Activation
import tensorflow as tf
batch = 20

class Model:

	def train(self, X_train, X_test, y_train, y_test, num_classes):
		model = Sequential()
		if len(tf.config.list_physical_devices('GPU')) == 0:
			model.add(Bidirectional(LSTM(128, input_shape=(batch, 1))))
		else:
			model.add(Bidirectional(CuDNNLSTM(128, input_shape=(batch, 1))))
		model.add(Dense(num_classes))
		model.add(Activation('softmax'))

		print('Compiling Model')
		model.compile(loss='categorical_crossentropy', metrics = ['accuracy'], optimizer='RMSprop')

		print('Training Model')
		model.fit(X_train, y_train, batch_size=128, epochs=100,validation_data = (X_test,y_test),verbose = 1)

		model.save_weights('my_model_weights.h5')
		model.save('my_model.h5')

		return model
