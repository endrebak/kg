"""
kegg

Get KEGG data from the command line.

Visit github.com/endrebak/kegg for docs and help.

Usage:
    kegg --keggcol=KEGG --species=SPEC (--definition | --gene) [--noheader] FILE
    kegg --genecol=GENE --species=SPEC [--noheader] FILE
    kegg --species=SPEC

Arguments:
    FILE                    infile to add KEGG data to (supports piping)
    -k KEGG --keggcol=KEGG  column with kegg ids
    -g GENE --genecol=GENE  column with gene ids
    -s SPEC --species=SPEC  name of species

Options:
    -h --help               show this message
    -n --noheader             the input data contains a header
"""

from __future__ import print_function

from sys import stdout
import re

from pandas import DataFrame
from Bio.KEGG import REST

from docopt import docopt
from joblib import Memory


memory = Memory(cachedir=".joblib", verbose=0)


@memory.cache(verbose=0)
def get_kegg(species):

    kegg_list = REST.kegg_list(species)
    rowdicts = _get_rowdicts(species, kegg_list)

    return DataFrame.from_dict(rowdicts)[["pathway_id", "gene", "definition"]]


def _get_rowdicts(species, kegg_list):

    clean_kegg_info = re.compile(r"{}:|\n".format(species))
    parse_kegg_info = re.compile(r"[^\t;\n]+")

    rowdicts = []
    for kegg_info in kegg_list:

        kegg_info = re.sub(clean_kegg_info, "", kegg_info)
        kegg_data = re.findall(parse_kegg_info, kegg_info)

        for gene in kegg_data[1].split(", "):
            rowdict = {"pathway_id": kegg_data[0], "gene": gene,
                       "definition": ";".join(kegg_data[2:])}

            rowdicts.append(rowdict)

    return rowdicts


if __name__ == '__main__':

    args = docopt(__doc__)

    input_df = read_indata(args["FILE"], args["--noheader"])

    input_df.to_csv(stdout, sep="\t")

    # kegg_df = get_kegg(args["--species"])
    # kegg_df.to_csv(stdout, sep="\t", index=False)
