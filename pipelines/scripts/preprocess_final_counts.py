import os
import pandas as pd
import subprocess


def main(args):
    exe = os.path.join(args.code_dir, 'bin', 'humi-preprocess')

    cmd = [
        exe,
        '--inputs'
    ]

    cmd.extend(args.in_files)

    subprocess.run(cmd, check=True)

    fix_empty_datasets('results/latest/output.csv', args.out_file)


def fix_empty_datasets(in_file, out_file):
    """ Add a dummy entry for datasets with no observed reads for sgRNA.
    """
    df = pd.read_csv(in_file, sep=',')

    if 'dataset.1' in df.columns:
        df = df.drop('dataset.1', axis=1)

    datasets = df['dataset'].unique()

    fix_df = df.groupby(['sgRNA', 'gene']).apply(
        lambda x: fix_empty(datasets, x)
    ).reset_index().drop('level_2', axis=1)

    fix_df.to_csv(out_file, index=False)


def fix_empty(datasets, df):
    df = df.drop(['sgRNA', 'gene'], axis=1)

    empty = set(datasets) - set(df['dataset'].unique())

    empty_df = []

    for d in empty:
        empty_df.append({'dataset': d, 'histogram': '1x1'})

    empty_df = pd.DataFrame(empty_df)

    return pd.concat([df, empty_df])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--code-dir', required=True)

    parser.add_argument('-i', '--in-files', nargs='+', required=True)

    parser.add_argument('-o', '--out-file', required=True)

    cli_args = parser.parse_args()

    main(cli_args)
