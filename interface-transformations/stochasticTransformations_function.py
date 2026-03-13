# function call to the transformation function of relevance to the stochasticModel

import os
import numpy as np
import matplotlib.pyplot as plt
from smstools.models import stochasticModel as STC
from smstools.models import utilFunctions as UF
from smstools.transformations import stochasticTransformations as STCT


def _plot_waveform(sound, fs, title="sound"):
    """Helper to plot a waveform consistently."""
    plt.plot(np.arange(sound.size) / float(fs), sound)
    plt.axis([0, sound.size / float(fs), min(sound), max(sound)])
    plt.ylabel("amplitude")
    plt.xlabel("time (sec)")
    plt.title(title)

_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))


def main(
    inputFile=os.path.join(_sounds_dir, "rain.wav"), stocf=0.1, timeScaling=np.array([0, 0, 1, 2])
):
    """
    function to perform a time scaling using the stochastic model
    inputFile: name of input sound file
    stocf: decimation factor used for the stochastic approximation
    timeScaling: time scaling factors, in time-value pairs
    """

    # hop size
    H = 128

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # perform stochastic analysis
    mYst = STC.stochasticModelAnal(x, H, H * 2, stocf)

    # perform time scaling of stochastic representation
    ystocEnv = STCT.stochasticTimeScale(mYst, timeScaling)

    # synthesize output sound
    y = STC.stochasticModelSynth(ystocEnv, H, H * 2)

    # write output sound
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_stochasticModelTransformation.wav")
    UF.wavwrite(y, fs, outputFile)

    # create figure to plot
    plt.figure(figsize=(9, 6))

    # plot the input sound
    plt.subplot(4, 1, 1)
    _plot_waveform(x, fs, "input sound: x")

    # plot stochastic representation
    plt.subplot(4, 1, 2)
    numFrames = int(mYst[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = np.arange(int(stocf * H)) * float(fs) / (stocf * 2 * H)
    plt.pcolormesh(frmTime, binFreq, np.transpose(mYst))
    plt.autoscale(tight=True)
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title("stochastic approximation")

    # plot modified stochastic representation
    plt.subplot(4, 1, 3)
    numFrames = int(ystocEnv[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = np.arange(int(stocf * H)) * float(fs) / (stocf * 2 * H)
    plt.pcolormesh(frmTime, binFreq, np.transpose(ystocEnv))
    plt.autoscale(tight=True)
    plt.xlabel("time (sec)")
    plt.ylabel("frequency (Hz)")
    plt.title("modified stochastic approximation")

    # plot the output sound
    plt.subplot(4, 1, 4)
    _plot_waveform(y, fs, "output sound: y")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
