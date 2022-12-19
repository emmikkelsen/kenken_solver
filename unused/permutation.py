from ..src.kenken_solver.operation import Operation


def permutation(max_value: int, group_size: int, op: Operation, result: int):
    """
    Generate all com
    """
    if op == Operation.Divide:
        maxes = list(filter(lambda x: x % result == 0 and x > 0,
                            range(max_value+1)))
        mins = [m//result for m in maxes]
        p = []
        for x in range(len(maxes)):
            p.append([maxes[x], mins[x]])
            p.append([mins[x], maxes[x]])
        return p

    if op == Operation.Subtract:
        maxes = list(filter(lambda x: x > result, range(max_value+1)))
        mins = [m-result for m in maxes]
        p = []
        for x in range(len(maxes)):
            p.append([maxes[x], mins[x]])
            p.append([mins[x], maxes[x]])
        return p

    if op == Operation.Add:
        return pe_add(max_value, result, group_size)

    if op == Operation.Multiply:
        return pe_multiply(max_value, result, group_size)


def pe_add(ma, res, n):
    if n == 1:
        return [[res]]
    t = []
    for x in range(1, ma+1):
        if (res-x)/(n-1) <= ma and res-x >= n-1:
            for ss in pe_add(ma, res-x, n-1):
                t.append(ss + [x])
    return t


def pe_multiply(ma, res, n):
    if n == 1:
        return [[res]]
    t = []
    factors = list(filter(lambda x: res % x == 0, range(1, ma+1)))
    for x in factors:
        if res//x <= ma**(n-1):
            for ss in pe_multiply(ma, res//x, n-1):
                t.append(ss + [int(x)])
    return t
