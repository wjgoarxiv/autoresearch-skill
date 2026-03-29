#!/usr/bin/env python3
"""Prediction function — the file the agent modifies.

The agent iterates on this function to minimize RMSE against test data.
"""

import math


def predict(x: float) -> float:
    """Predict y given x. Modify this function to fit the data."""
    w1 = 1.0 / math.sqrt(2.0)  # 0.7071...
    w2 = math.sqrt(2.0)         # 1.4142...
    return (
        0.528967
        + -0.451777 * math.cos(w1 * x)
        + -0.356047 * math.sin(w1 * x)
        + 0.131052 * math.cos(w2 * x)
        + 0.092643 * math.sin(w2 * x)
        + 0.002284 * math.cos(3.04 * x)
        + 0.493439 * math.sin(3.04 * x)
        + 0.304401 * math.cos(7.0 * x)
        + -0.002329 * math.sin(7.0 * x)
    )
