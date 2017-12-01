import re
from shutil import rmtree
from os.path import expanduser, join as path_join

from pandas import DataFrame
from Bio.KEGG import REST

import logging
from ebs.merge_cols import attach_data

from joblib import Memory

default_cache_path = path_join(expanduser("~"), ".joblib/kegg/")
memory = Memory(cachedir=default_cache_path, verbose=0)


@memory.cache(verbose=0)
def get_kegg_data(species, definitions):

    logging.info("Get KEGG path to gene map.")
    kegg_df = get_kegg_path_to_gene_map(species)[["kegg_pathway", "entrezgene"
                                                  ]]

    if definitions:
        logging.info("Get KEGG pathway to definition map.")
        definition_map = get_pathway_to_definition_map(species)

        logging.info("Attaching pathway definitions.")
        kegg_df = attach_data(kegg_df, definition_map, "kegg_pathway",
                              "kegg_pathway")

    return kegg_df


@memory.cache(verbose=0)
def get_pathway_to_definition_map(species):
    """Map kegg paths to their definition."""

    kegg_list = REST.kegg_list("pathway", species)

    clean_kegg_path = re.compile(r"path:{}|\n".format(species))

    rowdicts = []
    for kegg_path_line in kegg_list:

        try:
            kegg_path_line = kegg_path_line.decode("utf-8")
        except AttributeError:
            pass

        kegg_info = re.sub(clean_kegg_path, "", kegg_path_line)
        pathway, definition = kegg_info.split("\t")
        definition = definition.split(" - ")[0]  # Remove species info
        rowdict = {"kegg_pathway": pathway,
                   "kegg_pathway_definition": definition}
        rowdicts.append(rowdict)

    return DataFrame.from_dict(rowdicts)


@memory.cache(verbose=0)
def get_kegg_gene_to_external_map(species):
    """Maps kegg genes to external gene names.

    Legacy function for goverlap. Deprecated. """

    kegg_list = REST.kegg_list(species)

    clean_kegg_info = re.compile(r"{}:|\n".format(species))
    parse_kegg_info = re.compile(r"[^\t;\n]+")

    rowdicts = []
    for kegg_info in kegg_list:

        try:
            kegg_info = kegg_info.decode("utf-8")
        except AttributeError:
            pass
        kegg_info = re.sub(clean_kegg_info, "", kegg_info)
        kegg_data = re.findall(parse_kegg_info, kegg_info)

        for gene in kegg_data[1].split(", "):
            rowdict = {"entrezgene": kegg_data[0], "gene": gene}
            rowdicts.append(rowdict)

    return DataFrame.from_dict(rowdicts)


@memory.cache(verbose=0)
def get_kegg_path_to_gene_map(species):
    """Map kegg paths to genes."""

    kegg_list = REST.kegg_link(species, "pathway")

    clean_kegg_path_to_gene = re.compile(r"path:{0}|{0}:|\n".format(species))

    rowdicts = []
    for kegg_info in kegg_list:

        try:
            kegg_info = kegg_info.decode("utf-8")
        except AttributeError:
            pass
        kegg_info = re.sub(clean_kegg_path_to_gene, "", kegg_info)
        kegg_data = kegg_info.split("\t")

        rowdict = {"kegg_pathway": kegg_data[0], "entrezgene": kegg_data[1]}
        rowdicts.append(rowdict)

    return DataFrame.from_dict(rowdicts)


def remove_cache():
    rmtree(default_cache_path)


@memory.cache(verbose=0)
def get_kegg(species, definitions):
    """Legacy function for goverlap. Deprecated. """

    logging.info("Get KEGG gene to external gene map.")
    gene_map = get_kegg_gene_to_external_map(species)

    logging.info("Get KEGG path to gene map.")
    pathway_map = get_kegg_path_to_gene_map(species)

    if definitions:
        logging.info("Get KEGG pathway to definition map.")
        definition_map = get_pathway_to_definition_map(species)

    logging.info("Connect KEGG gene map and KEGG pathway map.")
    kegg_df = attach_data(pathway_map, gene_map, "entrezgene", "entrezgene")
    kegg_df = kegg_df[["kegg_pathway", "gene"]]

    if definitions:
        logging.info("Attaching pathway definitions.")
        kegg_df = attach_data(kegg_df, definition_map, "kegg_pathway",
                              "kegg_pathway")
        kegg_df = kegg_df[["kegg_pathway", "gene", "kegg_pathway_definition"]]

    return kegg_df
