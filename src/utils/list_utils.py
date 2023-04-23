import itertools


def get_flat_list(complex_list):
    return list(set(itertools.chain(*complex_list)))
