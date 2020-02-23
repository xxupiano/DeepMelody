"""
RNN-LSTM
"""

import tensorflow as tf

# the model of network
def network_model(inputs, num_pitch, weights_file=None):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(
              512,  # the number of LSTM layer cells, dimension of output
              # the input shape, only needed by the first layer
              input_shape=(inputs.shape[1], inputs.shape[2]),   # note, integer 
              # return_sequences: control the return
              # -True: return the full sequence, -False: return the last sequence
              # when it piles up LSTM layers, the last LSTM layer is not needed to set
              return_sequences = True)  # return the full sequences
             )
    
    model.add(tf.keras.layers.Dense(num_pitch)) # the num of output = the num of different pitchs
    model.add(tf.keras.layers.Dropout(0.3)) # drop 30% neures, overfitting
    model.add(tf.keras.layers.LSTM(512, return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.LSTM(512))
    model.add(tf.keras.layers.Dense(256))   # densely-connected NN layer
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(num_pitch)) # the num of output = the num of different pitchs
    model.add(tf.keras.layers.Activation('softmax'))

    # cross entropy, RMSProp optimizer
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")
    
    if weights_file is not None:    # when generate music
        # Get parameter from HDF5
        model.load_weights(weights_file)
    
    return model


