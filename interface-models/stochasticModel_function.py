# function to call the main analysis/synthesis functions in software/models/stochasticModel.py

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from scipy.signal.windows import hann
from smstools.models import utilFunctions as UF
from smstools.models import stochasticModel as STM
from smstools.models import stft as STFT


def _plot_spectrogram(sound, fs, N, H, maxplotfreq, title="spectrogram"):
    """Helper to plot a magnitude spectrogram consistently."""
    mX, pX = STFT.stftAnal(sound, hann(N), N, H)
    numFrames = int(mX[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = fs * np.arange(N * maxplotfreq / fs) / N
    plt.pcolormesh(
        frmTime, binFreq, np.transpose(mX[:, : int(N * maxplotfreq / fs + 1)])
    )
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title(title)
    plt.autoscale(tight=True)

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(
    inputFile=os.path.join(_sounds_dir, "ocean.wav"),
    H=256,
    N=512,
    stocf=0.1,
    melScale=1,
    normalization=1,
):
    """
    inputFile: input sound file (monophonic with sampling rate of 44100)
    H: hop size, N: fft size
    stocf: decimation factor used for the stochastic approximation (bigger than 0, maximum 1)
    melScale: frequency approximation scale (0: linear approximation, 1: mel frequency approximation)
    normalization: amplitude normalization of output (0: no normalization, 1: normalization to input amplitude)
    """

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # compute stochastic model
    stocEnv = STM.stochasticModelAnal(x, H, N, stocf, fs, melScale)

    # synthesize sound from stochastic model
    y = STM.stochasticModelSynth(stocEnv, H, N, fs, melScale)

    if normalization == 1:
        y = y * max(x) / max(y)

    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_stochasticModel.wav")

    # write output sound
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 10000.0

    # plot input spectrogram
    plt.subplot(2, 1, 1)
    _plot_spectrogram(x, fs, N, H, maxplotfreq, "input magnitude spectrogram")

    # plot the output sound
    plt.subplot(2, 1, 2)
    _plot_spectrogram(y, fs, N, H, maxplotfreq, "output magnitude spectrogram")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
