# ImprovedPlayMelody


**What It Does**

PlayMelody.py uses a directory containing an octave of semitones from one instrument and uses the sound clips to recreate the melody of a simple song. I was able to find .wav files of the 12 semitones from a single octave at [Free Sound], I added these to a directory and pass the directory into the paramaters upon execution of PlayMelody.py. From these semitones, my program creates a list of every note on a piano; to do this it first fills the list with each of the semitones, it then shifts the octave multiples times both up and down to capture the entire range of the piano. After this note list has been created, the program takes the song entered as a paramater and finds the euclidean distance between each pitch in the song and each sample pitch, appending the closest sample pitch to a new list and then encoding it as an audio file.

**How Did I Come Up With This Idea?**

As I was thinking of ideas for other research modules and my final project, I realized that the majority of the projects that I wanted to work on involved playing a note from a specific instrument. Most of my ideas involve something along the lines of creating a chord progression or using cellular automata to create a simple melody, and these all involve creating notes. I looked into [Echonest]'s API and couldn't find a way to properly create an AudioQuantum object that sounded natural, after that I looked into [Python Audio]'s API and learned about the methods to directly manipulate the sound card. After struggling with the previous two attempts, I realized that all I needed were 12 semitones from any octave. With these 12 pitches, I could make use of [Echonest] to pitch shift each note by an octave and create notes from any octave. I prefer this solution over the others too because it allows me to use other instruments if I choose, if I were to find .wav files for any other instruments, I could use them in the same way to generate notes as long as I have 12 semitones from any octave.

**What Problem Does It Solve?**

The completion of this program opens up a variety of possibilities for what I can do next. Now that I have a way to generate any note given a directory, I can accomplish multiple programs that I had in mind. One of the most obvious things I can do is expand on this specific project even more and mimic the melody from a much more complex song. [Extracting Melody] goes in depth on how to use fourier transformations to extract not only the melody, but also the rythm and the bass of a song. At the moment, my code can only mimic simple melodies, but I could use this resource to expand on my program and fix its shortcomings.

Another idea that could be accomplished now that I can generate notes is a simple chord progression. [Chord Probabilities] goes in depth on how to find the probability that any one chord will follow any other chord. By using this information, I can shift 4 notes and play them simulatenously to create a chord, use the probabilities to find a chord that would most likely sound good following the previous chord, and then repeat with some sort of randomized rythm.

Finally, I could make use of these notes to create a basic song based off of cellular automata. In a fashion similar to [Wolfram Tones] or [Molecular Music Box], I could experiment with simple patterns to create naturally complex songs. Cellular automata is an incredibly interesting way to create music because it makes use of analyzing simple patterns in life and using those to create an end product that is much more complex than the pattern that created it. Now that I can generate notes, I can simulate any instrument and use Stephen Wolfram's research to create generative music.

**Dependencies**

You will need Pyechonest to use PlayMelody.py.

**Resources**

1. [Free Sound]

2. [Modify]

3. [Extracting Melody]

4. [Chord Probabilities]

5. [Recurse Through Directory]

6. [Python Audio]

7. [Echonest]

8. [Molecular Music Box]

9. [Wolfram Tones]


**How To Mimic A Melody**

To run PlayMelody.py, the user must enter the location of the song they wish to be analyzed (the simpler the melody the better), the name of the output file, and the directory containing the 12 semitones from the chosen instrument. The following command will create a .mp3 file containing the melody of Happy Birthday:

```python
python PlayMelody.py NoteList HappyBirthday.mp3 HappyMelody.mp3
```

**Code Explanation**

The program begins by iterating through the given directory containing 12 semitones and adding them to a list. The following code, inspired by [Recursing Through Directory], iterates through a directory and makes a list containing each of the 12 semitones:

```python
AUDIO_EXTENSIONS = set(['mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'])

def createSemitones(directory, notes):
    for f in os.listdir(directory):
        if _isAudio(f):
            path = os.path.join(directory, f)
            _addOneNote(path, notes)

def _addOneNote(path, notes):
    audiofile = audio.LocalAudioFile(path)
    notes.append(audiofile)

def _isAudio(f):
    _, ext = os.path.splitext(f)
    ext = ext[1:]
    return ext in AUDIO_EXTENSIONS
```

After the semitones have been added to a list, they are run through the . The following methods take the total list of pitches, the list of semitones, and the desired shift in octave as paramaters and adds all the semitones in the desired octave to the total list of pitches:

```python
def addOctave(semitones, octaves, noteList):
    for note in semitones:
        changeOneNoteOctave(note, noteList, octaves)

def changeOneNoteOctave(note, noteList, octaves):
    soundtouch = modify.Modify()
    new_note = soundtouch.shiftPitchOctaves(note, octaves)
    noteList.append(new_note)
```


In the .wav file containing the pitch A from [Free Sound], the frequency is 220 Hz, this the 4 octaves above and the 3 octaves below this semitone must be added to span the entire range of an 88-key piano. The following code adds the 3 octaves below and the 4 octaves above the given pitches to the list of total pitches:

```python
for note in semitones:
        noteList.append(note)
    for i in range(1,4):
        addOctave(semitones, i, noteList)
    for i in range(1,3):
        addOctave(semitones, i*-1, noteList)
```


Finally, once the total list of pitches has been created, the program uses them to create the melody of the chosen song. For each pitch in the song, the program determines the most similar pitch and appends that to a list. Once the song has been fully analyzed, the list is encoded as a .mp3 with the chosen name. The following code iterates through the pitches of a song and recreates the melody:

```python
for i in range(len(songPitches)):
        for j in range(len(noteList)):
            notePitches = noteList[j].pitches
            dist = distFinder.cosine(songPitches[i], notePitches[0]) 
            if dist < bmd:
                bmd = dist
                bmi = j
        collect.append(noteList[bmi])
  out = audio.assemble(collect)
  out.encode(output_filename)
```


[Modify]: http://echonest.github.io/remix/apidocs/echonest.remix.modify.Modify-class.html
[Free Sound]: http://www.freesound.org/people/pinkyfinger/packs/4409/
[Recurse Through Directory]: https://github.com/echonest/pyechonest/blob/master/examples/show_attrs.py
[Python Audio]: https://wiki.python.org/moin/Audio/
[Echonest]: http://the.echonest.com/
[Extracting Melody]: http://perso.telecom-paristech.fr/~grichard/Publications/2013-Salomon-SigMag.pdf
[Chord Probabilities]: http://bengio.abracadoudou.com/cv/publications/pdf/paiement_2005_ismir.pdf
[Molecular Music Box]: https://www.youtube.com/watch?v=3Z8CuAC_-bg
[Wolfram Tones]: http://tones.wolfram.com/about/
