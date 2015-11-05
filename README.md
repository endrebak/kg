# kg

kg is a Python CLI/API that enables retrieving KEGG pathways, their definitions,
and their related genes.

##Changelog

```
# 0.0.7 (05.11.2015)
- Now uses entrezgene instead of ambiguous gene names.
- Add version info (kg -v).
```

```
kg

Get KEGG data from the command line.
(Visit github.com/endrebak/kg for examples and help.)

Usage:
    kg --help
    kg --version
    kg --mergecol=COL --species=SPEC [--genes] [--definitions] [--noheader] FILE
    kg --species=SPEC
    kg --removecache

Arguments:
    FILE                    infile to add KEGG data to (read STDIN with -)
    -s SPEC --species=SPEC  name of species (examples: hsa, mmu, rno...)
    -m COL --mergecol=COL   column (0-indexed int or name) containing gene names

Options:
    -h --help               show this message
    -v --version            show version info
    -n --noheader           the input data does not contain a header
    -d --definitions        add KEGG pathway definitions to the output
    -g --genes              get the genes related to KEGG pathways
                            (when used, mergecol COL should contain KEGG pathway
                            ids)
    --removecache           removes the local cache so that the KEGG REST DB is
                            accessed anew
```

### CLI

```bash
kg -s rno -d | head
Cache path is: /Users/endrebakkenstovner/.kegg/ (Time:  Thu, 05 Nov 2015 20:00:43 )
kegg_pathway	entrezgene	kegg_pathway_definition
00010	100145871	Glycolysis / Gluconeogenesis
00010	100364027	Glycolysis / Gluconeogenesis
00010	100364062	Glycolysis / Gluconeogenesis
00010	100911515	Glycolysis / Gluconeogenesis
00010	100911625	Glycolysis / Gluconeogenesis
00010	114508	Glycolysis / Gluconeogenesis
00010	117098	Glycolysis / Gluconeogenesis
00010	171178	Glycolysis / Gluconeogenesis
00010	24172	Glycolysis / Gluconeogenesis
```

As you can see above:
* When several pathways are associated with a gene, that gene row is duplicated
* `kg` supports `R style ".tsv"` files where the index column lacks a header

### API

```python
from kegg.lib import get_kegg_data

pathway_definitions = True

df = get_kegg_data("rno", pathway_definitions)

df.head(5)
# Output
#   kegg_pathway entrezgene       kegg_pathway_definition
# 0        00010  100145871  Glycolysis / Gluconeogenesis
# 1        00010  100364027  Glycolysis / Gluconeogenesis
# 2        00010  100364062  Glycolysis / Gluconeogenesis
# 3        00010  100911515  Glycolysis / Gluconeogenesis
# 4        00010  100911625  Glycolysis / Gluconeogenesis
```

### Gene names

The gene names returned by `kg` are of the type entrezgene.
If you'd like a different type of gene identifier, please use [biomartian](https://github.com/endrebak/biomartian) to convert them.

### Install

```bash
pip install kg
```
