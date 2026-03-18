# function to call the main analysis/synthesis functions in software/models/hpsModel.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import sys, os
from smstools.models import utilFunctions as UF
from smstools.models import hpsModel as HPS
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)
import plot_helpers as PH

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(
    inputFile=os.path.join(_sounds_dir, "sax-phrase-short.wav"),
    window="blackman",
    M=601,
    N=1024,
    t=-100,
    minSineDur=0.1,
    nH=100,
    minf0=350,
    maxf0=700,
    f0et=5,
    harmDevSlope=0.01,
    stocf=0.1,
):
    """
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size; N: fft size (power of two, bigger or equal than M)
    t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
    nH: maximum number of harmonics; minf0: minimum fundamental frequency in sound
    maxf0: maximum fundamental frequency in sound; f0et: maximum error accepted in f0 detection algorithm
    harmDevSlope: allowed deviation of harmonic tracks, higher harmonics have higher allowed deviation
    stocf: decimation factor used for the stochastic approximation
    """

    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # compute the harmonic plus stochastic model of the whole sound
    hfreq, hmag, hphase, stocEnv = HPS.hpsModelAnal(
        x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur, Ns, stocf
    )

    # synthesize a sound from the harmonic plus stochastic representation
    y, yh, yst = HPS.hpsModelSynth(hfreq, hmag, hphase, stocEnv, Ns, H, fs)

    # output sound file (monophonic with sampling rate of 44100)
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFileSines = os.path.join(output_dir, f"{stem}_hpsModel_sines.wav")
    outputFileStochastic = os.path.join(output_dir, f"{stem}_hpsModel_stochastic.wav")
    outputFile = os.path.join(output_dir, f"{stem}_hpsModel.wav")

    # write sounds files for harmonics, stochastic, and the sum
    UF.wavwrite(yh, fs, outputFileSines)
    UF.wavwrite(yst, fs, outputFileStochastic)
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 15000.0

    # plot the input sound
    plt.subplot(3, 1, 1)
    PH.plot_waveform(plt.gca(), x, fs, title="input sound: x")

    # plot spectrogram stochastic component
    plt.subplot(3, 1, 2)
    numFrames = stocEnv.shape[0]
    sizeEnv = stocEnv.shape[1]
    frame_time = H * np.arange(numFrames) / float(fs)
    binFreq = (0.5 * fs) * np.arange(sizeEnv) / sizeEnv
    tracks = hfreq * np.less(hfreq, maxplotfreq) if hfreq.shape[1] > 0 else None
    PH.plot_spectrogram_with_tracks(
        plt.gca(), stocEnv, tracks if tracks is not None else np.zeros_like(stocEnv),
        fs, N, H, max_plot_freq=maxplotfreq, title="harmonics + stochastic spectrogram",
        frame_time=frame_time, bin_freq=binFreq
    )

    # plot the output sound
    plt.subplot(3, 1, 3)
    PH.plot_waveform(plt.gca(), y, fs, title="output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
