import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
from scipy.signal import get_window
eps = np.finfo(float).eps
from smstools.models import utilFunctions as UF

Ns = 256
hNs = Ns//2
yw = np.zeros(Ns)
fs = 44100
freqs = np.array([1000.0, 4000.0, 8000.0])
amps = np.array([.6, .4, .6])
phases = ([0.5, 1.2, 2.3])
yploc = Ns*freqs/fs
ypmag = 20*np.log10(amps/2.0)
ypphase = phases

Y = UF.genSpecSines(freqs, ypmag, ypphase, Ns, fs)
absmY = abs(Y[:hNs])
absmY[absmY < eps] = eps
mY = 20*np.log10(absmY)
pY = np.unwrap(np.angle(Y[:hNs]))
y= fftshift(ifft(Y))*sum(get_window('blackmanharris',Ns))

plt.figure(1, figsize=(9, 5))
plt.subplot(3,1,1)
plt.plot(fs*np.arange(Ns/2)/Ns, mY, 'r', lw=1.5)
plt.axis([0, fs/2.0,-100,0])
plt.title("mY, freqs (Hz) = 1000, 4000, 8000; amps = .6, .4, .6")

plt.subplot(3,1,2)
pY[pY==0]= np.nan
plt.plot(fs*np.arange(Ns/2)/Ns, pY, 'c', lw=1.5)
plt.axis([0, fs/2.0,-.01,3.0])
plt.title("pY, phases (radians) = .5, 1.2, 2.3")

plt.subplot(3,1,3)
plt.plot(np.arange(-hNs, hNs), np.real(y), 'b', lw=1.5)
plt.axis([-hNs, hNs,min(np.real(y)),max(np.real(y))])
plt.title("y")

plt.tight_layout()
plt.savefig('spectral-sine-synthesis.png')
plt.show()
