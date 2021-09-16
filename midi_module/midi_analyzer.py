from mido import MidiFile


def open_midi_file(name):
    time = 0
    notes_on = []
    notes_off = []
    mid = MidiFile(name, clip=True)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            time += msg.time
            if msg.type == 'note_on':
                notes_on += [msg.note, time]
            elif msg.type == 'note_off':
                notes_off += [msg.note, time]