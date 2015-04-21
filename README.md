# ImprovedPlayMelody


**What It Does**

PlayMelody.py uses a directory containing an octave of semitones from a piano and uses the sound clips to recreate the melody of a simple song. I was able to find .wav files of the 12 semitones from a single octave at [Free Sound], I added these to a directory and pass the directory into the paramaters upon execution of PlayMelody.py. From these semitones, my program creates a list of every note on a piano; to do this it first fills the list with each of the semitones, it then shifts the octave multiples times both up and down to capture the entire range of the piano. After a list of every note has been created, the program takes the song entered as a paramater and uses both pitch and timbre to find the closest matching note. After the most similar piano note has been found, it is tempo shifted to match the duration of the segment of the song that it is mimicking.

**How Did I Come Up With This Idea?**

As I was thinking of ideas for other research modules and my final project, I realized that the majority of the projects that I wanted to work on involved playing a note from a specific instrument. Most of my ideas involve something along the lines of creating a chord progression or using cellular automata to create a simple melody, and these all involve creating notes. I looked into [Echonest]'s API and couldn't find a way to properly create an AudioQuantum object that sounded natural, after that I looked into [Python Audio]'s API and learned about the methods to directly manipulate the sound card. After struggling with the previous two attempts, I realized that all I needed were 12 semitones from any octave. With these 12 pitches, I could make use of [Echonest] to pitch shift each note by an octave and create notes from any octave. I prefer this solution over the others too because it allows me to use other instruments if I choose, if I were to find .wav files for any other instruments, I could use them in the same way to generate notes as long as I have 12 semitones from any octave.

Once I had produced the code necessary to produce any desired note, I started considering which of my ideas I could possibly bring to life. During this process I remembered an example I had encountered over the summer, [The Saddest Stylophone]; this project was one of the very first that began to pull my interest towards analyzing and manipulating music with code. I eventually decided that it would be fitting for me to create a project much like the one that originally formed my interest in this field of programming.

**What Problem Does It Solve?**

The completion of this program opens up a variety of possibilities for what I can do next. Now that I have a working product, I can begin to expand on my program to allow it to recreate more complex melodies. At the moment, my code can only mimic simple melodies, but it shows the potetntial to achieve more than that. [Extracting Melody] goes in depth on how to use fourier transformations to pull the melody, rythm, and bass of a song apart. By using fourier transformations to extract the melody, I would have much more accurate information about the semitones that are played. 

**Dependencies**

You will need Pyechonest to use PlayMelody.py.

**Resources**

1. [Free Sound]

2. [Extracting Melody]

3. [Recurse Through Directory]

4. [Echonest]

5. [PyPitch]

6. [Jehan On Timbre]

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

After the semitones have been added to a list, they are run through the addOctave() function. This function originally used the SoundTouch module to shift the octave of a note, but this is impossible now that the module returns an error for all users. To fix this problem, however, Jessie Sykes reverse-engineered SoundTouch's pitch shifting functions. Using Jessie's shiftPitchOctaves() function from [PyPitch], I can shift the octave of any given note. The following methods take the total list of pitches, the list of semitones, and the desired shift in octave as paramaters and adds all the semitones in the desired octave to the total list of pitches:

```python
def addOctave(semitones, octaves, noteList):
    for note in semitones:
        changeOneNoteOctave(note, noteList, octaves)

def changeOneNoteOctave(note, noteList, octaves):
    new_note = shiftPitchOctaves(note.render().data, octaves)
    dat = audio.AudioData(ndarray = new_note, shape = new_note.shape, numChannels = new_note.shape[1], sampleRate = 44100)
    noteList.append(dat.render())

def shiftPitchOctaves(audio_data, octaves): 
        factor = 2.0 ** octaves
        stretched_data = dirac.timeScale(audio_data, factor)
        index = numpy.floor(numpy.arange(0, stretched_data.shape[0], factor)).astype('int32')
        new_data = stretched_data[index]
        return new_data
```

In the .wav file containing the pitch A from [Free Sound], the frequency is 220 Hz, this means the 4 octaves above and the 3 octaves below this semitone must be added to span the entire range of an 88-key piano. After pitch shifting up 3 octaves and down 2 octaves, the sound quality of the piano notes begins to drastically drop so highest and lowest octave were left out. This doesn't prove to be a problem considering the majority of songs tend to stay within a smaller range of notes. The following code adds the 2 octaves below and the 3 octaves above the given pitches to the list of total pitches:

After being loaded into a list, these notes are all in the form of AudioData objects; due to this, there is no way to get the analysis to find the pitch and timbre from each note. To solve this, the program uploads the notes to Echonest and saves them in a local directory. After the directory of all notes has been created, the line where createAllNotes() is called can be commented out to save a great deal of time upon every execution of the program. The following code loads the semitones from the given directory into an AudioQuantumList, uses them to fill the list with the range of pitches, and then saves them locally as '0.mp3' through '71.mp3':

```python
def createAllNotes():
    allNotes =  audio.AudioQuantumList()
    semitones = audio.AudioQuantumList()
    createSemitones(directory, semitones)
    for i in range(4):
        addOctave(semitones, i, allNotes)
    for i in range(1,3):
        addOctave(semitones, i*-1, allNotes)
    for i in range(len(allNotes)):
        note = audio.AudioQuantumList()
        note.append(allNotes[i])
        out = audio.assemble(note)
        out.encode(str(i) + ".mp3")
```

After creating all the notes, the program must then load them into an array to be analyzed. The LocalAudioFiles are added to the array with each row containing an octave and each collumn containing all the pitches of a certain note. The following code runs through the directory that the notes were saved in (AllNotes) and loads them into a 2D-array

```python
def initNoteList(notes):
    for i in range(72):
        notes[i/12][i%12] = audio.LocalAudioFile("AllNotes/" + str(i) + ".mp3")
```

Finally, once the total list of pitches has been created, the program uses them to create the melody of the chosen song. The program iterates through the first row of notes to find the closest matching semitone and then records the index of the collumn. After finding the best matching pitch, the program then iterates through the collumn containing the closest matching semitone to find which octave best matches the song. I decided to model my note list this way in order to cut down on the time it takes to find the best matching note, this reduces the number of elements analyzed in every segment of the song from 72 to 18, saving a large amount of time in the long run.

After some research, I found [Jehan On Timbre] in which Tristan Jehan mentions that the second index of the timbre vector is closely related to frequency. After experimenting with the timbre vector, I found that comparing the second index of the timbre vector in each note to the same index in the timbre vector of the audiofile we wish to mimic serves as an excellent way of finding the appropriate octave. The following code finds the piano note that best matches the current note in the desired song before matching the duration and encoding the file as a .mp3:

```python
for i in range(len(songSegments)):
    for j in range(12):
        noteSegments = noteList[0][j].analysis.segments
        pDist = distFinder.cosine(songSegments[i].pitches, noteSegments[len(noteSegments) / 2].pitches)
        if pDist < bmp:
            bmp = pDist
            bmpi = j
    for k in range(6):
        noteSegments = noteList[k][bmpi].analysis.segments
        tDist = distFinder.cosine(songSegments[i].timbre[1], noteSegments[len(noteSegments) / 2].timbre[1])
        if tDist < bmt:
            bmt = tDist
            bmti = k 
    print str(i / len(songSegments)) + '%'
    matchDuration(noteList[bmti][bmpi].analysis.segments, songSegments[i], collect)
    bmp = 10000.0
    bmt = 10000.0
out = audio.assemble(collect)
out.encode(output_filename)
```

After finding the best matching note for a particular segment, the program calls the matchDuration() function to iterate through the segments of the note and match their duration to the song segment. Considering a number higher than 1 lowers the tempo and a number lower than 1 raises the tempo, it's simple enough to set a ratio for how much to shift the note's tempo by dividing the duration of the song segment by the duration of the note segment. It's important to note that dirac can't timescale by a ratio of less than .5, so each note is tripled in length. The resulting melody is played back slower than in the original song but it is still clear, this problem can be easily fixed in the future. The following code takes the segments of a note, matches their duration to the duration of a song segment, and appends the resulting AudioData to an AudioQuantumList():

```python
def matchDuration(note, songseg, end):
    ratio = 3 * songseg.duration / note.duration
    print ratio
    for seg in note:
        seg_audio = seg.render()
        scaled_seg = dirac.timeScale(seg_audio.data, ratio)
        ts = audio.AudioData(ndarray=scaled_seg, shape=scaled_seg.shape,
                    sampleRate=44100, numChannels=scaled_seg.shape[1])
        end.append(ts)
```

**Where To Go From Here**

At the moment, the program lacks the precision to match every note of a melody. The notes are being matched by segment, but some segments of the song contain two or three notes, making it so that the .mp3 output by the program only matches around half the notes in the melody. The output of the program still sounds like the original song but it sounds more like it is playing along harmonically than trying to mimic the melody. The notes that are being chosen for each segment of the song sound correct, so by accounting for the onset and offset of notes, it should be possible to fairly accurately match the melody of the sound.

[Free Sound]: http://www.freesound.org/people/pinkyfinger/packs/4409/
[Recurse Through Directory]: https://github.com/echonest/pyechonest/blob/master/examples/show_attrs.py
[Python Audio]: https://wiki.python.org/moin/Audio/
[Echonest]: http://the.echonest.com/
[Extracting Melody]: http://perso.telecom-paristech.fr/~grichard/Publications/2013-Salomon-SigMag.pdf
[Jehan On Timbre]: https://developer.echonest.com/forums/thread/794
[PyPitch]: https://github.com/sykesjd/echonest-research/tree/master/pypitch
