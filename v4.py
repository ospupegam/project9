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
ko_genes_dict_new={}
for p,j in ko_genes_dict.items():
    # print(p)
    # print("".join(j))
    tr=requests.get('http://rest.kegg.jp//link/genes/'+"".join(j))   # get organizm of each ko orthology
    tr_t= tr.text
    tor=[]
    l={}
    for i in org_list:
        if i in tr_t:
            tor.append(i)
        l["".join(j)]=tor
        ko_genes_dict_new[p]=l
print(ko_genes_dict_new)
print("=="*10)
org_dict = {}

for org in org_list:  # creating empty dictionary with keys
    org_dict[org] = []

for v in ko_genes_dict_new.values():  # Looping over the parent dict values
    for ko, org_lst in v.items():  # Lopping over ko:orgs dict for each pathways
        for org in org_lst:  # looping over orgs
            if ko not in org_dict[org]:  # making sure that no repeated items in org list (could be unnecessary step)
                org_dict[org].append(ko)

print(org_dict)

# print("smin",smin,"pti",pti,"fcy",fcy,"tps",tps,"cre",cre,"vcn",vcn,"mng",mng,"olu",olu,"otb",ota,"bpg",bpg,"mis",mis,"mpp",mpp,"csl",csl,"cvr",cvr,"apro",apro)
# print(org_dict)
