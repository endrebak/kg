# kg
Query KEGG from the command line

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
index	logFC	AveExpr	kegg_pathway	kegg_pathway_definition
Ipcef1	-2.70987558746701	4.80047582653889
Sema3b	2.00143465979322	3.82969788437155	04360	Axon guidance
Rab26	-2.40250648553797	5.57320249609294
Arhgap25	-1.84668909768998	3.66617832656769
Ociad2	-1.99052684394044	5.26213130909702
Mmp17	-2.01026790614161	4.88012776225311
C4a	2.22003976804983	3.52842041243544	04610	Complement and coagulation cascades
C4a	2.22003976804983	3.52842041243544	05133	Pertussis
C4a	2.22003976804983	3.52842041243544	05150	Staphylococcus aureus infection
C4a	2.22003976804983	3.52842041243544	05322	Systemic lupus erythematosus
Gna14	-2.42391191670209	1.56313048066253	04020	Calcium signaling pathway
Gna14	-2.42391191670209	1.56313048066253	05142	Chagas disease (American trypanosomiasis)
Gna14	-2.42391191670209	1.56313048066253	05146	Amoebiasis
Kcna6	-1.74168813159872	6.54586068659631
```

As you can see above:
* When several pathways are associated with a gene, that gene row is duplicated
* `kg` supports `R style ".tsv"` files where the index column lacks a header

### Install

```bash
pip install kg
```
