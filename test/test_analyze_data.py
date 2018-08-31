"""Test the data analysis."""

import os

import pandas as pd

from brainvision_pp_latency_testing import read_vmrk


# Path to data directory
file_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(file_dir, 'data')

test_vmrk = os.path.join(test_data_dir, 'test.vmrk')


def test_read_vmrk():
    """Test the marker reading."""
    # Test it properly reads the test file and returns a data frame
    df = read_vmrk(test_vmrk, 'S  1', 'S  2')
    assert isinstance(df, pd.core.frame.DataFrame)
