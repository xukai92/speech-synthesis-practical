import wave
import pylab


def graph_spectrogram(utt_name):
    wav_file = '{utt_name}.wav'.format(utt_name=utt_name)
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(16, 8))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    pylab.xlabel('Time (sec)')
    pylab.ylabel('Frequency (kHz)')
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig('{utt_name}.png'.format(utt_name=utt_name))


def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


def main():
    utt_name = 'utt1'
    graph_spectrogram(utt_name)


if __name__ == '__main__':
    main()
