# Replicating the original HUMI manuscript

Details of how to run an example dataset from the manuscript describing the HUMI model are in the `readme.txt` file included in the repository.

General details on how to run and install the pipeline are given below.

# Installation

**1) Install Miniconda**

To install this pipeline you must first have a working `conda` installation. You can get this by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

**2) Remove old HUMI conda environment (optional)**

If you have previously installed an older version of humi remove the environmnet as follows.

```bash
conda env remove -n humi
```

**3) Create you new HUMI conda environment**

You can create the required `conda` environment as follows.

First install `mamba` which is required by Snakemake, the workflow software that runs the pipeline.

```bash
conda install -n base -c conda-forge mamba
```

Next install Snakemake.

```bash
conda activate base
mamba create -c conda-forge -c bioconda -n humi snakemake
```

**4) Download the HUMI pipeline code**

You can get the latest version of the HUMI from the GitHub repo as as follows.

```bash
git clone https://github.com/aroth85/humi_pipeline
```

# Running

**1) Activate your conda environment**

First we need to activate the conda environment so you have the correct packages to run the pipeline. To do so run the following command.

```bash
conda activate humi
```

if this was succesfull the command line should look something like

```bash
(humi) bash-4.1$
```

> Note: You will need to activate the conda environment everytime you login. The currently active conda environment is shown on the command line in brackets i.e. (humi) above.

**2) Change into the HUMI pipeline code directory**

You will need to change into the directory which contains the HUMI pipeline code you downloaded in the final installation step.

**3) Run an analysis**

Inside the git repo for the HUMI pipeline there is a script called `run.py`. You can see the command line options for it by running.

```bash
./run.py -h
```

For example the following command will run a short analysis on your local machine using the input file `examples/C2271.tsv` in the HUMI pipeline directory.

```bash
./run.py -i examples/C2271.tsv -o examples/output -m mix-nb -d PATH_TO_HUMI_PIPELINE/examples
```

Replace PATH_TO_HUMI_PIPELINE with the absolute path where you downloaded the HUMI pipeline code.
This command will run four analyses.
One analyses grouping each replicate and one analysis per replicate treated as singles.

In this example we pass four options to `run.py`

- `-m` - The model to use. To see choices run `run.py -h`.

- `-i` - The path to the input file. See below for details of file format.

- `-o` - The path to the directory where output will be written. For this example we will write files inside the HUMI pipeline directory. In general it is better to output the files somewhere outside the code directory.

- `-d` - The path where the input data is stored. This flag is required if the paths in the file specified by `-i` are _relative_ paths. In this case it is assumed these paths are relative to `{DATA_DIR}` where you will replace this with the relevant path. If the paths in file specified by `-i` are absolute this command can be ommited.

There are some other useful options that can be specified.

- `-b` - The number of samples to discard from the start of the MCMC chain as burnin.

- `-c` - The number of parallel tempering chains to be used. This should be an integer.

- `-n` - The number of post burnin MCMC samples to collect.

- `-t` - The number of threads to use when fitting the HUMI model with BLANG.

- `-j` - The number of jobs to run in parallel.

- `--cluster` - If you are running the pipeline on the shahlab cluster set this flag. Jobs will automatically be submitted using `qsub`.

- `--comparison-file` - This specifies a comparison file for comparing pairs of experiments. This runs the poset analysis to identify sgRNA with significantly different fitnesses between experiments. See below for details of file format.

- `--ci-width` - Confidence interval width. Default is 0.9.

- `--truncation-cutoff` - Cutoff value for computing truncated GOF statistics. Default is 20.

- `--winsorization-cutoff` - Cutoff for cimputing winsorization GOF statistics. Default is 0.9.

- `--dry-run` - Do a dry run an print out files that will be generated but do not execute any commands.

- `--no-unpack` - Do not unpack the trace tar files. Useful for saving space.

## Input

### Paths file `-i`

To run the pipeline you will need to create an input file which specifies the location of the data files to analyze. This file will be passed to the pipeline using the `-i` flag. This file should have four named columns

- group_id - Specifies the dataset group

- sample_id - Unique identifier for a dataset

- initial_counts_path - Path to initial counts library file

- final_counts_path - Path to UMI counts from experiment

The file paths can be relative to a directory, in which case the `-d` flag should be used with the pipeline. Example files are in the `examples` sub-directory of the pipeline.

### Comparison file `--comparison-file`

If you which to identify sgRNAs that have significantly different fitness between experiments you need to input this file with the `--comparison-file` flag. The file is a Tab delimited file with the following columns.

- group_1 - The first group (experiment) to compare.

- group_2 - The second group (experiment) to compare.

This groups must match one of the group_id entries in the paths file. There is an example file `examples/test/comparison.tsv` in the HUMI pipeline code directory.
