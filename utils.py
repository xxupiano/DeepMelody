import os
import subprocess
import pickle
import glob
from music21 import converter, instrument, note, chord, stream


def convertMidi2Mp3():
    input_file = "output.mid"
    output_file = "output.mp3"

    assert os.path.exists(input_file)
    print("Converting %s to MP3" % input_file)

    # use timidity to convert to MP3
    command='timidity {} -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 256k {}'.format(input_file, output_file)
    subprocess.call(command, shell = True)

    print("Converted. Generated file is %s" % output_file)

#if __name__ == "__main__":
#    convertMidi2Mp3()


def get_notes():
    """
    Get notes and chords from MIDI files in music_midi
    """
    notes = []
    
    # glob: get files satisfing the condition, return List
    for file in glob.glob("music_midi/*.mid"):
        stream = converter.parse(file)
        # Get instuments
        parts = instrument.partitionByInstrument(stream)

        if parts:
            # If there is the instrument, get the first part.
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = stream.flat.notes
            
        for element in notes_to_parse:
            # Note, string, eg: E6
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            # Chord, eg: [B4, E5, G5#] -> 4.15.7
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    # notes -> data/notes
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes


def create_music(prediction):
    """
    use musical data predicted by LSTM to create MIDI file, then convert to MP3
    """
    offset = 0
    output_notes = []

    # generate Note and Chord
    for data in prediction:
        # Chord
        if('.' in data) or data.isdigit():
            notes_in_chord = data.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
            notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # Note
        else:
            new_note = note.Note(data)
            new_note.offset = offset 
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # modify offset
        offset += 0.5

    # create stream
    midi_stream = stream.Stream(output_notes)

    # wirte MIDI file
    midi_stream.write('midi', fp='output.mid')

    # Convert MIDI to MP3
    convertMidi2Mp3()


