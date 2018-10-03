MIN = 2.3
MAX = 10.5


def _lm(x):
    '''
    x: days passed
    '''
    if x < 1:
        return MAX
    elif x > 17:  # ignore 2.4 result with _lm(18)
        return MIN
    return round(10.510978-0.800944*x+0.019493*x**2, 1)


def calculate(acc_rain, days_passed):
    if acc_rain <= 2.5:
        return 2.3
    for i in range(20):
        if acc_rain > _lm(i):
            return _lm(i+days_passed-1)


def clamp(val):
    if val < MIN:
        return MIN
    elif val > MAX:
        return MAX
    else:
        return val
