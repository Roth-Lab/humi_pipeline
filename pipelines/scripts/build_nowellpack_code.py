import os
import re
import shutil
import subprocess


def main(args):
    """ Download and build latest version of HUMI
    """
    subprocess.run(['git', 'clone', 'https://github.com/UBC-Stat-ML/nowellpack.git'])

    os.chdir('nowellpack')

    subprocess.run(['git', 'checkout', 'humi-v1.3'])

    set_monitor_params(
        'src/main/java/humi/DistributionSummary.xtend', args.truncation_cutoff, args.winsorization_cutoff
    )

    subprocess.run(['./gradlew', 'clean'])

    subprocess.run(['./gradlew', 'installDist'])

    shutil.move(os.path.join('build', 'install', 'nowellpack'), os.path.join(args.out_dir))


def set_monitor_params(file_name, truncation_cutoff, winsorization_cutoff):
    with open(file_name, 'r') as fh:
        out_lines = []

        for line in fh:
            if line.strip().startswith('static val cutoff'):
                line = re.sub(r'\d+', str(truncation_cutoff), line)

            elif line.strip().startswith('static val winsorizationP'):
                line = re.sub(r'\d*[.,]?\d* /', '{} /'.format(winsorization_cutoff), line)

            out_lines.append(line)

    with open(file_name, 'w') as fh:
        fh.writelines(out_lines)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--out-dir', required=True)

    parser.add_argument('-t', '--truncation-cutoff', type=int)

    parser.add_argument('-w', '--winsorization-cutoff', type=float)

    cli_args = parser.parse_args()

    main(cli_args)
