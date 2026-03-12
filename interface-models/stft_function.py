# function to call the main analysis/synthesis functions in software/models/stft.py

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from scipy.signal import get_window
from smstools.models import utilFunctions as UF
from smstools.models import stft as STFT


def _plot_waveform(sound, fs, title="sound"):
    """Helper to plot a waveform consistently."""
    plt.plot(np.arange(sound.size) / float(fs), sound)
    plt.axis([0, sound.size / float(fs), min(sound), max(sound)])
    plt.ylabel("amplitude")
    plt.xlabel("time (sec)")
    plt.title(title)

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def _label_spectrogram(title):
    """Add standard labels to a spectrogram plot."""
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title(title)
    plt.autoscale(tight=True)


def main(inputFile=os.path.join(_sounds_dir, "piano.wav"), window="hamming", M=1024, N=1024, H=512):
    """
    analysis/synthesis using the STFT
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (choice of rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size
    N: fft size (power of two, bigger or equal than M)
    H: hop size (at least 1/2 of analysis window size to have good overlap-add)
    """

    # read input sound (monophonic with sampling rate of 44100)
    fs, x = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # compute the magnitude and phase spectrogram
    mX, pX = STFT.stftAnal(x, w, N, H)

    # perform the inverse stft
    y = STFT.stftSynth(mX, pX, M, H)

    # output sound file (monophonic with sampling rate of 44100)
    outputFile = f"output_sounds/{os.path.basename(inputFile)[:-4]}_stft.wav"

    # write the sound resulting from the inverse stft
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 5000.0

    # plot the input sound
    plt.subplot(4, 1, 1)
    _plot_waveform(x, fs, "input sound: x")

    # plot magnitude spectrogram
    plt.subplot(4, 1, 2)
    numFrames = int(mX[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = fs * np.arange(N * maxplotfreq / fs) / N
    plt.pcolormesh(
        frmTime, binFreq, np.transpose(mX[:, : int(N * maxplotfreq / fs + 1)])
    )
    _label_spectrogram("magnitude spectrogram")

    # plot the phase spectrogram
    plt.subplot(4, 1, 3)
    numFrames = int(pX[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = fs * np.arange(N * maxplotfreq // fs) // N
    plt.pcolormesh(
        frmTime,
        binFreq,
        np.transpose(np.diff(pX[:, : int(N * maxplotfreq / fs + 1)], axis=1)),
    )
    _label_spectrogram("phase spectrogram (derivative)")

    # plot the output sound
    plt.subplot(4, 1, 4)
    _plot_waveform(y, fs, "output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
