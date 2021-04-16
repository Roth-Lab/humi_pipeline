import os
import shutil
import subprocess
import tarfile


def main(args):
    with tarfile.open(args.in_file, 'r') as archive:
        archive.extract('estimates.csv')

    exe = os.path.join(args.code_dir, 'bin', 'humi-poset')

    cmd = [
        exe,
        '--intervalsCSVFile', 'estimates.csv',
    ]

    subprocess.run([str(x) for x in cmd], check=True)

    shutil.copyfile('results/latest/hasse.dot', args.out_file)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--code-dir', required=True)

    parser.add_argument('-i', '--in-file', required=True)

    parser.add_argument('-o', '--out-file', required=True)

    cli_args = parser.parse_args()

    main(cli_args)
