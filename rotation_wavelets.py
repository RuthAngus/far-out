import numpy as np
import matplotlib.pyplot as pl
from Wavelets import wavelets, power_of_2
import pyfits

# load data
hdulist = pyfits.open("/Users/angusr/angusr/Kepler/11904151/kplr011904151-2010265121752_llc.fits")
tbdata = hdulist[1].data
x = tbdata["TIME"]
y = tbdata["PDCSAP_FLUX"]
yerr = tbdata["PDCSAP_FLUX_ERR"]
q = tbdata["SAP_QUALITY"]

# remove nans and median normalise
x = np.isfinite(x)*np.isfinite(y)*np.isfinite(yerr)*(q==0)
y = y[x]
# y = y[:1024]
y = y - np.median(y)

# wavelet decomposition ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']
coeffs = wavelets(y, 'dmey')

pl.clf()
ax1 = pl.subplot2grid((10,1), (0,0), rowspan=5)
ax1.imshow(coeffs, aspect=(512./8.))
ax2 = pl.subplot2grid((10,1), (5,0), sharex=ax1, rowspan=5)
ax2.plot(y[:power_of_2(y)], 'k')
pl.xlim(0, len(y[:power_of_2(y)]))
pl.xlabel('Time (days)')
pl.ylabel('Flux')
pl.savefig('rotation')
