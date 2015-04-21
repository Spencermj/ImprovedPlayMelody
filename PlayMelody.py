import echonest.remix.audio as audio
import scipy.spatial.distance as distFinder
import os
import dirac
import numpy

AUDIO_EXTENSIONS = set(['mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'])

def main(directory, inputfile_name, output_filename):
    semitones = []
    noteList = [[0 for x in range(12)] for x in range(6)]
    collect = audio.AudioQuantumList()
    final = audio.AudioQuantumList()
    #createAllNotes()
    initNoteList(noteList)
    print len(noteList)
    print noteList[0][0].analysis.segments.timbre
    audiofile = audio.LocalAudioFile(input_filename)
    songSegments = audiofile.analysis.segments
    bmp = 10000.0
    bmpi = 0
    bmt = 10000.0
    bmti = 0
    #print len(songSegments)
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
    
def matchDuration(note, songseg, end):
    ratio = 3 * songseg.duration / note.duration
    print ratio
    for seg in note:
        seg_audio = seg.render()
        scaled_seg = dirac.timeScale(seg_audio.data, ratio)
        ts = audio.AudioData(ndarray=scaled_seg, shape=scaled_seg.shape,
                    sampleRate=44100, numChannels=scaled_seg.shape[1])
        end.append(ts)
    #print songseg.duration
    #print audiolist.duration
    #print (audiolist.duration / songseg.duration)
     
def addOctave(semitones, octaves, noteList):
    for note in semitones:
        changeOneNoteOctave(note, noteList, octaves)

def changeOneNoteOctave(note, noteList, octaves):
    new_note = shiftPitchOctaves(note.render().data, octaves)
    dat = audio.AudioData(ndarray = new_note, shape = new_note.shape, numChannels = new_note.shape[1], sampleRate = 44100)
    noteList.append(dat.render())

def createSemitones(directory, notes):
    for f in os.listdir(directory):
        if _isAudio(f):
            path = os.path.join(directory, f)
            _addOneNote(path, notes)

def shiftPitchOctaves(audio_data, octaves): 
        factor = 2.0 ** octaves
        stretched_data = dirac.timeScale(audio_data, factor)
        index = numpy.floor(numpy.arange(0, stretched_data.shape[0], factor)).astype('int32')
        new_data = stretched_data[index]
        return new_data

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

def initNoteList(notes):
    for i in range(72):
        notes[i/12][i%12] = audio.LocalAudioFile("AllNotes/" + str(i) + ".mp3")

def _addOneNote(path, notes):
    audiofile = audio.LocalAudioFile(path)
    notes.append(audiofile)   

def _isAudio(f):
    _, ext = os.path.splitext(f)
    ext = ext[1:]
    return ext in AUDIO_EXTENSIONS

if __name__ == '__main__':
    import sys
    try:
        directory = sys.argv[1]
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
    except:
        print usage
    main(directory, input_filename, output_filename)


