import inflection
import os
import pandas as pd
import tarfile


class Trace(object):
    """ Class for loading files from HUMI BLANG trace.
    """

    def __init__(self, trace_file, burnin=0):
        self.burnin = burnin

        self.trace_file = trace_file

        self.tables = self._parse_tables()

    def load_table(self, name):
        name = inflection.camelize(name, False)

        with tarfile.open(self.trace_file, 'r') as archive:
            fh = archive.extractfile('samples/{}.csv'.format(name))

            df = pd.read_csv(fh)

            df = df[df['sample'] >= self.burnin]

        if 'value' in df.columns:
            df['value'] = df['value'].astype(float)

        return df

    def _parse_tables(self):
        tables = []

        with tarfile.open(self.trace_file, 'r') as archive:
            for x in archive.getnames():
                if os.path.basename(os.path.dirname(x)) == 'samples':
                    table_name = inflection.underscore(os.path.splitext(os.path.basename(x))[0])

                    if not table_name.startswith('.'):
                        tables.append(table_name)

        return tables
