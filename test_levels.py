#source: https://stackoverflow.com/a/16385946/11736660
#alsa error handling from: https://stackoverflow.com/a/17673011/11736660

#original desciption by user eugene: 
#Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
#I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave

from ctypes import * #ALSA error handling
from contextlib import contextmanager #ALSA error handling

THRESHOLD = 500  # audio levels not normalised.
CHUNK_SIZE = 4098
SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4

#ALSA error handling:
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    return max(data_chunk) < THRESHOLD


def show_levels():
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""
    with noalsaerr():
        p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    #audio_started = False
    #data_all = array('h')

    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            data_chunk.byteswap()
        #data_all.extend(data_chunk)
        print('max: {}'.format(max(data_chunk)))
        silent = is_silent(data_chunk)

        #if audio_started:
        if silent:
            print('-> silent')
        else:
            print('-> LOUD')
        print()

    #sample_width = p.get_sample_size(FORMAT)
    #stream.stop_stream()
    #stream.close()
    #p.terminate()


if __name__ == '__main__':
    #print("Wait in silence to begin recording; wait in silence to terminate")
    show_levels()
    print("done, stream terminated")
