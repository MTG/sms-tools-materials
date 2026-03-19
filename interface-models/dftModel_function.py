# function to call the main analysis/synthesis functions in software/models/dftModel.py

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
from smstools.models import utilFunctions as UF
from smstools.models import dftModel as DFT
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(inputFile=os.path.join(_sounds_dir, "piano.wav"), window="blackman", M=511, N=1024, time=0.2):
    """
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (choice of rectangular, hann, hamming, blackman, blackmanharris)
    M: analysis window size (odd integer value)
    N: fft size (power of two, bigger or equal than than M)
    time: time  to start analysis (in seconds)
    """

    # read input sound (monophonic with sampling rate of 44100)
    fs, x = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # get a fragment of the input sound of size M
    sample = int(time * fs)
    if sample + M >= x.size or sample < 0:  # raise error if time outside of sound
        raise ValueError("Time outside sound boundaries")
    x1 = x[sample : sample + M]

    # compute the dft of the sound fragment
    mX, pX = DFT.dftAnal(x1, w, N)

    # compute the inverse dft of the spectrum
    y = DFT.dftSynth(mX, pX, w.size) * sum(w)

    # create figure
    plt.figure(figsize=(9, 6))

    # plot the sound fragment
    plt.subplot(4, 1, 1)
    #t = time + np.arange(M) / float(fs)
    PH.plot_waveform(plt.gca(), x1, fs, title="input sound: x1")
    #plt.xlim([time, time + M / float(fs)])
    plt.xlim([0, 0 + M / float(fs)]) # not strictly needed

    # plot the magnitude spectrum
    plt.subplot(4, 1, 2)
    freqs = float(fs) * np.arange(mX.size) / float(N)
    PH.plot_spectrum(plt.gca(), freqs, mX, title="magnitude spectrum: mX", xlabel="frequency (Hz)", ylabel="amplitude (dB)", color="r")
    plt.xlim([0, fs / 2.0])
    # plot the phase spectrum
    plt.subplot(4, 1, 3)
    freqs = float(fs) * np.arange(pX.size) / float(N)
    PH.plot_spectrum(plt.gca(), freqs, pX, title="phase spectrum: pX", xlabel="frequency (Hz)", ylabel="phase (radians)", color="c")
    plt.xlim([0, fs / 2.0])

    # plot the sound resulting from the inverse dft
    plt.subplot(4, 1, 4)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")
    #plt.xlim([time, time + M / float(fs)])
    plt.xlim([0, 0 + M / float(fs)]) # not strictly needed

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
