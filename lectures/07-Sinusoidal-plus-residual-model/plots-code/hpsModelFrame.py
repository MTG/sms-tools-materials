import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample, get_window
from scipy.fftpack import fft, ifft, fftshift
from smstools.models import dftModel as DFT
from smstools.models import utilFunctions as UF
from smstools.models import harmonicModel as HM

(fs, x) = UF.wavread('../../../sounds/flute-A4.wav')
pos = int(.8*fs)
M = 601
hM1 = (M+1)//2
hM2 = M//2
w = np.hamming(M)
N = 1024
t = -100
nH = 40
minf0 = 420
maxf0 = 460
f0et = 5
minSineDur = .1
harmDevSlope = 0.01
Ns = 512
H = Ns//4
stocf = .2
x1 = x[pos-hM1:pos+hM2]
x2 = x[pos-Ns//2-1:pos+Ns//2-1]

mX, pX = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX, t)
iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)
ipfreq = fs*iploc/N
f0 = UF.f0Twm(ipfreq, ipmag, f0et, minf0, maxf0)
hfreqp = []
hfreq, hmag, hphase = HM.harmonicDetection(ipfreq, ipmag, ipphase, f0, nH, hfreqp, fs, harmDevSlope)
Yh = UF.genSpecSines(hfreq, hmag, hphase, Ns, fs)
mYh = 20 * np.log10(abs(Yh[:Ns//2]))
bh = get_window('blackmanharris', Ns)
X2 = fft(fftshift(x2*bh/sum(bh)))
Xr = X2-Yh
mXr = 20 * np.log10(abs(Xr[:Ns//2]))
mYst = resample(np.maximum(-200, mXr), int(mXr.size*stocf))  # decimate the mag spectrum


maxplotfreq = 8000.0
plt.figure(1, figsize=(9, 7))
plt.subplot(2,1,1)
binFreq = (fs/2.0)*np.arange(mX.size)/(mX.size)
plt.plot(binFreq,mX,'r', lw=1.5)
plt.axis([0,maxplotfreq,-100,max(mX)+2])
plt.plot(hfreq, hmag, marker='x', color='b', linestyle='', lw=2, markeredgewidth=1.5)
plt.title('mX + harmonics')

plt.subplot(2,1,2)
binFreq = (fs/2.0)*np.arange(mXr.size)/(mXr.size)
plt.plot(binFreq,mYh,'r', lw=.6, label='mYh')
plt.plot(binFreq,mXr,'r', lw=1.0, label='mXr')
binFreq = (fs/2.0)*np.arange(mYst.size)/(mYst.size)
plt.plot(binFreq,mYst,'r', lw=1.5, label='mYst')
plt.axis([0,maxplotfreq,-100,max(mYh)+2])
plt.legend(prop={'size':15})
plt.title('mYh + mXr + mYst')

plt.tight_layout()
plt.savefig('hpsModelFrame.png')
plt.show()

