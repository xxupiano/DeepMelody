# DeepMelody
Monophonic Piano Generation with LSTM

## Requirements

- python = 2.7
- pip install<br>
  tensorflow==1.14.0<br>
  keras==2.3.1<br>
  h5py<br>
  music21<br>
- sudo apt install<br>
  ffmpeg<br>
  timidity<br>



## Train

* The dataset is in `music_midi`.
* `python train.py`<br>
  Set training 100 epochs in default, but it can be stopped anytime (Ctrl + C).



## Generate

- Choose the best parameter  `.hdf5`  produced in training process <br>
  and rename it `best-weights.hdf5`

- `python generate.py`<br>
  Generate `output.mid` firstly, and then turn it into `output.mp3`

