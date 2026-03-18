# function to call the main analysis/synthesis functions in software/models/stochasticModel.py

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from scipy.signal.windows import hann
from smstools.models import utilFunctions as UF
from smstools.models import stochasticModel as STM
from smstools.models import stft as STFT
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH

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
    mX_in, _ = STFT.stftAnal(x, hann(N), N, H)
    PH.plot_spectrogram(plt.gca(), mX_in, fs, N, H, max_plot_freq=maxplotfreq, title="input magnitude spectrogram")

    plt.subplot(2, 1, 2)
    mX_out, _ = STFT.stftAnal(y, hann(N), N, H)
    PH.plot_spectrogram(plt.gca(), mX_out, fs, N, H, max_plot_freq=maxplotfreq, title="output magnitude spectrogram")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
