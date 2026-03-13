# function to call the main analysis/synthesis functions in software/models/spsModel.py

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
from smstools.models import spsModel as SPS
from smstools.models import utilFunctions as UF


def _plot_waveform(sound, fs, title="sound"):
    """Helper to plot a waveform consistently."""
    plt.plot(np.arange(sound.size) / float(fs), sound)
    plt.axis([0, sound.size / float(fs), min(sound), max(sound)])
    plt.ylabel("amplitude")
    plt.xlabel("time (sec)")
    plt.title(title)

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def _mask_frequencies(freq, maxfreq):
    """Mask frequencies above maxfreq and set zeros to NaN."""
    masked = freq * np.less(freq, maxfreq)
    masked[masked <= 0] = np.nan
    return masked


def _plot_sine_overlay(tfreq, maxplotfreq, H, fs, title="sinusoidal + stochastic spectrogram"):
    """Overlay sinusoidal frequency tracks on the current matplotlib subplot."""
    if tfreq.shape[1] > 0:
        sines = _mask_frequencies(tfreq, maxplotfreq)
        frmTime = H * np.arange(int(sines[:, 0].size)) / float(fs)
        plt.plot(frmTime, sines, color="k", ms=3, alpha=1)
        plt.xlabel("time(s)")
        plt.ylabel("Frequency(Hz)")
        plt.autoscale(tight=True)
        plt.title(title)


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
    stocf=0.2,
):
    """
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size; N: fft size (power of two, bigger or equal than M)
    t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
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

    # perform sinusoidal+sotchastic analysis
    tfreq, tmag, tphase, stocEnv = SPS.spsModelAnal(
        x, fs, w, N, H, t, minSineDur, maxnSines, freqDevOffset, freqDevSlope, stocf
    )

    # synthesize sinusoidal+stochastic model
    y, ys, yst = SPS.spsModelSynth(tfreq, tmag, tphase, stocEnv, Ns, H, fs)

    # output sound file (monophonic with sampling rate of 44100)
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFileSines = os.path.join(output_dir, f"{stem}_spsModel_sines.wav")
    outputFileStochastic = os.path.join(output_dir, f"{stem}_spsModel_stochastic.wav")
    outputFile = os.path.join(output_dir, f"{stem}_spsModel.wav")

    # write sounds files for sinusoidal, residual, and the sum
    UF.wavwrite(ys, fs, outputFileSines)
    UF.wavwrite(yst, fs, outputFileStochastic)
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # frequency range to plot
    maxplotfreq = 10000.0

    # plot the input sound
    plt.subplot(3, 1, 1)
    _plot_waveform(x, fs, "input sound: x")

    plt.subplot(3, 1, 2)
    numFrames = int(stocEnv[:, 0].size)
    sizeEnv = int(stocEnv[0, :].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = (0.5 * fs) * np.arange(sizeEnv * maxplotfreq / (0.5 * fs)) / sizeEnv
    plt.pcolormesh(
        frmTime,
        binFreq,
        np.transpose(stocEnv[:, : int(sizeEnv * maxplotfreq / (0.5 * fs) + 1)]),
        shading="auto",
    )
    plt.autoscale(tight=True)

    # plot sinusoidal frequencies on top of stochastic component
    _plot_sine_overlay(tfreq, maxplotfreq, H, fs)

    # plot the output sound
    plt.subplot(3, 1, 3)
    _plot_waveform(y, fs, "output sound: y")

    plt.tight_layout()
    plt.ion()
    plt.show()


if __name__ == "__main__":
    main()
