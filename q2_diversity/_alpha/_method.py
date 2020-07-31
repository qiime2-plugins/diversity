# ----------------------------------------------------------------------------
# Copyright (c) 2016-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from inspect import signature
from functools import partial
import warnings

import unifrac

from q2_diversity_lib.alpha import METRICS

_all_phylo_metrics = METRICS['PHYLO']['IMPL'] | METRICS['PHYLO']['UNIMPL']
_all_nonphylo_metrics = METRICS['NONPHYLO']['IMPL'] \
                       | METRICS['NONPHYLO']['UNIMPL']

METRIC_NAME_TRANSLATIONS = {'shannon': 'shannon_entropy',
                            'pielou_e': 'pielou_evenness'}


# TODO: remove these collections ASAP
def phylogenetic_metrics():
    return {'faith_pd'}


# must contain an entry for every metric in phylogenetic_metrics
def _phylogenetic_functions():
    return {'faith_pd': unifrac.faith_pd}


def non_phylogenetic_metrics():
    return {'ace', 'chao1', 'chao1_ci', 'berger_parker_d', 'brillouin_d',
            'dominance', 'doubles', 'enspie', 'esty_ci', 'fisher_alpha',
            'goods_coverage', 'heip_e', 'kempton_taylor_q', 'margalef',
            'mcintosh_d', 'mcintosh_e', 'menhinick', 'michaelis_menten_fit',
            'observed_features', 'osd', 'pielou_e', 'robbins', 'shannon',
            'simpson', 'simpson_e', 'singles', 'strong', 'gini_index',
            'lladser_pe', 'lladser_ci'}


def alpha_phylogenetic(ctx, table, phylogeny, metric):
    f = ctx.get_action('diversity_lib', 'alpha_phylogenetic_dispatch')
    result = f(table, phylogeny, metric)
    return tuple(result)


def alpha(ctx, table, metric):
    implemented_metrics = METRICS['NONPHYLO']['IMPL']
    if metric not in _all_nonphylo_metrics:
        raise ValueError("Unknown metric: %s" % metric)

    metric = METRIC_NAME_TRANSLATIONS[metric] if (
            metric in METRIC_NAME_TRANSLATIONS) else metric

    if metric in implemented_metrics:
        func = ctx.get_action('diversity_lib', metric)
        func = partial(func, table=table)
    else:
        func = ctx.get_action('diversity_lib', 'alpha_passthrough')
        func = partial(func, table=table, metric=metric)

    result = func()
    return tuple(result)
