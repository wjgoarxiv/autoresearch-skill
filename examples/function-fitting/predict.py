#!/usr/bin/env python3
"""Prediction function -- the file the agent modifies.

The agent iterates on this function to minimize RMSE against test data.
"""

import math


def predict(x: float) -> float:
    """5-frequency Fourier model (1/sqrt2, sqrt2, 3.035, 7, 12.765), all-data fit."""
    w1 = 1.0 / math.sqrt(2.0)
    w2 = math.sqrt(2.0)
    return (
        0.532033202580
        - 0.456144410031 * math.cos(w1 * x)
        - 0.355008142293 * math.sin(w1 * x)
        + 0.132890795776 * math.cos(w2 * x)
        + 0.093317344327 * math.sin(w2 * x)
        + 0.001263084552 * math.cos(3.035 * x)
        + 0.500776833061 * math.sin(3.035 * x)
        + 0.304077064361 * math.cos(7.0 * x)
        + 0.002067368681 * math.sin(7.0 * x)
        + 0.001401769134 * math.cos(12.765 * x)
        - 0.006746571636 * math.sin(12.765 * x)
    )
