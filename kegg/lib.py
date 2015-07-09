
import re
from shutil import rmtree

from pandas import DataFrame
from Bio.KEGG import REST


from joblib import Memory


memory = Memory(cachedir="kegg_cache", verbose=0)

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


def remove_cache():
    rmtree("kegg_cache")
