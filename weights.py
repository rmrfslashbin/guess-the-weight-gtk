from z3 import *

MAX_TRIES = 10

weights = {
    "bars": [7, 22],
    "plates": {
        "a": {"weight": 13.2, "qty": 4},
        "b": {"weight": 10, "qty": 4},
        "c": {"weight": 8.8, "qty": 6},
        "d": {"weight": 8, "qty": 2},
        "e": {"weight": 5, "qty": 4},
    }
}


def maxWeight():
    total = 0    
    for plate in weights["plates"]:
        total = total + (weights["plates"][plate]["weight"] * weights["plates"][plate]["qty"])
    return total


def test_range(bar, upper, lower):
    # Define the plates
    a, b, c, d, e, q = Ints('a b c d e q')

    # Create a solver
    s = Solver()
    s.add(
        q == 1,  # One and only one bar
        a <= weights["plates"]["a"]["qty"], a >= 0, a % 2 == 0,  # 0 or more plates, must be in pairs
        b <= weights["plates"]["b"]["qty"], b >= 0, b % 2 == 0,
        c <= weights["plates"]["c"]["qty"], c >= 0, c % 2 == 0,
        d <= weights["plates"]["d"]["qty"], d >= 0, d % 2 == 0,
        e <= weights["plates"]["e"]["qty"], e >= 0, e % 2 == 0,
        weights["plates"]["a"]["weight"]*a + \
            weights["plates"]["b"]["weight"] * b + \
            weights["plates"]["c"]["weight"] * c + \
            weights["plates"]["d"]["weight"] * d + \
            weights["plates"]["e"]["weight"] * e + \
            bar * \
            q > lower,  # must be at least
        weights["plates"]["a"]["weight"] * a + \
            weights["plates"]["b"]["weight"] * b + \
            weights["plates"]["c"]["weight"] * c + \
            weights["plates"]["d"]["weight"] * d + \
            weights["plates"]["e"]["weight"] * e + \
            bar * \
            q < upper)  # can't be more than
    
    # Check to see if the plan is sane
    z = s.check()
    if z.r != 1:
        return False
    else:
        return s

def pong(bar, target):
    solution = False
    tries = 0
    eo = True
    while solution == False:
        if eo:
            upper = target + tries + 1
            lower = target + tries - 1
            eo = False
        else:
            upper = target - tries + 1
            lower = target - tries - 1
            eo = True
        tries = tries + 1
        solution = test_range(bar, upper, lower)
        if tries > MAX_TRIES:
            break
    
    if solution:
        final = []
        model = solution.model()
        for plate in model:
            if str(plate) == "q": # skip the bar
                continue
            count = model[plate].as_long()
            weight = weights["plates"][str(plate)]["weight"]
            if count == 0: # skip plates which are not used
                continue
            final.append({"weight": weight, "count": count})
        return final
 
    else:
        return False
