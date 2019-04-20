import requests
import re
p = requests.get('http://rest.kegg.jp/list/pathway/ath') # pathways of ath organusm
print(p.text)
path_id_list=[]
for line in p.text.rstrip().split("\n"):
    n = re.findall(r":(ath\d{0,})", line)
    path_id_list.append("".join(n))
print(path_id_list)
no_pathways_org=len(path_id_list)
r = requests.get('http://rest.kegg.jp/link/ath/ath04626') # select ath04626 pathway to study.
print(r.text)
gene_id_list=[]
for lineg in r.text.rstrip().split("\n"):
    n = re.findall(r"(ath:AT[\d][G]\d{0,})", lineg)
    gene_id_list.append("".join(n))
print(gene_id_list) # gene list of ath04626 pathway
print(type(gene_id_list))
ko_genes=[]
ko_genes_dict={}
for gene in gene_id_list:
    orth = requests.get('http://rest.kegg.jp/link/ko/'+gene)
    n = re.findall(r"(ko:K\d{0,})", orth.text)
    ko_genes_dict[gene] = n
print(ko_genes_dict) # orthology of each gene in gene list

org_list=["smin","pti","fcy","tps","cre","vcn","mng","olu","ota","bpg","mis","mpp","csl","cvr","apro"]
