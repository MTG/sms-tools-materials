# function to call the main analysis/synthesis functions in software/models/sineModel.py

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH
from scipy.signal import get_window
import os, sys
from smstools.models import utilFunctions as UF
from smstools.models import sineModel as SM

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(
    inputFile=os.path.join(_sounds_dir, "bendir.wav"),
    window="hamming",
    M=2001,
    N=2048,
    t=-80,
    minSineDur=0.02,
    maxnSines=150,
    freqDevOffset=10,
    freqDevSlope=0.001,
):
    """
    Perform analysis/synthesis using the sinusoidal model
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size; N: fft size (power of two, bigger or equal than M)
    t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
    """

    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # read input sound
    fs, x = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # analyze the sound with the sinusoidal model
    tfreq, tmag, tphase = SM.sineModelAnal(
        x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope
    )

    # synthesize the output sound from the sinusoidal representation
    y = SM.sineModelSynth(tfreq, tmag, tphase, Ns, H, fs)

    # output sound file name
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_sineModel.wav")

    # write the synthesized sound obtained from the sinusoidal synthesis
    UF.wavwrite(y, fs, outputFile)

    # create figure to show plots
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 5000.0

    # plot the input sound
    plt.subplot(3, 1, 1)
    PH.plot_waveform(plt.gca(), x, fs, title="input sound: x")

    # plot the sinusoidal frequencies
    plt.subplot(3, 1, 2)
    if tfreq.shape[1] > 0:
        PH.plot_frequency_tracks(plt.gca(), tfreq, fs, H, title="frequencies of sinusoidal tracks", max_freq=maxplotfreq)

    # plot the output sound
    plt.subplot(3, 1, 3)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
