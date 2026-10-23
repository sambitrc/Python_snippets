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
