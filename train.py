"""
Train RNN, save weight in HDF5 file
"""

import numpy as np
import tensorflow as tf

from utils import *
from network import *

def train():
	notes = get_notes()
	
	# Get different notes
	num_pitch = len(set(notes))
	
	network_input, network_output = prepare_sequences(notes, num_pitch)
	model = network_model(network_input, num_pitch)
	filepath = "weights.{epoch:02d}-{loss:.4f}.hdf5"
	
	# Use checkpoint File to save Weights
	# When Loss is satisfied, we can stop training anytime
	checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor = "loss", verbose = 0,
													save_best_only = True,
													mode = "min")
	callbacks_list = [checkpoint]
	
	# use 'fit' to train
	model.fit(network_input, network_output, epochs = 100, batch_size = 60, callbacks = callbacks_list)
	

def prepare_sequences(notes, num_pitch):
	"""
	Prepare sequences needed in training
	"""
	sequence_length = 80	# the length of a training sequence
	
	# Get every note
	pitch_names = sorted(set(item for item in notes))
	
	# Dictory: note -> integer
	pitch_to_int = dict((pitch, num) for num, pitch in enumerate(pitch_names))
	
	# Create input and output sequences
	network_input = []
	network_output = []
	
	for i in range(0, len(notes) - sequence_length, 1):
		sequence_in = notes[i : i+sequence_length]
		sequence_out = notes[i+sequence_length]
		
		network_input.append([pitch_to_int[char] for char in sequence_in])
		network_output.append([pitch_to_int[sequence_out]])
	
	n_patterns = len(network_input)
	
	# Convert input sequences to the shape of LSTM input
	network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
	
	# Normalize the input
   # Let the optimizer find the minimum of deviation faster and better
	network_input = network_input / float(num_pitch)
	
	# Ouput {0,1}
	network_output = tf.keras.utils.to_categorical(network_output)
	
	return (network_input, network_output)
	
if __name__ == "__main__":
	train()
