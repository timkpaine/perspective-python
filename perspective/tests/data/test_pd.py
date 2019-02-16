from mock import patch
import pandas as pd
import numpy as np
import lantern as l
from perspective import PerspectiveWidget


DF = l.superstore()
LINE = l.line()


class TestPandas:
    def setup(self):
        pass

    def test_rowpivots(self):
        # basic
        df_pivoted = DF.set_index(['Country', 'Region'])
        psp = PerspectiveWidget(df_pivoted)
        assert psp.rowpivots == ['Country', 'Region']
        assert psp.columnpivots == []
        assert sorted(psp.columns) == sorted(['Category', 'City', 'Customer ID', 'Discount', 'Order Date', 'Order ID', 'Postal Code',
                                              'Product ID', 'Profit', 'Quantity', 'Row ID', 'Sales', 'Segment', 'Ship Date',
                                              'Ship Mode', 'State', 'Sub-Category'])
        assert psp.schema == {'Country': 'string', 'Region': 'string', 'Category': 'string', 'City': 'string', 'Customer ID': 'string', 'Discount': 'float',
                              'Order Date': 'string', 'Order ID': 'string', 'Postal Code': 'string', 'Product ID': 'string', 'Profit': 'float', 'Quantity': 'integer',
                              'Row ID': 'integer', 'Sales': 'integer', 'Segment': 'string', 'Ship Date': 'string', 'Ship Mode': 'string', 'State': 'string', 'Sub-Category': 'string'}

    def test_pivottable(self):
        pt = pd.pivot_table(DF, values='Discount', index=['Country', 'Region'], columns='Category')
        psp = PerspectiveWidget(pt)
        assert psp.rowpivots == ['Country', 'Region']
        assert psp.columnpivots == []
        assert psp.columns == ['Consumer Discretionary', 'Consumer Staples', 'Energy', 'Financials',
                               'Health Care', 'Industrials', 'Information Technology', 'Materials', 'Real Estate', 'Telecommunication Services', 'Utilities']
        assert psp.schema == {'Country': 'string', 'Region': 'string', 'Consumer Discretionary': 'float', 'Consumer Staples': 'float', 'Energy': 'float', 'Financials': 'float',
                              'Health Care': 'float', 'Industrials': 'float', 'Information Technology': 'float', 'Materials': 'float', 'Real Estate': 'float',
                              'Telecommunication Services': 'float', 'Utilities': 'float'}

    def test_colpivots(self):
        arrays = [np.array(['bar', 'bar', 'bar', 'bar', 'baz', 'baz', 'baz', 'baz', 'foo', 'foo', 'foo', 'foo', 'qux', 'qux', 'qux', 'qux']),
                  np.array(['one', 'one', 'two', 'two', 'one', 'one', 'two', 'two', 'one', 'one', 'two', 'two', 'one', 'one', 'two', 'two']),
                  np.array(['X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y'])]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second', 'third'])

        df_both = pd.DataFrame(np.random.randn(3, 16), index=['A', 'B', 'C'], columns=index)
        psp = PerspectiveWidget(df_both)
        assert psp.columns == [' ']
        assert psp.columnpivots == ['first', 'second', 'third']
        assert psp.rowpivots == ['index']
        assert psp.schema == {'first': 'string', 'second': 'string', 'third': 'string', 'index': 'string', ' ': 'float'}

    def test_schema_conversion(self):
        pass

    def test_schema_no_ignore(self):
        pass
