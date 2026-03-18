# function for doing a morph between two sounds using the stft

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
from smstools.models import stft as STFT
from smstools.models import utilFunctions as UF
from smstools.transformations import stftTransformations as STFTT
import sys
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH


## Removed duplicate waveform plotting, now using PH.plot_waveform

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(
    inputFile1=os.path.join(_sounds_dir, "ocean.wav"),
    inputFile2=os.path.join(_sounds_dir, "speech-male.wav"),
    window1="hamming",
    window2="hamming",
    M1=1024,
    M2=1024,
    N1=1024,
    N2=1024,
    H1=256,
    smoothf=0.5,
    balancef=0.2,
):
    """
    Function to perform a morph between two sounds
    inputFile1: name of input sound file to be used as source
    inputFile2: name of input sound file to be used as filter
    window1 and window2: windows for both files
    M1 and M2: window sizes for both files
    N1 and N2: fft sizes for both sounds
    H1: hop size for sound 1 (the one for sound 2 is computed automatically)
    smoothf: smoothing factor to be applyed to magnitude spectrum of sound 2 before morphing
    balancef: balance factor between booth sounds, 0 is sound 1 and 1 is sound 2
    """

    # read input sounds
    (fs, x1) = UF.wavread(inputFile1)
    (fs, x2) = UF.wavread(inputFile2)

    # compute analysis windows
    w1 = get_window(window1, M1)
    w2 = get_window(window2, M2)

    # perform morphing
    y = STFTT.stftMorph(x1, x2, fs, w1, N1, w2, N2, H1, smoothf, balancef)

    # compute the magnitude and phase spectrogram of input sound (for plotting)
    mX1, pX1 = STFT.stftAnal(x1, w1, N1, H1)

    # compute the magnitude and phase spectrogram of output sound (for plotting)
    mY, pY = STFT.stftAnal(y, w1, N1, H1)

    # write output sound
    stem = os.path.basename(inputFile1)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_stftMorph.wav")
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 10000.0

    # plot sound 1
    plt.subplot(4, 1, 1)
    PH.plot_waveform(plt.gca(), x1, fs, title="input sound: x")

    # plot magnitude spectrogram of sound 1
    plt.subplot(4, 1, 2)
    PH.plot_spectrogram(plt.gca(), mX1, fs, N1, H1, max_plot_freq=maxplotfreq, title="magnitude spectrogram of x")

    # plot magnitude spectrogram of morphed sound
    plt.subplot(4, 1, 3)
    PH.plot_spectrogram(plt.gca(), mY, fs, N1, H1, max_plot_freq=maxplotfreq, title="magnitude spectrogram of y")

    # plot the morphed sound
    plt.subplot(4, 1, 4)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
