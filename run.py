#!/usr/bin/env python3
import json
import os
import re

from snakemake import snakemake


def main(args):
    config = get_config(args)

    pipeline_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pipelines")

    if args.cluster:
        cluster_log_dir = os.path.join(args.out_dir, "log")

        if not os.path.exists(cluster_log_dir):
            os.makedirs(cluster_log_dir)

        cluster_cmd = "sbatch --export=ALL -n {threads} -p upgrade --mem={cluster.mem}"

        restart_times = 2

    else:
        cluster_cmd = None

        restart_times = 0

    old_cluster_config_file = os.path.join(pipeline_dir, "config", "analysis", "cluster.json")

    new_cluster_config_file = os.path.join(args.out_dir, "tmp", "cluster.json")

    write_cluster_config(old_cluster_config_file, new_cluster_config_file, threads=args.num_threads)

    snakemake(
        cluster=cluster_cmd,
        cluster_config=new_cluster_config_file,
        config=config,
        cores=args.num_jobs,
        dryrun=args.dry_run,
        force_incomplete=True,
        nodes=args.num_jobs,
        printshellcmds=True,
        restart_times=restart_times,
        snakefile=os.path.join(pipeline_dir, "analysis.smk"),
        workdir=pipeline_dir,
        latency_wait=args.latency_wait,
        use_conda=True
    )


def get_config(args):
    config = {
        "paths_file": os.path.abspath(args.in_file),
        "out_dir": os.path.abspath(args.out_dir),
        "model": args.model,
        "num_chains": args.num_chains,
        "num_iters": args.num_iters,
        "num_threads": args.num_threads,
        "ci_width": args.ci_width,
        "truncation_cutoff": args.truncation_cutoff,
        "winsorization_cutoff": args.winsorization_cutoff
    }

    if args.code_dir is not None:
        config["code_dir"] = args.code_dir

    if args.data_dir is not None:
        config["data_dir"] = args.data_dir

    return config


def write_cluster_config(in_file, out_file, threads=1):
    if not os.path.exists(os.path.dirname(out_file)):
        os.makedirs(os.path.dirname(out_file))

    with open(in_file, "r") as fh:
        config = json.load(fh)

    with open(out_file, "w") as fh:
        json.dump(config, fh)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in-file", required=True)

    parser.add_argument("-o", "--out-dir", required=True)

    parser.add_argument(
        "-m",
        "--model",
        choices=["bnb", "mix-bnb", "mix-bnb-local", "nb", "mix-nb", "mix-gnb", "poi", "ys", "mix-ys"],
        required=True
    )

    parser.add_argument("-d", "--data-dir", default=None)

    parser.add_argument("-c", "--num-chains", default=18, type=int)

    parser.add_argument("-n", "--num-iters", default=1999, type=int)

    parser.add_argument("-t", "--num-threads", default=1, type=int)

    parser.add_argument("-j", "--num-jobs", default=1, type=int)

    parser.add_argument("--cluster", action="store_true", default=False)

    parser.add_argument("--code-dir", default=None)

    parser.add_argument("--dry-run", action="store_true", default=False)

    parser.add_argument("--latency-wait", default=60, type=int)

    parser.add_argument("--ci-width", default=0.9, type=float)

    parser.add_argument("--truncation-cutoff", default=20, type=int)

    parser.add_argument("--winsorization-cutoff", default=0.9, type=float)

    cli_args = parser.parse_args()

    main(cli_args)
