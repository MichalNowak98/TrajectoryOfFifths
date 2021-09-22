from midi_module.midi_analyzer import get_cpms_array

NUMBER_OF_CHUNKS = 32


if __name__ == '__main__':
    cpms = get_cpms_array('../../../Download/C G am F.mid', NUMBER_OF_CHUNKS)
