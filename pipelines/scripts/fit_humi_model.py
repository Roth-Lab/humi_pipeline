import os
import subprocess
import tarfile


def main(args):
    if args.model == "mix-bnb-local":
        exe = os.path.join(args.code_dir, "bin", "humi-mixbnb-local")

    else:
        model = args.model.replace("-", "")

        exe = os.path.join(args.code_dir, "bin", "humi-{}".format(model))

    cmd = [
        exe,
        "--model.data.source", args.final_counts_file,
        "--model.data.genes.name", "gene",
        "--model.data.targets.name", "sgRNA",
        "--model.data.experiments.name", "dataset",
        "--model.data.histograms.name", "histogram ",
        "--model.initialPopCounts.dataSource", args.initial_counts_file,
        "--model.initialPopCounts.name", "counts",
        "--engine", "PT",
        "--engine.ladder", "Polynomial",
        "--engine.nChains", args.num_chains,
        "--engine.nScans", args.num_iters,
        "--engine.nPassesPerScan", 1,
        "--engine.nThreads", "Fixed",
        "--engine.nThreads.number", args.num_threads,
        "--engine.scmInit.temperatureSchedule.threshold", 0.6,
        "--engine.scmInit.nThreads", "Fixed",
        "--engine.scmInit.nThreads.number", args.num_threads,
        "--engine.scmInit.nParticles", 20,
        "--postProcessor", "humi.HumiPostProcessor",
        "--postProcessor.data.targets.name", "sgRNA",
        "--postProcessor.data.genes.name", "gene",
        "--postProcessor.data.experiments.name", "dataset",
        "--postProcessor.data.histograms.name", "histogram",
        "--postProcessor.credibleIntervalPr", args.ci_width,
        "--postProcessor.runPxviz", "false"
    ]

    subprocess.run([str(x) for x in cmd], check=True)

    with tarfile.open(args.out_file, dereference=True, mode="w:gz") as archive:
        archive.add("results/latest", arcname="")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--code-dir", required=True)

    parser.add_argument("-i", "--initial-counts-file", required=True)

    parser.add_argument("-f", "--final-counts-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    parser.add_argument(
        "-m", "--model",
        choices=["bnb", "nb", "poi", "ys", "mix-bnb", "mix-bnb-local", "mix-gnb", "mix-nb", "mix-ys"]
    )

    parser.add_argument("-nc", "--num-chains", default=18, type=int)

    parser.add_argument("-ni", "--num-iters", default=1000, type=int)

    parser.add_argument("-nt", "--num-threads", default=1, type=int)

    parser.add_argument("--ci-width", default=0.9, type=float)

    cli_args = parser.parse_args()

    main(cli_args)
