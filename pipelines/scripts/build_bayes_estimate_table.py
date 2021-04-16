import inflection
import pandas as pd
import tarfile


def main(args):
    with tarfile.open(args.in_file, "r") as archive:
        fh = archive.extractfile("estimates.csv")

        df = pd.read_csv(fh)

    df = df.rename(columns=inflection.underscore)

    df = df[["gene", "sgrna", "log_ratio", "log_ratio_left_bound", "log_ratio_right_bound"]]

    df.to_csv(args.out_file, index=False, sep="\t")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in-file", required=True)

    parser.add_argument("-o", "--out-file", required=True)

    cli_args = parser.parse_args()

    main(cli_args)
