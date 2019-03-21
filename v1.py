from Bio.KEGG import REST
aaf_pathways=REST.kegg_list("pathway", "aaf").read()
print(aaf_pathways)
print(
    '=='*10
)
phagosome_pathways = []
for line in aaf_pathways.rstrip().split("\n"):
    entry, description = line.split("\t")
    if "Phagosome" in description:
        phagosome_pathways.append(entry)
print(phagosome_pathways)

phagosome_genes = []
for pathway in phagosome_pathways:
    pathway_file = REST.kegg_get(pathway).read()
    print("**"*10)
    print(pathway_file)
    current_section = None
    for line in pathway_file.rstrip().split("\n"):
        section = line[:12].strip()
        if not section == "":
            current_section = section

        if current_section == "GENE":
            gene_identifiers, gene_description = line[12:].split("; ")
            gene_id, gene_symbol = gene_identifiers.split()

            if not gene_symbol in phagosome_genes:
                phagosome_genes.append(gene_symbol)

print("There are %d repair pathways and %d repair genes. The genes are:" % \
      (len(phagosome_pathways), len(phagosome_genes)))
print(", ".join(phagosome_genes))