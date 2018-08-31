"""Analyze the latency data and provide a report."""

import os
from warnings import warn

import pandas as pd

# The sampling frequency of the BrainVision equipment in Hz
SAMPLING_FREQUENCY = 5000

# Path to data directory
file_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(file_dir, 'data')


def read_vmrk(vmrk_path, key1, key2):
    """Read a BrainVision .vmrk file.

    Reads a .vmrk file, parsing the occurrences of a
    marker ``key1`` and a marker ``key2`` in samples
    and returns their occurrences as a 2D array.

    Parameters
    ----------
    vmrk_path : str
        Path to a .vmrk file

    key1, key2 : str
        String describing the two keys, which to parse
        from the .vmrk file

    Returns
    -------
    df : pandas DataFrame
        Contains the n detected markers and their occurrences
        in samples. First column: marker index (1 or 2),
        second column, occurrence in samples.

    """
    if not vmrk_path.endswith('.vmrk'):
        raise ValueError('input path must be a .vmrk file!')

    # Read the data
    with open(vmrk_path, 'r') as fin:
        lines = fin.readlines()

    # Go through the whole doc
    info = []
    for line in lines:
        # Skip all non-related lines
        if not line.startswith('Mk'):
            continue

        # If we have a marker line, extract the information we want
        mtype, mdesc, onset = line.split(',')[:3]
        if mdesc in [key1, key2]:
            info.append([mdesc, onset])

    # Reformat as pandas DataFrame
    df = pd.DataFrame(info, columns=['mdesc', 'onset'])

    return df


def assert_df_integrity(df):
    """Assert that the df is in the format we want."""
    # df should have two keys
    keys = df.mdesc.unique()
    if len(keys) != 2:
        raise ValueError('df should contain exactly two keys.')
    else:
        key1, key2 = keys

    # key1 needs to come first
    if df.mdesc.tolist()[0] != key1:
        raise ValueError('Key1 should be first in df. '
                         'Re-read .vmrk with proper arguments.')

    # ... always followed by a key2. Thus, last key should be key2
    if df.mdesc.tolist()[-1] != key2:
        raise ValueError('Key2 should be last in df. '
                         'For every sent key1, there should be a key2 next. '
                         'Perhaps, re-do collect_data.py')

    # ... thus, length needs to be even
    if len(df.mdesc) % 2 != 0:
        raise ValueError('df should have an even length.')

    # Assert ordering is key1, key2, key1, ... , key2
    prev = df.mdesc[0]
    for i in df.mdesc[1::]:
        if prev == i:
            raise ValueError('Keys 1 and 2 must always alternate')
        prev = i

    # Assert the onsets are all integers
    for i in df.onset:
        if not isinstance(i, int):
            raise ValueError('All onsets must be integers')

    # Assert the onsets are monotonously increasing
    prev = df.onset[0]
    for i in df.onset[1::]:
        if prev >= i:
            print(prev, i, prev >= i)
            raise ValueError('Onsets must be monotonously increasing')
        prev = i


if __name__ == '__main__':
    warn('Assuming sampling frequency of {} Hz.'
         ' Make sure this is true!'.format(SAMPLING_FREQUENCY))
