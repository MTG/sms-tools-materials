# function call to the transformation function of relevance to the stochasticModel

    # Removed empty function definition; now using plot_helpers
import os
import numpy as np
import matplotlib.pyplot as plt
from smstools.models import stochasticModel as STC
from smstools.models import utilFunctions as UF
from smstools.transformations import stochasticTransformations as STCT

# Add interface-transformations to sys.path for robust imports
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from plot_helpers import setup_plot_style, plot_waveform


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


    setup_plot_style()
    fig, axes = plt.subplots(4, 1, figsize=(9, 6))

    # plot input sound
    plot_waveform(axes[0], x, fs, title="input sound: x")

    # plot stochastic representation
    numFrames = int(mYst[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = np.arange(int(stocf * H)) * float(fs) / (stocf * 2 * H)
    axes[1].pcolormesh(frmTime, binFreq, np.transpose(mYst))
    axes[1].autoscale(tight=True)
    axes[1].set_xlabel("time (sec)")
    axes[1].set_ylabel("frequency (Hz)")
    axes[1].set_title("stochastic approximation")

    # plot modified stochastic representation
    numFrames = int(ystocEnv[:, 0].size)
    frmTime = H * np.arange(numFrames) / float(fs)
    binFreq = np.arange(int(stocf * H)) * float(fs) / (stocf * 2 * H)
    axes[2].pcolormesh(frmTime, binFreq, np.transpose(ystocEnv))
    axes[2].autoscale(tight=True)
    axes[2].set_xlabel("time (sec)")
    axes[2].set_ylabel("frequency (Hz)")
    axes[2].set_title("modified stochastic approximation")

    # plot output sound
    plot_waveform(axes[3], y, fs, title="output sound: y")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
