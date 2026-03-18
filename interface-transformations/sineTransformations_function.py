# function call to the transformation functions of relevance for the sineModel
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
import sys, os
from smstools.models import sineModel as SM
from smstools.transformations import sineTransformations as ST
from smstools.models import utilFunctions as UF

# Add interface-transformations to sys.path for robust imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from plot_helpers import setup_plot_style, plot_waveform, plot_frequency_tracks


_sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))



def _mask_frequencies(freq, maxfreq):
    masked = np.copy(freq)
    masked[masked > maxfreq] = np.nan
    masked[masked <= 0] = np.nan
    return masked


def analysis(
    inputFile=os.path.join(_sounds_dir, "mridangam.wav"),
    window="hamming",
    M=801,
    N=2048,
    t=-90,
    minSineDur=0.01,
    maxnSines=150,
    freqDevOffset=20,
    freqDevSlope=0.02,
):
    """
    Analyze a sound with the sine model
    inputFile: input sound file (monophonic with sampling rate of 44100)
    window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M: analysis window size; N: fft size (power of two, bigger or equal than M)
    t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
    maxnSines: maximum number of parallel sinusoids
    freqDevOffset: frequency deviation allowed in the sinusoids from frame to frame at frequency 0
    freqDevSlope: slope of the frequency deviation, higher frequencies have bigger deviation
    returns inputFile: input file name; fs: sampling rate of input file,
            tfreq, tmag: sinusoidal frequencies and magnitudes
    """

    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)

    # compute the sine model of the whole sound
    tfreq, tmag, tphase = SM.sineModelAnal(
        x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope
    )

    # synthesize the sines without original phases
    y = SM.sineModelSynth(tfreq, tmag, np.array([]), Ns, H, fs)

    # output sound file (monophonic with sampling rate of 44100)
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_sineModel.wav")

    # write the sound resulting from the inverse stft
    UF.wavwrite(y, fs, outputFile)


    setup_plot_style()
    fig, axes = plt.subplots(3, 1, figsize=(9, 6))
    maxplotfreq = 5000.0

    # plot input sound
    plot_waveform(axes[0], x, fs, title="input sound: x")

    # plot sinusoidal frequencies
    if tfreq.shape[1] > 0:
        tracks = _mask_frequencies(tfreq, maxplotfreq)
        plot_frequency_tracks(axes[1], tracks, fs, H, title="frequencies of sinusoidal tracks", max_freq=maxplotfreq)
        axes[1].set_xlim([0, x.size / float(fs)])

    # plot output sound
    plot_waveform(axes[2], y, fs, title="output sound: y")

    fig.tight_layout()
    plt.show(block=False)

    return inputFile, fs, tfreq, tmag


def transformation_synthesis(
    inputFile,
    fs,
    tfreq,
    tmag,
    freqScaling=np.array([0, 2.0, 1, 0.3]),
    timeScaling=np.array([0, 0.0, 0.671, 0.671, 1.978, 1.978 + 1.0]),
):
    """
    Transform the analysis values returned by the analysis function and synthesize the sound
    inputFile: name of input file; fs: sampling rate of input file
    tfreq, tmag: sinusoidal frequencies and magnitudes
    freqScaling: frequency scaling factors, in time-value pairs
    timeScaling: time scaling factors, in time-value pairs
    """

    # size of fft used in synthesis
    Ns = 512

    # hop size (has to be 1/4 of Ns)
    H = 128

    # frequency scaling of the sinusoidal tracks
    ytfreq = ST.sineFreqScaling(tfreq, freqScaling)

    # time scale the sinusoidal tracks
    ytfreq, ytmag = ST.sineTimeScaling(ytfreq, tmag, timeScaling)

    # synthesis
    y = SM.sineModelSynth(ytfreq, ytmag, np.array([]), Ns, H, fs)

    # write output sound
    stem = os.path.basename(inputFile)[:-4]
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds")
    os.makedirs(output_dir, exist_ok=True)
    outputFile = os.path.join(output_dir, f"{stem}_sineModelTransformation.wav")
    UF.wavwrite(y, fs, outputFile)


    setup_plot_style()
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    maxplotfreq = 15000.0

    # plot transformed sinusoidal frequencies
    if ytfreq.shape[1] > 0:
        tracks = _mask_frequencies(ytfreq, maxplotfreq)
        plot_frequency_tracks(axes[0], tracks, fs, H, title="transformed sinusoidal tracks", max_freq=maxplotfreq)
        axes[0].set_xlim([0, y.size / float(fs)])

    # plot output sound
    plot_waveform(axes[1], y, fs, title="output sound: y")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":

    # analysis
    inputFile, fs, tfreq, tmag = analysis()

    # transformation and synthesis
    transformation_synthesis(inputFile, fs, tfreq, tmag)

    plt.show()
