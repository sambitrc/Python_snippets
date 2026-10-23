"""Analysis functions used by the notebooks in this repository."""

import numpy as np
from scipy.stats import median_abs_deviation


def mean_stack(tms):
    """Unweighted mean stack of a set of timeseries, ignoring NaNs.

    Parameters
    ----------
    tms : 2D array_like, shape (n_series, n_points)
        One timeseries per row.

    Returns
    -------
    1D ndarray, shape (n_points,)
    """
    return np.nanmean(tms, axis=0)


def median_stack(tms):
    """Unweighted median stack of a set of timeseries, ignoring NaNs.

    Parameters
    ----------
    tms : 2D array_like, shape (n_series, n_points)
        One timeseries per row.

    Returns
    -------
    1D ndarray, shape (n_points,)
    """
    return np.nanmedian(tms, axis=0)


def noise_weights(tms, n_edge=100, mad_threshold=5.0, power=2):
    """Normalized noise-based weights for each timeseries.

    The noise (rms) of each timeseries is measured from its first and last
    `n_edge` points, which are assumed to be free of signal. Series with
    outlying low noise (robust cut in log10(rms)) or zero / undefined noise
    are rejected and given a weight of NaN.

    Parameters
    ----------
    tms : 2D array_like, shape (n_series, n_points)
        One timeseries per row.
    n_edge : int
        Number of points at each end used to measure the noise.
    mad_threshold : float
        Reject series with (median(log10 rms) - log10 rms) > mad_threshold * MAD.
    power : float
        Weights are 1/rms**power: 2 gives inverse-variance weights, 1 gives 1/rms.

    Returns
    -------
    wts : 1D ndarray, shape (n_series,)
        Weights summing to 1, NaN for rejected series.
    rms : 1D ndarray, shape (n_series,)
        Measured noise of each series.
    """
    tms = np.asarray(tms, dtype=float)
    edges = np.concatenate((tms[:, :n_edge], tms[:, -n_edge:]), axis=1)
    rms = np.nanstd(edges, axis=1)

    good = np.isfinite(rms) & (rms > 0)
    logrms = np.log10(rms[good])
    mad = median_abs_deviation(logrms)
    good[good] = (np.median(logrms) - logrms) <= mad_threshold * mad

    wts = np.full(rms.shape, np.nan)
    wts[good] = 1. / rms[good]**power
    wts /= np.nansum(wts)
    return wts, rms


def weighted_mean_stack(tms, wts):
    """Weighted mean stack of a set of timeseries.

    Series with NaN weight, and NaN data points, are left out; at each point
    the weights of the remaining series are renormalized.

    Parameters
    ----------
    tms : 2D array_like, shape (n_series, n_points)
        One timeseries per row.
    wts : 1D array_like, shape (n_series,)
        Weight of each timeseries, e.g. from noise_weights().

    Returns
    -------
    1D ndarray, shape (n_points,)
    """
    tms = np.asarray(tms, dtype=float)
    w = np.broadcast_to(np.asarray(wts, dtype=float)[:, None], tms.shape)
    use = np.isfinite(tms) & np.isfinite(w)
    wsum = np.sum(np.where(use, w, 0.), axis=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.sum(np.where(use, w * tms, 0.), axis=0) / wsum


def autodifference(x, lag=1):
    """Autodifference of a timeseries, (x[i] - x[i+lag]) / sqrt(2).

    Differencing removes slow (correlated) variations, and dividing by
    sqrt(2) keeps the rms of uncorrelated (white) noise unchanged, so the
    standard deviation of the result estimates the white noise level.

    Parameters
    ----------
    x : 1D array_like
        Timeseries.
    lag : int
        Separation, in samples, of the differenced points.

    Returns
    -------
    1D ndarray, shape (len(x) - lag,)
    """
    x = np.asarray(x, dtype=float)
    return (x[:-lag] - x[lag:]) / np.sqrt(2)


def power_spectrum(x, dt):
    """One-sided power spectral density of a timeseries.

    PSD = |FFT(x)|**2 * dt, with an orthonormal FFT, so white noise of rms
    sigma has a flat PSD of sigma**2 * dt. The zero-frequency (mean) term
    is left out.

    Parameters
    ----------
    x : 1D array_like
        Timeseries, sampled every `dt`.
    dt : float
        Sampling interval, in seconds.

    Returns
    -------
    f : 1D ndarray
        Frequencies, in Hz.
    psd : 1D ndarray
        PSD at each frequency, in (units of x)**2 / Hz.
    """
    x = np.asarray(x, dtype=float)
    psd = np.absolute(np.fft.rfft(x, norm='ortho'))**2 * dt
    f = np.fft.rfftfreq(x.shape[0], dt)
    return f[1:], psd[1:]


def gain_match(x, ref):
    """Scale a timeseries so that its mean (DC level) matches that of `ref`.

    Parameters
    ----------
    x : 1D array_like
        Timeseries to rescale.
    ref : 1D array_like
        Reference timeseries.

    Returns
    -------
    1D ndarray
        x * mean(ref) / mean(x)
    """
    x = np.asarray(x, dtype=float)
    return x * np.mean(ref) / np.mean(x)


def difference_timeseries(x1, x2):
    """Difference two correlated timeseries after removing their linear relation.

    A straight line x2 = m * x1 + c is fitted by least squares, and the
    difference is the fit's prediction of x2 minus x2 itself,
    (m * x1 + c - x2) / sqrt(2). This removes the variations common to both
    inputs; dividing by sqrt(2) keeps the rms of uncorrelated noise of equal
    level in the two inputs unchanged.

    Parameters
    ----------
    x1, x2 : 1D array_like, same length
        Timeseries to difference.

    Returns
    -------
    d : 1D ndarray
        Difference timeseries.
    m, c : float
        Slope and offset of the fitted line, c in the units of x2.
    """
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    m, c = np.polyfit(x1, x2, 1)
    d = (m * x1 + c - x2) / np.sqrt(2)
    return d, m, c
