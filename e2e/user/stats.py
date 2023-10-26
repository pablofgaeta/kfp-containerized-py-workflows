import numpy as np


def gen_sample(n: int) -> np.ndarray:
    return np.random.rand(n)


def sample_mean(sample: np.ndarray) -> float:
    return float(sample.mean())
