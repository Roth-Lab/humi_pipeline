import inflection
import pandas as pd
import os
import scipy.stats
import subprocess


def main(args):
    a = (1 - args.ci_width) / 2

    criticla_value = scipy.stats.norm.ppf(1 - a)

    exe = os.path.join(args.code_dir, "bin", "humi-delta")

    cmd = [
        exe,
        "--initialPopCounts.dataSource", args.initial_counts_file,
        "--initialPopCounts.name", "counts",
        "--data.source", args.final_counts_file,
        "--data.targets.name", "sgRNA",
        "--data.genes.name", "gene",
        "--data.experiments.name", "dataset",
        "--data.histograms.name", "histogram",
        "--criticalValue", criticla_value,
        "--winsorizedTailCutoff", args.tail_cutoff
    ]

    subprocess.run([str(x) for x in cmd], check=True)

    df = pd.read_csv("results/latest/estimates.csv")

    df = df.rename(columns=inflection.underscore)

    df = df[["dataset", "gene", "sgrna", "log_ratio", "log_ratio_left_bound", "log_ratio_right_bound"]]

    df = df.sort_values(by=["dataset", "sgrna"])

    df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--code-dir", required=True)

    parser.add_argument("-i", "--initial-counts-file", required=True)

    parser.add_argument("-f", "--final-counts-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    parser.add_argument("--ci-width", default=0.9, type=float)

    parser.add_argument("--tail-cutoff", default=0.99, type=float)

    cli_args = parser.parse_args()

    main(cli_args)
