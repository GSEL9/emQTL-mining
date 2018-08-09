# -*- coding: utf-8 -*-
#
# cluster.py
#

"""
Wrappers for R biclustering algorithms.
"""

__author__ = 'Severin E. R. Langberg'
__email__ = 'Langberg91@gmail.no'


import numpy as np
import rpy2.robjects as robjects

from base import RBiclusterBase


class ChengChurch(RBiclusterBase):
    """A wrapper for the R BCCC algorithm."""

    MODEL = 'BCCC'

    # Hyperparameters
    params = {
        'delta': 0.1,
        'alpha': 1.5,
        'number': 100
    }

    def __init__(self, random_state=0, **kwargs):

        super().__init__(random_state, **kwargs)

        # Update parameters.
        for key in kwargs:
            if key in self.params.keys():
                self.params[key] = kwargs[key]

        self.set_params(**kwargs)

        # NOTE:
        self._output = None

        self.rows_ = None
        self.columns_ = None
        self.biclusters_ = None

    def fit(self, X, y=None, **kwargs):

        self._fit(self.MODEL, X, self.params)

        return self


class XMotifs(RBiclusterBase):
    """A wrapper for the R BCXmotifs algorithm."""

    MODEL = 'BCXmotifs'

    # Hyperparameters
    params = {
        'number': 1,
        'ns': 200,
        'nd': 100,
        'sd': 5,
        'alpha': 0.05
    }

    def __init__(self, random_state=0, **kwargs):

        super().__init__(random_state, **kwargs)

        # Update parameters.
        for key in kwargs:
            if key in self.params.keys():
                self.params[key] = kwargs[key]

        self.set_params(**kwargs)

        # NOTE:
        self._output = None

        self.rows_ = None
        self.columns_ = None
        self.biclusters_ = None

    def fit(self, X, y=None, **kwargs):

        self._fit(self.MODEL, X, self.params)

        return self


class Plaid(RBiclusterBase):
    """A wrapper for R the BCPlaid algorithm."""

    MODEL = 'BCPlaid'

    # Hyperparameters
    params = {
        'cluster': 'b',
        'fit_model': robjects.r('y ~ m + a + b'),
        'background': True,
        'row_release': 0.7,
        'col_release': 0.7,
        'shuffle': 3,
        'back_fit': 0,
        'max_layers': 20,
        'iter_startup': 5,
        'iter_layer': 10,
        'back_fit': 0,
        'verbose': False
    }

    def __init__(self, random_state=0, **kwargs):

        super().__init__(random_state, **kwargs)

        # Update parameters.
        for key in kwargs:
            if key in self.params.keys():
                self.params[key] = kwargs[key]

        self.set_params(**kwargs)

        # NOTE:
        self._output = None

        self.rows_ = None
        self.columns_ = None
        self.biclusters_ = None

    def fit(self, X, y=None, **kwargs):

        self._fit(self.MODEL, X, self.params)

        return self


if __name__ == '__main__':

    import datasets
    import model_selection

    import numpy as np
    import pandas as pd

    from sklearn.datasets import samples_generator as sgen
    from sklearn.cluster import SpectralBiclustering
    from sklearn.metrics import consensus_score
    from sklearn.datasets import make_biclusters
    from sklearn.datasets import samples_generator as sg

    data_feats = pd.read_csv(
        './../data/data_characteristics.csv', sep='\t', index_col=0
    )
    test_data, rows, cols = datasets.gen_test_sets(
        data_feats,
        sparse=[False, True, False, True],
        non_neg=[False, True, False, True],
        shape=(500, 300),
        n_clusters=5,
        seed=0
    )
    rmodels_and_params = [
        (
            ChengChurch, {
                'delta': [0.1, 0.2],
            }
        ),
    ]
    data = test_data[data_feats.index[0]]
    _rows = rows[data_feats.index[0]]
    _cols = cols[data_feats.index[0]]

    for key in test_data.keys():
        test_data[key] = data
        rows[key] = _rows
        cols[key] = _cols

    experiment = model_selection.Experiment(rmodels_and_params, verbose=2)
    experiment.execute(test_data, (rows, cols), target='score')