# function to call the main analysis/synthesis functions in software/models/sprModel.py

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH
import os, sys
from scipy.signal import get_window
from smstools.models import utilFunctions as UF
from smstools.models import sprModel as SPR
from smstools.models import stft as STFT

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
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size
    N: fft size (power of two, bigger or equal than M)
    t: magnitude threshold of spectral peaks
    minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
    """

    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # perform sinusoidal plus residual analysis
    tfreq, tmag, tphase, xr = SPR.sprModelAnal(
        x, fs, w, N, H, t, minSineDur, maxnSines, freqDevOffset, freqDevSlope
    )

    # compute spectrogram of residual
    mXr, pXr = STFT.stftAnal(xr, w, N, H)

    # sum sinusoids and residual
    y, ys = SPR.sprModelSynth(tfreq, tmag, tphase, xr, Ns, H, fs)

    # output sound file (monophonic with sampling rate of 44100)
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFileSines = os.path.join(output_dir, f"{stem}_sprModel_sines.wav")
    outputFileResidual = os.path.join(output_dir, f"{stem}_sprModel_residual.wav")
    outputFile = os.path.join(output_dir, f"{stem}_sprModel.wav")

    # write sounds files for sinusoidal, residual, and the sum
    UF.wavwrite(ys, fs, outputFileSines)
    UF.wavwrite(xr, fs, outputFileResidual)
    UF.wavwrite(y, fs, outputFile)

    # create figure to show plots
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 5000.0

    # plot the input sound
    plt.subplot(3, 1, 1)
    PH.plot_waveform(plt.gca(), x, fs, title="input sound: x")

    # plot the magnitude spectrogram of residual
    plt.subplot(3, 1, 2)
    tracks = tfreq * np.less(tfreq, maxplotfreq) if tfreq.shape[1] > 0 else None
    PH.plot_spectrogram_with_tracks(plt.gca(), mXr, tracks if tracks is not None else np.zeros_like(mXr), fs, N, H, max_plot_freq=maxplotfreq, title="sinusoidal tracks + residual spectrogram")

    # plot the output sound
    plt.subplot(3, 1, 3)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
