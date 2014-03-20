import pywt
import matplotlib.pyplot as pl
import pyfits
import numpy as np
import math

# wavelet decomposition
def wavelets(y, basis):
    coeffs = []
    scales = np.log2(len(y))
    if math.fabs(scales-int(scales))>1e-10:
        print "len(y) must be a power of 2"
        y = y[:power_of_2(y)]
    scales = int(scales)
    for i in range(1,scales):
        c = pywt.wavedec(y, basis, 'zpd', level=i)[0]
        coeffs.append(c)
    coeffs = matrix(coeffs)
    return np.array(coeffs)

# Calculate the nearest power of two
def power_of_2(y):
    a = np.arange(0, 15)
    x = np.argmin(np.fabs(2**a-len(y)))
    nearest = 2**a[x]
    if nearest < len(y):
        return nearest
    else: return 2**a[x-1]

# pad matrix with repetitions
def matrix(coeffs):
    m = 0
    for i in range(len(coeffs)):
        coeffs[i] = list(coeffs[i])
        nc = np.zeros(len(coeffs[0]*2))
        reps = int(float(len(coeffs[0])/float(len(coeffs[i]))))
        for k in range(len(coeffs[i])):
            for j in range(reps):
                nc[m] = coeffs[i][k]
                m+=1
        coeffs[i] = np.array(nc)
        m = 0
    return coeffs

# load data
hdulist = pyfits.open('/Users/angusr/.kplr/data/kplr009002278-2009166043257_llc.fits')
tbdata = hdulist[1].data
flux = tbdata['PDCSAP_FLUX']

# remove nans
flux = flux[np.isfinite(flux)][:1024]
flux = flux - np.median(flux)

# wavelet decomposition
coeffs = wavelets(flux, 'Haar')

# pad matrix
# coeffs = matrix(coeffs)

pl.clf()
ax1 = pl.subplot2grid((10,1), (0,0), rowspan=5)
ax1.imshow(coeffs, aspect=(512./8.))
ax2 = pl.subplot2grid((10,1), (5,0), sharex=ax1, rowspan=5)
ax2.plot(flux, 'k')
pl.xlim(0, len(flux))
pl.xlabel('Time (days)')
pl.ylabel('Flux')
pl.savefig('demo')
