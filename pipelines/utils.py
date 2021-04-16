import os
import pandas as pd
import shutil


class ConfigManager(object):
    def __init__(self, config):
        self.config = config

        self._init_paths_df()

    @property
    def groups(self):
        return self.paths_df["group_id"].unique()

    @property
    def pipeline_output_files(self):
        files = []

        files.extend(self.get_group_file_list(self.trace_file_template))

        if self.config.get("unpack", True):
            files.extend(self.get_group_file_list(self.trace_dir_template))

        files.extend(self.get_group_file_list(self.bayes_estimate_table_template))

        files.extend(self.get_group_file_list(self.frequentist_estimate_table_template))

        files.extend(self.get_group_file_list(self.poset_plot_template))

        files.append(self.coverage_table)

        return files

    @property
    def bayes_estimate_table_template(self):
        return os.path.join(self.tables_dir, "estimates", "bayes", "{group}.tsv")

    @property
    def code_dir(self):
        return self.config.get("code_dir", os.path.join(self.out_dir, "code/humi"))

    @property
    def coverage_table(self):
        return os.path.join(self.tables_dir, "coverage.tsv")

    @property
    def data_dir(self):
        return self.config.get("data_dir", None)

    @property
    def final_counts_files_dict(self):
        return self.paths_df.groupby('group_id')['final_counts_path'].apply(list).to_dict()

    @property
    def frequentist_estimate_table_template(self):
        return os.path.join(self.tables_dir, "estimates", "frequentist", "{group}.tsv")

    @property
    def initial_counts_files_dict(self):
        return self.paths_df.set_index("group_id")["initial_counts_path"].to_dict()

    @property
    def log_dir(self):
        return os.path.join(self.out_dir, "log")

    @property
    def merged_final_counts_template(self):
        return os.path.join(self.out_dir, "input", "merged_final_counts", "{group}.csv")

    @property
    def plots_dir(self):
        return os.path.join(self.out_dir, "plots")

    @property
    def poset_dir(self):
        return os.path.join(self.out_dir, "poset")

    @property
    def poset_comparison_dir_template(self):
        return os.path.join(self.poset_dir, "comparison", "{group_1}_vs_{group_2}")

    @property
    def poset_dot_template(self):
        return os.path.join(self.poset_dir, "experiment", "{group}.dot")

    @property
    def poset_plot_template(self):
        return os.path.join(self.plots_dir, "poset", "{group}.pdf")

    @property
    def preprocessed_final_counts_tmp_template(self):
        return os.path.join(self.tmp_dir, "preprocessed_final_counts", "{group}.csv")

    @property
    def preprocessed_final_counts_template(self):
        return os.path.join(self.out_dir, "input", "final_counts", "{group}.csv")

    @property
    def out_dir(self):
        return self.config["out_dir"]

    @property
    def tables_dir(self):
        return os.path.join(self.out_dir, "tables")

    @property
    def tmp_dir(self):
        return os.path.join(self.out_dir, "tmp")

    @property
    def trace_dir_template(self):
        return os.path.join(self.out_dir, "trace", "unpacked", "{group}")

    @property
    def trace_file_template(self):
        return os.path.join(self.out_dir, "trace", "archived", "{group}.tar.gz")

    @property
    def unpack(self):
        return self.config["unpack"]

    def cleanup(self):
        if os.path.exists(self.log_dir):
            shutil.rmtree(self.log_dir)

        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def get_final_counts_file(self, wc):
        return self.final_counts_files_dict[wc.group]

    def get_group_file_list(self, template):
        return [template.format(group=x) for x in self.groups]

    def get_initial_counts_file(self, wc):
        return self.initial_counts_files_dict[wc.group]

    def _init_paths_df(self):
        self.paths_df = pd.read_csv(self.config["paths_file"], sep="\t")

        if self.data_dir is not None:
            self.paths_df["final_counts_path"] = self.paths_df["final_counts_path"].apply(
                lambda x: os.path.join(self.data_dir, x)
            )

            self.paths_df["initial_counts_path"] = self.paths_df["initial_counts_path"].apply(
                lambda x: os.path.join(self.data_dir, x)
            )
