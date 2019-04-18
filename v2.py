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

def get_pathways_of_gene(gene_id_):
    gene_link = 'http://rest.kegg.jp/get/'
    ge = requests.get(gene_link+gene_id_)
    m= ge.text.rstrip().split("\n")
    path_of_gene_list=[]
    k=0
    for item in m:
        if item[0:7]=="PATHWAY":
            n1=item[12:20]
            path_of_gene_list.append(n1)
            k=1
        if ((item[0:7]).isspace()) & (k==1):
                n2=item[12:20]
                path_of_gene_list.append(n2)
        if (item[0:6] == "MODULE") | (item[0:5] == "BRITE"):
            break
    return (path_of_gene_list)

gene_dict={}
for item in gene_id_list:
    gene_dict[item]=get_pathways_of_gene(item)
print(gene_dict)