import os
import pandas as pd
import shutil

import utils

config_manager = utils.ConfigManager(config)

onsuccess:
    config_manager.cleanup()

localrules: all, build_humi_code, unpack_results

rule all:
    input:
        config_manager.pipeline_output_files

rule build_humi_code:
    output:
        directory(config_manager.code_dir)
    conda:
        "envs/blang.yaml"
    shadow:
        "shallow"
    shell:
        "python scripts/build_nowellpack_code.py "
        "-o {output} "
        "-t {config[truncation_cutoff]} "
        "-w {config[winsorization_cutoff]}"

rule preprocess_final_counts:
    input:
        code_dir = config_manager.code_dir,
        in_files = config_manager.get_final_counts_file
    output:
        config_manager.preprocessed_final_counts_template
    conda:
        "envs/blang.yaml"
    shadow:
        "shallow"
    shell:
        "python scripts/preprocess_final_counts.py -c {input.code_dir} -i {input.in_files} -o {output}"

rule fit_humi:
    input:
        code_dir = config_manager.code_dir,
        initial_counts = config_manager.get_initial_counts_file,
        final_counts = config_manager.preprocessed_final_counts_template
    output:
        config_manager.trace_file_template
    conda:
        "envs/blang.yaml"
    log:
        err = os.path.join(config_manager.log_dir, "fit", "{group}.err"),
        out = os.path.join(config_manager.log_dir, "fit", "{group}.out")
    shadow:
        "shallow"
    threads:
        config['num_threads']
    shell:
        "python scripts/fit_humi_model.py "
        "-c {input.code_dir} "
        "-i {input.initial_counts} "
        "-f {input.final_counts} "
        "-o {output} "
        "-m {config[model]} "
        "-nc {config[num_chains]} "
        "-ni {config[num_iters]} "
        "-nt {config[num_threads]} "
        "--ci-width {params} {config[ci_width]}"
        "> {log.out} "
        "2> {log.err}"

rule unpack_results:
    input:
        config_manager.trace_file_template
    output:
        directory(config_manager.trace_dir_template)
    shell:
        "mkdir -p {output} && tar -zxvf {input} -C {output}"

rule build_coverage_table:
    input:
        expand(config_manager.trace_file_template, group=config_manager.groups)
    output:
        config_manager.coverage_table
    conda:
        "envs/python.yaml"
    params:
        ' '.join(config_manager.groups)
    shell:
        "python scripts/build_coverage_table.py -g {params} -t {input} -o {output}"

rule build_bayes_estimate_table:
    input:
        config_manager.trace_file_template
    output:
        config_manager.bayes_estimate_table_template
    conda:
        "envs/python.yaml"
    shell:
        "python scripts/build_bayes_estimate_table.py -i {input} -o {output}"

rule build_poset:
    input:
        code = config_manager.code_dir,
        trace = config_manager.trace_file_template
    output:
        config_manager.poset_dot_template
    conda:
        "envs/blang.yaml"
    shadow:
        "shallow"
    shell:
        "python scripts/build_poset.py -c {input.code} -i {input.trace} -o {output}"

rule plot_poset:
    input:
        config_manager.poset_dot_template
    output:
        config_manager.poset_plot_template
    conda:
        "envs/blang.yaml"
    shell:
        "dot {input} -Tpdf -o {output}"

rule build_frequentist_estimate_table:
    input:
        code = config_manager.code_dir,
        init = config_manager.get_initial_counts_file,
        final = config_manager.preprocessed_final_counts_template
    output:
        config_manager.frequentist_estimate_table_template
    conda:
        "envs/blang.yaml"
    shadow:
        "shallow"
    shell:
        "python scripts/build_frequentist_estimate_table.py "
        "-c {input.code} "
        "-f {input.final} "
        "-i {input.init} "
        "-o {output} "
        "--ci-width {config[ci_width]} "
        "--tail-cutoff {config[winsorization_cutoff]}"
