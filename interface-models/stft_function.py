# function to call the main analysis/synthesis functions in software/models/stft.py

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from scipy.signal import get_window
from smstools.models import utilFunctions as UF
from smstools.models import stft as STFT
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))

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
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_stft.wav")

    # write the sound resulting from the inverse stft
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 5000.0

    # plot the input sound
    plt.subplot(4, 1, 1)
    PH.plot_waveform(plt.gca(), x, fs, title="input sound: x")

    # plot magnitude spectrogram
    plt.subplot(4, 1, 2)
    PH.plot_spectrogram(plt.gca(), mX, fs, N, H, max_plot_freq=maxplotfreq, title="magnitude spectrogram")

    # plot the phase spectrogram
    plt.subplot(4, 1, 3)
    # Compute phase difference spectrogram
    n_bins = int(N * maxplotfreq / fs) + 1
    phase_diff = np.diff(pX[:, :n_bins], axis=1)
    # Adjust bin_freq to match the reduced dimension after np.diff
    bin_freq = fs * np.arange(n_bins - 1) / N
    PH.plot_spectrogram(
        plt.gca(),
        phase_diff,
        fs,
        N,
        H,
        max_plot_freq=maxplotfreq,
        title="phase spectrogram (derivative)",
        bin_freq=bin_freq
    )

    # plot the output sound
    plt.subplot(4, 1, 4)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
