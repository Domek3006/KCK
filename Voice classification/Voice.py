import numpy as np
import scipy.io.wavfile
import scipy.fft as fft
import argparse as argp
import warnings
warnings.filterwarnings('ignore')
#from os import listdir

def findCepstrums(file_name):
    # Read a wav file
    w, sig = scipy.io.wavfile.read(file_name)
    # If the signal array has more than one dimension - keep only one
    if (sig.ndim > 1):
        sig = [s[0] for s in sig]
        sig = np.array(sig).astype('float64')
    
    frame_size = 4096
    ceps = list()
    qfreqs = list()

    # Iterate through the signal dividing it into frames
    for frame in range(0, sig.size, frame_size//8):
        if (frame+frame_size > len(sig)):
            break
        sign = sig[frame:frame+frame_size]

        # Multiply frame by hamming window
        wind = sign * np.hamming(len(sign))
        # Get FFT of window
        wind = fft.rfft(wind)

        # Get logarithmic magnitude
        log_sig = np.log(abs(wind))
        freq = fft.rfftfreq(len(sign), 1/w)

        # Calculate cepstrum
        cep = fft.rfft(log_sig)
        df = freq[1] - freq[0]
        # Calculate quefrequecies
        qfreq = fft.rfftfreq(log_sig.size, df)

        ceps.append(cep)
        qfreqs.append(qfreq)
    
    gen = classify(ceps, qfreqs)
    return gen

def classify(cepstrums, quefrequencies):
    M, K = 0, 0
    for qfreqs, cep in zip(quefrequencies, cepstrums):
        # Finad valid frequency range
        valid = (qfreqs > 1/255) & (qfreqs <= 1/85)
        if (True not in valid):
            continue
        # Find dominant frequency
        max_freq_ind = np.argmax(np.abs(cep)[valid])
        f0 = 1/qfreqs[valid][max_freq_ind]
        # Classify
        if (f0 < 174):
            M += 1
        else:
            K += 1
    if M >= K:
        return 'M'
    return 'K'

if __name__ == '__main__':
    parser = argp.ArgumentParser(description='Classify a voice file.')
    parser.add_argument('file_name', metavar='file', type=str, help='a file to be calssified')

    args = parser.parse_args()

    print(findCepstrums(args.file_name))

    '''dir = listdir('train')
    Mc = 0
    Kc = 0
    Mw = 0
    Kw = 0

    for n, w in enumerate(dir):
        cl = findCepstrums('train/' + w)
        if (cl == w[4]) and (w[4] == 'K'):
            Kc += 1
            print(n, cl, 'Correct')
        elif (cl == w[4]) and (w[4] == 'M'):
            Mc += 1
            print(n, cl, 'Correct')
        elif (cl == 'M'):
            Mw += 1
            print(n, cl, 'Wrong')
        else:
            Kw += 1
            print(n, cl, 'Wrong')
    print('Correct: M={} K={}'.format(Mc, Kc))
    print('Wrong: M={} K={}'.format(Mw, Kw))
    print('Overall: C={} W={}'.format(Mc+Kc, Kw+Mw))'''
        
    