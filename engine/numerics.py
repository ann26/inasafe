"""Numerical tools
"""

import numpy
import math
from interpolation1d import interpolate1d


def cdf(x, mu=0, sigma=1, kind='normal'):
    """Cumulative Normal Distribution Function

    Input
        x: scalar or array of real numbers
        mu: Mean value. Default 0
        sigma: Standard deviation. Default 1
        kind: Either 'normal' (default) or 'lognormal'

    Output
        An approximation of the cdf of the normal

    CDF of the normal distribution is defined as
    \frac12 [1 + erf(\frac{x - \mu}{\sigma \sqrt{2}})], x \in \R

    Source: http://en.wikipedia.org/wiki/Normal_distribution
    """

    msg = 'Argument "kind" must be either normal or lognormal'
    assert kind in ['normal', 'lognormal'], msg

    if kind == 'lognormal':
        return cdf(numpy.log(x), mu=mu, sigma=sigma, kind='normal')

    arg = (x - mu) / (sigma * numpy.sqrt(2))
    res = (1 + erf(arg)) / 2

    return res


def cdf_table(z):
    """Cumulative Normal Distribution Function

    Input
        z: scalar or array of real numbers

    Output
        An approximation of the cdf of the normal distribution i.e. erf(z)

    The result is approximated through a table lookup and interpolation
    using values generated by scipy.stats.norm.cdf:

    x = (numpy.arange(100) - 50.) / 10
    y = scipy.stats.norm.cdf(x)
    """

    # Input check
    try:
        len(z)
    except:
        scalar = True
        z = [z]
    else:
        scalar = False

    z = numpy.array(z)

    # Table data
    x = [-5.00, -4.90, -4.80, -4.70, -4.60, -4.50, -4.40, -4.30, -4.20, -4.10,
         -4.00, -3.90, -3.80, -3.70, -3.60, -3.50, -3.40, -3.30, -3.20, -3.10,
         -3.00, -2.90, -2.80, -2.70, -2.60, -2.50, -2.40, -2.30, -2.20, -2.10,
         -2.00, -1.90, -1.80, -1.70, -1.60, -1.50, -1.40, -1.30, -1.20, -1.10,
         -1.00, -0.90, -0.80, -0.70, -0.60, -0.50, -0.40, -0.30, -0.20, -0.10,
          0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00,
          1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.10,
          2.20, 2.30, 2.40, 2.50, 2.60, 2.70, 2.80, 2.90, 3.00, 3.10, 3.20,
          3.30, 3.40, 3.50, 3.60, 3.70, 3.80, 3.90, 4.00, 4.10, 4.20, 4.30,
          4.40, 4.50, 4.60, 4.70, 4.80, 4.90]

    y = [2.86651572e-07, 4.79183277e-07, 7.93328152e-07, 1.30080745e-06,
         2.11245470e-06, 3.39767312e-06, 5.41254391e-06, 8.53990547e-06,
         1.33457490e-05, 2.06575069e-05, 3.16712418e-05, 4.80963440e-05,
         7.23480439e-05, 1.07799733e-04, 1.59108590e-04, 2.32629079e-04,
         3.36929266e-04, 4.83424142e-04, 6.87137938e-04, 9.67603213e-04,
         1.34989803e-03, 1.86581330e-03, 2.55513033e-03, 3.46697380e-03,
         4.66118802e-03, 6.20966533e-03, 8.19753592e-03, 1.07241100e-02,
         1.39034475e-02, 1.78644206e-02, 2.27501319e-02, 2.87165598e-02,
         3.59303191e-02, 4.45654628e-02, 5.47992917e-02, 6.68072013e-02,
         8.07566592e-02, 9.68004846e-02, 1.15069670e-01, 1.35666061e-01,
         1.58655254e-01, 1.84060125e-01, 2.11855399e-01, 2.41963652e-01,
         2.74253118e-01, 3.08537539e-01, 3.44578258e-01, 3.82088578e-01,
         4.20740291e-01, 4.60172163e-01, 5.00000000e-01, 5.39827837e-01,
         5.79259709e-01, 6.17911422e-01, 6.55421742e-01, 6.91462461e-01,
         7.25746882e-01, 7.58036348e-01, 7.88144601e-01, 8.15939875e-01,
         8.41344746e-01, 8.64333939e-01, 8.84930330e-01, 9.03199515e-01,
         9.19243341e-01, 9.33192799e-01, 9.45200708e-01, 9.55434537e-01,
         9.64069681e-01, 9.71283440e-01, 9.77249868e-01, 9.82135579e-01,
         9.86096552e-01, 9.89275890e-01, 9.91802464e-01, 9.93790335e-01,
         9.95338812e-01, 9.96533026e-01, 9.97444870e-01, 9.98134187e-01,
         9.98650102e-01, 9.99032397e-01, 9.99312862e-01, 9.99516576e-01,
         9.99663071e-01, 9.99767371e-01, 9.99840891e-01, 9.99892200e-01,
         9.99927652e-01, 9.99951904e-01, 9.99968329e-01, 9.99979342e-01,
         9.99986654e-01, 9.99991460e-01, 9.99994587e-01, 9.99996602e-01,
         9.99997888e-01, 9.99998699e-01, 9.99999207e-01, 9.99999521e-01]

    r = interpolate1d(x, y, z)

    # Set values outside domain to asymtotic result
    r[z < x[0]] = 0
    r[z > x[-1]] = 1

    if scalar:
        return r[0]
    else:
        return r


def unstable_cdf2(z):
    """Cumulative Distribution Function

    Input
        z: scalar or array of real numbers

    Output
        An approximation of the cdf of the normal distribution i.e. erf(z)

    Sources:
    http://mathworld.wolfram.com/NormalDistribution.html
    http://mathworld.wolfram.com/DistributionFunction.html
    http://en.wikipedia.org/wiki/Error_function


    \frac{2}{\sqrt{\pi}} \sum_0^N \frac{z}{2n+1} \prod_{k=1}^n \frac{-z^2}{k}
    """

    N = 10  # Number of iterations

    sum = 0
    for n in range(N):

        prod = 1
        for i in range(n):
            k = i + 1
            prod *= -(z * z / k)

        den = 2 * n + 1
        term = z * prod / den
        print n, den, term

        sum += term

    return 2 * sum / numpy.sqrt(numpy.pi)


def unstable_cdf(z):
    """Cumulative Distribution Function

    Input
        z: scalar or array of real numbers

    Output
        An approximation of the cdf of the normal distribution i.e. erf(z)

    Sources:
    http://mathworld.wolfram.com/NormalDistribution.html
    http://mathworld.wolfram.com/DistributionFunction.html
    http://en.wikipedia.org/wiki/Error_function


    \frac{2}{\sqrt{\pi}} \sum_0^N \frac{(-1)^n z^{2n+1}}{n! (2n+1)}
    """

    N = 10

    sum = 0
    sign = 1  # (-1)^n
    fact = 1  # n!
    for n in range(N):

        exp = 2 * n + 1

        num = sign * (z ** exp)
        den = fact * exp

        term = num / den
        print n, num, den, term

        sum += term

        sign = -sign
        if n > 0:
            fact = fact * n

    return 2 * sum / numpy.sqrt(numpy.pi)


def erf(z):
    """Approximation to ERF

    from:
    http://www.cs.princeton.edu/introcs/21function/ErrorFunction.java.html
    Implements the Gauss error function.
    erf(z) = 2 / sqrt(pi) * integral(exp(-t*t), t = 0..z)

    Fractional error in math formula less than 1.2 * 10 ^ -7.
    although subject to catastrophic cancellation when z in very close to 0
    from Chebyshev fitting formula for erf(z) from Numerical Recipes, 6.2

    Source:
    http://stackoverflow.com/questions/457408/
    is-there-an-easily-available-implementation-of-erf-for-python
    """

    # Input check
    try:
        len(z)
    except:
        scalar = True
        z = [z]
    else:
        scalar = False

    z = numpy.array(z)

    # Begin algorithm
    t = 1.0 / (1.0 + 0.5 * numpy.abs(z))

    # Use Horner's method
    ans = 1 - t * numpy.exp(-z * z - 1.26551223 +
                           t * (1.00002368 +
                           t * (0.37409196 +
                           t * (0.09678418 +
                           t * (-0.18628806 +
                           t * (0.27886807 +
                           t * (-1.13520398 +
                           t * (1.48851587 +
                           t * (-0.82215223 +
                           t * (0.17087277))))))))))

    neg = (z < 0.0)  # Mask for negative input values
    ans[neg] = -ans[neg]

    if scalar:
        return ans[0]
    else:
        return ans
