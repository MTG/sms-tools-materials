import numpy as np
import matplotlib.pyplot as plt
from smstools.models import stft as STFT
from smstools.models import utilFunctions as UF
from smstools.models import harmonicModel as HM


(fs, x) = UF.wavread('../../../sounds/flute-A4.wav')
w = np.blackman(551)
N = 1024
t = -100
nH = 40
minf0 = 420
maxf0 = 460
f0et = 5
maxnpeaksTwm = 5
minSineDur = .1
harmDevSlope = 0.01
Ns = 512
H = Ns//4

mX, pX = STFT.stftAnal(x, w, N, H)
hfreq, hmag, hphase = HM.harmonicModelAnal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur)
xr = UF.sineSubtraction(x, Ns, H, hfreq, hmag, hphase, fs)
mXr, pXr = STFT.stftAnal(xr, np.hamming(Ns), Ns, H)

maxplotfreq = 5000.0
plt.figure(1, figsize=(9, 7))

plt.subplot(221)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = fs*np.arange(N*maxplotfreq/fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:int(N*maxplotfreq/fs+1)]))
plt.autoscale(tight=True)

harms = hfreq*np.less(hfreq,maxplotfreq)
harms[harms==0] = np.nan
numFrames = int(harms[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
plt.autoscale(tight=True)
plt.title('mX + harmonics (flute-A4.wav)')

plt.subplot(222)
numFrames = int(mX[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = fs*np.arange(N*maxplotfreq/fs)/N
plt.pcolormesh(frmTime, binFreq, np.transpose(np.diff(pX[:,:int(N*maxplotfreq/fs+1)],axis=1)))
plt.autoscale(tight=True)

harms = hfreq*np.less(hfreq,maxplotfreq)
harms[harms==0] = np.nan
numFrames = int(harms[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
plt.autoscale(tight=True)
plt.title('pX + harmonics')

plt.subplot(223)
numFrames = int(mXr[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = fs*np.arange(Ns*maxplotfreq/fs)/Ns
plt.pcolormesh(frmTime, binFreq, np.transpose(mXr[:,:int(Ns*maxplotfreq/fs+1)]))
plt.autoscale(tight=True)
plt.title('mXr')

plt.subplot(224)
numFrames = int(pXr[:,0].size)
frmTime = H*np.arange(numFrames)/float(fs)
binFreq = fs*np.arange(Ns*maxplotfreq/fs)/Ns
plt.pcolormesh(frmTime, binFreq, np.transpose(np.diff(pXr[:,:int(Ns*maxplotfreq/fs+1)],axis=1)))
plt.autoscale(tight=True)
plt.title('pXr')

plt.tight_layout()
plt.savefig('hprModelAnal-flute.png')
UF.wavwrite(5*xr, fs, 'flute-residual.wav')
plt.show()
