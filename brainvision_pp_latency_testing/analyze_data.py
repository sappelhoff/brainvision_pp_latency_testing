"""Analyze the latency data and provide a report."""

import os
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    skip = True
    skip_until = 'Mk6'
    print('NOTE: Skipping until line starts with {}'.format(skip_until))
    for line in lines:
        
        if line.startswith('Mk6'):
            skip = False

        # Skip all non-related lines
        if skip:
            continue

        # If we have a marker line, extract the information we want
        mtype, mdesc, onset = line.split(',')[:3]
        if mdesc in [key1, key2]:
            info.append([mdesc, int(onset)])

    # Reformat as pandas DataFrame
    df = pd.DataFrame(info, columns=['mdesc', 'onset'])

    return df


def _assert_df_integrity(df, key1='R128', key2='S  1'):
    """Assert that the df is in the format we want."""
    # df should have two keys
    keys = df.mdesc.unique()
    if len(keys) != 2:
        raise ValueError('df should contain exactly two keys.')

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
        if prev > i:
            print(prev, i, prev > i)
            raise ValueError('Onsets must be monotonously increasing')
        prev = i

    return True


def analyze_df(df, key1='R128', key2='S  1'):
    """Analyze a vmrk df and print out some stats."""
    # First check the df is in our expected format
    assert _assert_df_integrity(df)

    # Now get the differences between markers in samples
    diffs = []
    prev_onset = df.onset[0]
    for i, onset in enumerate(df.onset[1::]):
        # Skip every second marker because we only measure differences
        # between pairs ... not across last of previous pair and first of
        # current pair
        if i % 2 != 0:
            prev_onset = onset
            continue
        else:
            diffs.append(onset - prev_onset)
            prev_onset = onset

    # Print the stats
    diffs = np.asarray(diffs)
    print('Analyzing differences between {} sent triggers'.format(len(diffs)))
    print('"{}" comes after "{}" with a delay of:'.format(key2, key1))
    print('------------------------------------')
    print('Mean {} samples'.format(np.mean(diffs).round(3)))
    print('STD: {} samples'.format(np.std(diffs).round(3)))
    print('Median: {} samples'.format(np.median(diffs).round(3)))

    return diffs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', '-f', type=str, required=True)
    args = parser.parse_args()

    print('Analyzing: {}'.format(args.file))

    # NOTE: edit the key1 and key2 to your needs.
    df = read_vmrk(args.file, key1='R128', key2='S  1')
    _assert_df_integrity(df, key1='R128', key2='S  1')
    diffs = analyze_df(df, key1='R128', key2='S  1')

    # Make a histogram plot
    hist_plot = pd.Series(diffs).plot.hist()
    hist_plot.set_title('Histogram of {} triggers.\n'
                        'Results for "{}"'.format(len(diffs), args.file))
    hist_plot.set_xlabel('Delay in samples')
    hist_plot.set_ylabel('count')
    plt.show()
