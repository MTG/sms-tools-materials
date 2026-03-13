# function for doing a morph between two sounds using the stft

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
from smstools.models import stft as STFT
from smstools.models import utilFunctions as UF
from smstools.transformations import stftTransformations as STFTT


def _plot_waveform(sound, fs, title="sound"):
    """Helper to plot a waveform consistently."""
    plt.plot(np.arange(sound.size) / float(fs), sound)
    plt.axis([0, sound.size / float(fs), min(sound), max(sound)])
    plt.ylabel("amplitude")
    plt.xlabel("time (sec)")
    plt.title(title)

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
    _plot_waveform(x1, fs, "input sound: x")

    # plot magnitude spectrogram of sound 1
    plt.subplot(4, 1, 2)
    numFrames = int(mX1[:, 0].size)
    frmTime = H1 * np.arange(numFrames) / float(fs)
    binFreq = fs * np.arange(N1 * maxplotfreq / fs) / N1
    plt.pcolormesh(
        frmTime, binFreq, np.transpose(mX1[:, : int(N1 * maxplotfreq / fs) + 1])
    )
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title("magnitude spectrogram of x")
    plt.autoscale(tight=True)

    # plot magnitude spectrogram of morphed sound
    plt.subplot(4, 1, 3)
    numFrames = int(mY[:, 0].size)
    frmTime = H1 * np.arange(numFrames) / float(fs)
    binFreq = fs * np.arange(N1 * maxplotfreq / fs) / N1
    plt.pcolormesh(
        frmTime, binFreq, np.transpose(mY[:, : int(N1 * maxplotfreq / fs) + 1])
    )
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title("magnitude spectrogram of y")
    plt.autoscale(tight=True)

    # plot the morphed sound
    plt.subplot(4, 1, 4)
    _plot_waveform(y, fs, "output sound: y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
