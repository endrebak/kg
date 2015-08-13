# kg
Query KEGG from the command line

# Bug
Note that there is a bug that causes kg to return invalid kegg path ids; see the example below. My mistake; I was using undocumented BioPython code to do this, and I just assumed that the numbers were pathway IDs. This is the first thing on my TODO-list - expect a correction next week, around Monday the 17. of August.

```
kg

Get KEGG data from the command line.
(Visit github.com/endrebak/kg for examples and help.)

Usage:
    kg --help
    kg --mergecol=COL --species=SPEC [--genes] [--definitions] [--noheader] FILE
    kg --species=SPEC
    kg --removecache

Arguments:
    FILE                    infile to add KEGG data to (read STDIN with -)
    -s SPEC --species=SPEC  name of species (examples: hsa, mmu, rno...)
    -m COL --mergecol=COL   column (0-indexed int or name) containing gene names

Options:
    -h --help               show this message
    -n --noheader           the input data does not contain a header
    -d --definitions        add KEGG pathway definitions to the output
    -g --genes              get the genes related to KEGG pathways
                            (when used, mergecol COL should contain KEGG pathway
                            ids)
    --removecache           removes the local cache so that the KEGG REST DB is
                            accessed anew
```

### Example

```bash

$ head examples/no_index_header.tsv
logFC	AveExpr
Ipcef1	-2.70987558746701	4.80047582653889
Sema3b	2.00143465979322	3.82969788437155
Rab26	-2.40250648553797	5.57320249609294
Arhgap25	-1.84668909768998	3.66617832656769
Ociad2	-1.99052684394044	5.26213130909702
Mmp17	-2.01026790614161	4.88012776225311
C4a	2.22003976804983	3.52842041243544
Gna14	-2.42391191670209	1.56313048066253
Kcna6	-1.74168813159872	6.54586068659631

$ kg -s rno -m 0 -d examples/no_index_header.tsv
index	logFC	AveExpr	kegg_pathway	kegg_definition
Ipcef1	-2.70987558746701	4.80047582653889	361474	 interaction protein for cytohesin exchange factors 1
Sema3b	2.00143465979322	3.82969788437155	363142	 sema domain, immunoglobulin domain (Ig), short basic domain, secreted, (semaphorin) 3B; K06840 semaphorin 3
Rab26	-2.40250648553797	5.57320249609294	171111	 RAB26, member RAS oncogene family; K07913 Ras-related protein Rab-26
Arhgap25	-1.84668909768998	3.66617832656769	500246	 Rho GTPase activating protein 25
Ociad2	-1.99052684394044	5.26213130909702	100361733	 OCIA domain containing 2
Mmp17	-2.01026790614161	4.88012776225311	288626	 matrix metallopeptidase 17; K07997 matrix metalloproteinase-17 (membrane-inserted) [EC:3.4.24.-]
C4a	2.22003976804983	3.52842041243544	24233	 complement component 4A (Rodgers blood group); K03989 complement component 4
Gna14	-2.42391191670209	1.56313048066253	309242	 guanine nucleotide binding protein, alpha 14; K04636 guanine nucleotide-binding protein subunit alpha-14
Gna14	-2.42391191670209	1.56313048066253	314046	 ankyrin repeat and MYND domain containing 2
Kcna6	-1.74168813159872	6.54586068659631	64358	 potassium channel, voltage gated shaker related subfamily A, member 6; K04879 potassium voltage-gated channel Shaker-related subfamily A member 6
```

As you can see above:
* When several pathways are associated with a gene, that gene row is duplicated
* `kg` supports `R style ".tsv"` files where the index column lacks a header

### Install

```bash
pip install kg
```
