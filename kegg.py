"""
kegg

Get KEGG data from the command line.

Visit github.com/endrebak/kegg for docs and help.

Usage:
    kegg --keggcol=KEGG --species=SPEC (--definition | --gene) [--noheader] FILE
    kegg --genecol=GENE --species=SPEC [--noheader] FILE

Arguments:
    FILE                    infile to add KEGG data to (supports piping)
    -k KEGG --keggcol=KEGG  column with kegg ids
    -g GENE --genecol=GENE  column with gene ids
    -s SPEC --species=SPEC  name of species

Options:
    -h --help                  show this message
    -n --noheader              the input data does not contain a header
"""

from __future__ import print_function

from docopt import docopt

def get_kegg(species):

    import re
    import pandas as pd
    from Bio.KEGG import REST

    kegg_list = REST.kegg_list(species)
    clean_kegg_info = re.compile(r"{}:|\n".format(species))
    parse_kegg_info = re.compile(r"[^\t;\n]+")

    rowdicts = []
    for kegg_info in kegg_list:

        kegg_info = re.sub(clean_kegg_info, "", kegg_info)
        kegg_data = re.findall(parse_kegg_info, kegg_info)

        rowdict = {"pathway_id": kegg_data[0], "genes": kegg_data[1].split(", "),
                   "definition": kegg_data[2:]}
        rowdicts.append(rowdict)

    return pd.DataFrame.from_dict(rowdicts)


if __name__ == '__main__':

    args = docopt(__doc__)

    kegg_df = get_kegg(args["--species"])
