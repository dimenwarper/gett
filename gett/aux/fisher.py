# Copyright (c) 2008-2010, David Simcha
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#       * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#       * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#       * Neither the name of the authors nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES
# LOSS OF USE, DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from numpy.testing import assert_, assert_approx_equal
from scipy.stats import hypergeom


def fisher_exact(c) :
    """Performs a Fisher exact test on a 2x2 contingency table.

    Parameters
    ----------
    c : array_like of ints
        A 2x2 contingency table.

    Returns
    -------
    oddsratio : float
        This is prior odds ratio and not a posterior estimate.
    p-value : float
        P-value for 2-sided hypothesis of independence.


    Examples
    --------
    >>> fisher_exact([[100, 2], [1000, 5]])
    (0.25, 0.13007593634330314)
    """

    c = np.asarray(c, dtype=np.int64)  # int32 is not enough for the algorithm
    odssratio = c[0,0] * c[1,1] / float(c[1,0] * c[0,1]) \
                            if (c[1,0] > 0 and c[0,1] > 0) else np.inf
    n1 = c[0,0] + c[0,1]
    n2 = c[1,0] + c[1,1]
    n  = c[0,0] + c[1,0]

    mode = int(float((n + 1) * (n1 + 1)) / (n1 + n2 + 2))
    pexact = hypergeom.pmf(c[0,0], n1 + n2, n1, n)
    pmode = hypergeom.pmf(mode, n1 + n2, n1, n)

    epsilon = 1 - 1e-4
    if float(np.abs(pexact - pmode)) / np.abs(np.max(pexact, pmode)) <= 1 - epsilon:
        return odssratio, 1

    elif c[0,0] < mode:
        plower = hypergeom.cdf(c[0,0], n1 + n2, n1, n)

        if hypergeom.pmf(n, n1 + n2, n1, n) > pexact / epsilon:
            return odssratio, plower

        # Binary search for where to begin upper half.
        min = mode
        max = n
        guess = -1
        while max - min > 1:
            guess = max if max == min + 1 and guess == min else (max + min) / 2

            pguess = hypergeom.pmf(guess, n1 + n2, n1, n)
            if pguess <= pexact and hypergeom.pmf(guess - 1, n1 + n2, n1, n) > pexact:
                break
            elif pguess < pexact:
                max = guess
            else:
                min = guess

        if guess == -1:
            guess = min

        while guess > 0 and hypergeom.pmf(guess, n1 + n2, n1, n) < pexact * epsilon:
            guess -= 1

        while hypergeom.pmf(guess, n1 + n2, n1, n) > pexact / epsilon:
            guess += 1

        p = plower + hypergeom.sf(guess - 1, n1 + n2, n1, n)
        if p > 1.0:
            p = 1.0
        return odssratio, p
    else:
        pupper = hypergeom.sf(c[0,0] - 1, n1 + n2, n1, n)
        if hypergeom.pmf(0, n1 + n2, n1, n) > pexact / epsilon:
            return odssratio, pupper

        # Binary search for where to begin lower half.
        min = 0
        max = mode
        guess = -1
        while max - min > 1:
            guess = max if max == min + 1 and guess == min else (max + min) / 2
            pguess = hypergeom.pmf(guess, n1 + n2, n1, n)
            if pguess <= pexact and hypergeom.pmf(guess + 1, n1 + n2, n1, n) > pexact:
                break
            elif pguess <= pexact:
                min = guess
            else:
                max = guess

        if guess == -1:
            guess = min

        while hypergeom.pmf(guess, n1 + n2, n1, n) < pexact * epsilon:
            guess += 1

        while guess > 0 and hypergeom.pmf(guess, n1 + n2, n1, n) > pexact / epsilon:
            guess -= 1

        p = pupper + hypergeom.cdf(guess, n1 + n2, n1, n)
        if p > 1.0:
            p = 1.0
        return odssratio, p


def testFisherExact() :
        # Test hypergeometric survival function against R's, showing that one
        # of them (probably Scipy's) is slightly defective (see the test with
        # significant=1).  This is probably because, in distributions.py, Scipy
        # uses 1.0 - cdf as the sf instead of calculating the sf more directly
        # for improved numerical accuracy.
        #
        # Also note that R and Scipy have different argument formats for their
        # hypergeometric distrib functions.
        #
        # R:
        # > phyper(18999, 99000, 110000, 39000, lower.tail = FALSE)
        # [1] 1.701815e-09

        res = fisher_exact([[18000, 80000], [20000, 90000]])[1]
        assert_approx_equal(res, 0.2751, significant=4)
        res = fisher_exact([[14500, 20000], [30000, 40000]])[1]
        assert_approx_equal(res, 0.01106, significant=4)
        res = fisher_exact([[100, 2], [1000, 5]])[1]
        assert_approx_equal(res, 0.1301, significant=4)
        res = fisher_exact([[2, 7], [8, 2]])[1]
        assert_approx_equal(res, 0.0230141, significant=6)
        res = fisher_exact([[5, 1], [10, 10]])[1]
        assert_approx_equal(res, 0.1973244, significant=6)
        res = fisher_exact([[5, 15], [20, 20]])[1]
        assert_approx_equal(res, 0.0958044, significant=6)
        res = fisher_exact([[5, 16], [20, 25]])[1]
        assert_approx_equal(res, 0.1725862, significant=6)
        res = fisher_exact([[10, 5], [10, 1]])[1]
        assert_approx_equal(res, 0.1973244, significant=6)
        res = fisher_exact([[5, 0], [1, 4]])[1]
        assert_approx_equal(res, 0.04761904)
        res = fisher_exact([[0, 1], [3, 2]])[1]
        assert_approx_equal(res, 1.0)
        res = fisher_exact([[0, 2], [6, 4]])[1]
        assert_approx_equal(res, 0.4545454545)

        # High tolerance due to survival function inaccuracy.
        res = fisher_exact([[19000, 80000], [20000, 90000]])[1]
        assert_approx_equal(res, 3.319e-9, significant=1)


def testfisher_exact() :
    """Just some tests to show that fisher_exact() works correctly."""

    res = fisher_exact([[100, 2], [1000, 5]])
    assert_approx_equal(res[1], 0.1301)
    assert_approx_equal(res[0], 0.25)
    res = fisher_exact([[2, 7], [8, 2]])
    assert_approx_equal(res[1], 0.0230141)
    assert_approx_equal(res[0], 4.0 / 56)
    res = fisher_exact([[5, 1], [10, 10]])
    assert_approx_equal(res[1], 0.1973244)
    res = fisher_exact([[5, 15], [20, 20]])
    assert_approx_equal(res[1], 0.0958044)
    res = fisher_exact([[5, 16], [20, 25]])
    assert_approx_equal(res[1], 0.1725862)
    res = fisher_exact([[10, 5], [10, 1]])
    assert_approx_equal(res[1], 0.1973244)

tablelist = ( [[100, 2], [1000, 5]],
            [[2, 7], [8, 2]],
            [[5, 1], [10, 10]],
            [[5, 15], [20, 20]],
            [[5, 16], [20, 25]],
            [[10, 5], [10, 1]],
            [[10, 5], [10, 0]],
            [[5,0], [1, 4]],
            [[0,5], [1, 4]],
            [[5,1], [0, 4]],
            [[0, 1], [3, 2]] )


for table in tablelist:
    #results from R

    tablist = [
        ([[100, 2], [1000, 5]], (2.505583993422285e-001,  1.300759363430016e-001)),
        ([[2, 7], [8, 2]], (8.586235135736206e-002,  2.301413756522114e-002)),
        ([[5, 1], [10, 10]], (4.725646047336584e+000,  1.973244147157190e-001)),
        ([[5, 15], [20, 20]], (3.394396617440852e-001,  9.580440012477637e-002)),
        ([[5, 16], [20, 25]], (3.960558326183334e-001,  1.725864953812994e-001)),
        ([[10, 5], [10, 1]], (2.116112781158483e-001,  1.973244147157190e-001)),
        ([[10, 5], [10, 0]], (0.000000000000000e+000,  6.126482213438734e-002)),
        ([[5, 0], [1, 4]], (np.inf,  4.761904761904762e-002)),
        ([[0, 5], [1, 4]], (0.000000000000000e+000,  1.000000000000000e+000)),
        ([[5, 1], [0, 4]], (np.inf,  4.761904761904758e-002)),
        ([[0, 1], [3, 2]], (0.000000000000000e+000,  1.000000000000000e+000))
        ]

for table, res in tablist:
    res_r = fisher_exact(np.asarray(table))


if __name__ == "__main__":
        testFisherExact()
