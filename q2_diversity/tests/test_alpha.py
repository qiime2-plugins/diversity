# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

import io
import biom
import skbio
import qiime
import numpy as np
import pandas as pd
import pandas.util.testing as pdt

from q2_diversity import alpha, alpha_phylogenetic, alpha_correlation


class AlphaTests(unittest.TestCase):

    def test_alpha(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        actual = alpha(table=t, metric='observed_otus')
        # expected computed by hand
        expected = pd.Series({'S1': 1, 'S2': 2, 'S3': 2}, name='observed_otus')
        pdt.assert_series_equal(actual, expected)

    def test_alpha_phylo_metric(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        with self.assertRaises(ValueError):
            alpha(table=t, metric='faith_pd')

    def test_alpha_unknown_metric(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        with self.assertRaises(ValueError):
            alpha(table=t, metric='not-a-metric')

    def test_alpha_phylogenetic(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        tree = skbio.TreeNode.read(io.StringIO(
            '((O1:0.25, O2:0.50):0.25, O3:0.75)root;'))
        actual = alpha_phylogenetic(table=t, phylogeny=tree, metric='faith_pd')
        # expected computed with skbio.diversity.alpha_diversity
        expected = pd.Series({'S1': 0.75, 'S2': 1.0, 'S3': 1.0},
                             name='faith_pd')
        pdt.assert_series_equal(actual, expected)

    def test_alpha_phylogenetic_non_phylo_metric(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        tree = skbio.TreeNode.read(io.StringIO(
            '((O1:0.25, O2:0.50):0.25, O3:0.75)root;'))
        with self.assertRaises(ValueError):
            alpha_phylogenetic(table=t, phylogeny=tree, metric='observed_otus')

    def test_alpha_phylogenetic_unknown_metric(self):
        t = biom.Table(np.array([[0, 1, 3], [1, 1, 2]]),
                       ['O1', 'O2'],
                       ['S1', 'S2', 'S3'])
        tree = skbio.TreeNode.read(io.StringIO(
            '((O1:0.25, O2:0.50):0.25, O3:0.75)root;'))
        with self.assertRaises(ValueError):
            alpha_phylogenetic(table=t, phylogeny=tree, metric='not-a-metric')


class AlphaCorrelationTests(unittest.TestCase):

    def test_spearman(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['1.0', '2.0', '3.0']},
                         index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            alpha_correlation(output_dir, alpha_div, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            jsonp_fp = os.path.join(output_dir, 'category-value.jsonp')
            self.assertTrue(os.path.exists(jsonp_fp))

            self.assertTrue('Spearman' in open(jsonp_fp).read())
            self.assertTrue('"sampleSize": 3' in open(jsonp_fp).read())
            self.assertTrue('"data":' in open(jsonp_fp).read())
            self.assertFalse('filtered' in open(jsonp_fp).read())

    def test_pearson(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['1.0', '2.0', '3.0']},
                         index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            alpha_correlation(output_dir, alpha_div, md, method='pearson')
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            jsonp_fp = os.path.join(output_dir, 'category-value.jsonp')
            self.assertTrue(os.path.exists(jsonp_fp))

            self.assertTrue('Pearson' in open(jsonp_fp).read())
            self.assertTrue('"sampleSize": 3' in open(jsonp_fp).read())
            self.assertTrue('"data":' in open(jsonp_fp).read())
            self.assertFalse('filtered' in open(jsonp_fp).read())

    def test_bad_method(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.MetadataCategory(
            pd.Series(['1.0', '2.0', '3.0'], name='value',
                      index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaises(ValueError):
                alpha_correlation(output_dir, alpha_div, md, method='bad!')

    def test_bad_metadata(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['a', 'b', 'c']},
                         index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaises(ValueError):
                alpha_correlation(output_dir, alpha_div, md)

    def test_nan_metadata(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['1.0', '2.0', '']},
                         index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            alpha_correlation(output_dir, alpha_div, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            jsonp_fp = os.path.join(output_dir, 'category-value.jsonp')
            self.assertTrue(os.path.exists(jsonp_fp))

            self.assertTrue('"filtered": 2' in open(jsonp_fp).read())
            self.assertTrue('"initial": 3' in open(jsonp_fp).read())

    def test_extra_metadata(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['1.0', '2.0', '3.0', '4.0']},
                         index=['sample1', 'sample2', 'sample3', 'sample4']))
        with tempfile.TemporaryDirectory() as output_dir:
            alpha_correlation(output_dir, alpha_div, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            jsonp_fp = os.path.join(output_dir, 'category-value.jsonp')
            self.assertTrue(os.path.exists(jsonp_fp))

            self.assertTrue('"sampleSize": 3' in open(jsonp_fp).read())

    def test_extra_alpha_div(self):
        alpha_div = pd.Series([2.0, 4.0, 6.0, 8.0], name='alpha-div',
                              index=['sample1', 'sample2', 'sample3',
                                     'sample4'])
        md = qiime.Metadata(
            pd.DataFrame({'value': ['1.0', '2.0', '3.0']},
                         index=['sample1', 'sample2', 'sample3']))
        with tempfile.TemporaryDirectory() as output_dir:
            alpha_correlation(output_dir, alpha_div, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            jsonp_fp = os.path.join(output_dir, 'category-value.jsonp')
            self.assertTrue(os.path.exists(jsonp_fp))

            self.assertTrue('"sampleSize": 3' in open(jsonp_fp).read())
