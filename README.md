# DeepMelody
Music Generation with LSTM

## Requirements

- python = 2.7
- pip install
  tensorflow==1.14.0
  keras==2.3.1
  h5py
  music21
- sudo apt install
  ffmpeg
  timidity



## Train

* The dataset is in `music_midi`.
* `python train.py`
  Set training 100 epochs in default, but we can stop anytime (Ctrl + C).



## Generate

- Choose the best parameter  `.hdf5`  produced in training process 
  and rename it `best-weights.hdf5`

- `python generate.py`
  Generate `output.mid` firstly, and then turn it into `output.mp3`

