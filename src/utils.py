"""
Utilities
=========

Author: Jiayi (Jason) Liu
Date: 7/8/2018

"""

import logging

import pickle
import pandas as pd
from iexfinance import get_historical_data

logger = logging.getLogger(__name__)


def get_history(start_time, end_time, stocks):
    """
    Get the historical data from iexfinance

    :param start_time: start time (datetime obj, e.g. `datatime.today()`)
    :param end_time: end time (datetime obj, e.g. `datatime.today()`)
    :param stocks: stock names
    :return: {"name": `pd.DataFrame`}
    """
    history = {}
    for s in stocks:
        history[s] = get_historical_data(s.upper(), start=start_time, end=end_time, output_format='pandas')
        history[s].index = pd.to_datetime(history[s].index)
    return history


def save_history(history, filename):
    with open(filename, 'wb') as f:
        pickle.dump(history, f)


def restore_history(history, filename):
    with open(filename,'rb') as f:
        return pickle.load(f)