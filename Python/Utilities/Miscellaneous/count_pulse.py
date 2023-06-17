import numpy as np
from typing import List
import random


def count_digital_pulse(waveform: List[int]):
    """ Count the number of pulses in an array """

    count = []
    pulses = []
    for i in range(0, len(waveform) - 1):
        curr = waveform[i]
        next = waveform[i + 1]
        count.append(curr)
        if next != curr:
            pulses.append(count)
            count = []

    pulses = [list(set(m))[0] for m in pulses]
    return pulses.count(1)


N = random.randint(1, 9) * 10
P = 10
D = P / 2
sig = np.arange(N) % P < D
sig = [int(b) for b in sig]

sig.insert(0, 0)
sig.insert(0, 1)
sig.insert(0, 1)
sig.insert(0, 0)
sig.insert(0, 1)

print(sig)
print(count_digital_pulse(sig))
