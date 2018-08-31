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


if __name__ == '__main__':
    warn('Assuming sampling frequency of {} Hz.'
         ' Make sure this is true!'.format(SAMPLING_FREQUENCY))
