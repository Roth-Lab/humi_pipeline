import inflection
import pandas as pd
import tarfile


def main(args):
    trace_files = dict(zip(args.groups, args.trace_files))

    out_df = []

    for group in trace_files:
        with tarfile.open(trace_files[group], "r") as archive:
            fh = archive.extractfile("gof.csv")

            group_df = pd.read_csv(fh)

        group_df = group_df.rename(columns=inflection.underscore)

        group_df["gof_statistic"] = group_df["gof_statistic"].apply(inflection.underscore)

        group_df["group_id"] = group

        out_df.append(group_df)

    out_df = pd.concat(out_df)

    out_df = out_df.rename(columns={"reference_dataset": "sample_id"})

    out_df = out_df[["group_id", "sample_id", "gof_statistic", "theoretical_coverage", "actual_coverage", "width"]]

    out_df = out_df.sort_values(by=["group_id", "sample_id", "gof_statistic"])

    out_df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--groups", nargs="+", required=True)

    parser.add_argument("-t", "--trace-files", nargs="+", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    cli_args = parser.parse_args()

    main(cli_args)
