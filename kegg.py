"""
kegg

Get KEGG data from the command line.

Merge related KEGG pathway IDs on COL, where COL contains gene names.

Visit github.com/endrebak/kegg for docs and help.

Usage:
    kegg --incol=COL --species=SPEC [--get-genes] [--definitions] [--noheader] FILE
    kegg --species=SPEC

Arguments:
    FILE                    infile to add KEGG data to (supports piping with -)
    -s SPEC --species=SPEC  name of species
    -c COL --incol=COL      column (zero-indexed number or name) containing gene
                            names of the type called "external_gene_name" or
                            "Associated Gene Name" in BioMart.
                            (when --get-genes is used, COL should contain
                            KEGG pathway ids)

Options:
    -h --help               show this message
    -n --noheader           the input data contains a header
    -g --get-genes          get the genes related to KEGG pathway ids
    -a --definitions        add KEGG pathway definitions to the output
"""


from __future__ import print_function

from sys import stdout
import re

from pandas import DataFrame
from Bio.KEGG import REST

from docopt import docopt
from joblib import Memory

from ebs.read_indata import read_indata
from ebs.merge_cols import attach_data


memory = Memory(cachedir=".joblib", verbose=0)

@memory.cache(verbose=0)
def get_kegg(species):

    kegg_list = REST.kegg_list(species)
    rowdicts = _get_rowdicts(species, kegg_list)

    return DataFrame.from_dict(rowdicts)[["kegg_pathway", "gene",
                                          "kegg_definition"]]


def _get_rowdicts(species, kegg_list):

    clean_kegg_info = re.compile(r"{}:|\n".format(species))
    parse_kegg_info = re.compile(r"[^\t;\n]+")

    rowdicts = []
    for kegg_info in kegg_list:

        kegg_info = re.sub(clean_kegg_info, "", kegg_info)
        kegg_data = re.findall(parse_kegg_info, kegg_info)

        for gene in kegg_data[1].split(", "):
            rowdict = {"kegg_pathway": kegg_data[0], "gene": gene,
                       "kegg_definition": ";".join(kegg_data[2:])}

            rowdicts.append(rowdict)

    return rowdicts


if __name__ == '__main__':

    args = docopt(__doc__)

    input_df = read_indata(args["FILE"], args["--noheader"])

    kegg_df = get_kegg(args["--species"])
    kegg_df.to_csv("genes.txt", sep="\t", index=False)

    kegg_col_to_merge_on = 0 if args["--gene"] else 1

    final_df = attach_data(input_df, kegg_df, args["--incol"], 1)
    final_df.to_csv(stdout, sep="\t", index=False)
