import requests
import re
import json
import numpy as np

def get_plantPathways(plant):
    f1=open('pathwayoforg.txt','w+')
    p = requests.get('http://rest.kegg.jp/list/pathway/'+plant) # pathways of plant organusm by kegg api
    f1.write(p.text) # put output from kegg to file to can deal with it
    path_id_list=[]
    f2='pathwayoforg.txt'
    for line in open(f2):
        kg = line.split()[0][5:] # to extract pathways names from each line of file
        path_id_list.append(kg) # append each pathways from above to list
    f1.close()
    return path_id_list # output : list of pathways that append each time.

def get_geneforPathways(plant,path):
    p = requests.get('http://rest.kegg.jp/link/' + plant +'/'+path)  # gene of pathways of plant organusm
    gene_id_list = []
    #ncbi_g_list=[]
    for line in p.text.rstrip().split('\n'): # remove space and split line by tap to separate first element from second
        kg = line.split('\t')[1] # extract second item ( kegg gene id) from line and append it to list
        gene_id_list.append(kg)
    return gene_id_list

def ncbi_gene_id_conv(gene_list):
    j=[]
    for i in gene_list:
        try:  # avoid that orthologygene don't have ncbi id in kegg data base and make loop continue
            ncbi_g = requests.get('http://rest.kegg.jp/conv/ncbi-geneid/'+i) # from keggapi to get ncbi gene id for each kegg gene id
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (ncbi_g.text and not ncbi_g.text.isspace()):
            j.append(ncbi_g.text.rstrip("\n").split(':')[2]) # extract second item ( ncbi gene id) from line and append it to list
    return j

def getOrthGroup(gene_list):
    ko_genes={}
    for gene in gene_list:
        try:          # avoid gene don't have orthologous one in kegg data base and make loop continue
            orth = requests.get('http://rest.kegg.jp/link/ko/'+gene) # get orthology of gene from kegg data base
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (orth.text and not orth.text.isspace()):
            line= orth.text.rstrip()
            kg = line.split('\t')[1]  # extract second item ( kegg gene id) from line and append it to list
            ko_genes[gene]=kg
    return ko_genes

def algae_org(alga_orgamism):
    s = requests.get('http://rest.kegg.jp/list/organism') # pathways of ath organusm
    org_list=[]
    for line in s.text.rstrip().split("\n"):
        for org in alga_orgamism:
            if org in line:
                j=line.split()[1]
                org_list.append(j)
    return org_list

alga_orgamism=["algae","Diatoms","Dinoflagellates"]
org_list=algae_org(alga_orgamism)
#org_list=["smin","pti","fcy","tps","cre","vcn","mng","olu","ota","bpg","mis","mpp","csl","cvr","apro"]
#k_genes=['ko:K15397', 'ko:K05391', 'ko:K13448', 'ko:K13436', 'ko:K13447', 'ko:K13460', 'ko:K13448', 'ko:K05391']
def orthKoDict(dict,org_list):
    o_dict={}
    for gene,k in dict.items():
        o_dict[k] = {}
        try: # avoid gene don't have orthology one in kegg data base and make loop continue
            g=requests.get('http://rest.kegg.jp//link/genes/'+dict[gene][3:]) # get orthologies gene for each ko from kegg database
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (g.text and not g.text.isspace()):
            d= []
            for line in g.text.rstrip().split("\n"):
                for org in org_list:
                    if (org in line):
                        orthologous_genes=line.split()[1]
                        d.append(orthologous_genes)
            o_dict[k]=d
            dict[gene]=o_dict
    return dict
#print(orthologs_group_(org_list,k_genes))

# plants,algae=get_plant_or_alge_list()  # get plants list using subfunction get_plant_or_alge_list that found in plant_or_algae_list.py
plants=["ath"]
#org_list=["smin","pti","fcy","tps","cre","vcn","mng","olu","ota","bpg","mis","mpp","csl","cvr","apro"]

# create nested dictionary, first one to contain plant organism as a keys and make second dictionary as a values of first one
# second dictionary contain a pathways of plant organism as a keys and list of gene of each pathways as a values.
plant_dict = {}
for plant in plants:  # creating empty nested dictionary with keys
    plant_dict[plant] = {}

path_dict={}
# for plant in plants:
#     path_dict[plant]={}
kg_dict={}
for plant in plants:
    paths = get_plantPathways(plant) # get pathways of plant org by using get_plantPathways in get_plantPathways
    #path_dict[plant]=paths
    for path in paths:
        if path == "ath04626":
            ge=get_geneforPathways(plant,"ath04626")
            print(ge)
            print(type(ge))
            path_dict[path]=ge
            k_dict=getOrthGroup(ge)
            print(k_dict)
            orthKoGen=orthKoDict(k_dict, org_list)
            print(orthKoGen)
            kg_dict[path]=orthKoGen
            print(kg_dict)
    plant_dict[plant]=kg_dict

# showing results as json formate with indent and put it to file to easy show
#print(json.dumps(plant_dict,indent=4))
json=json.dumps(plant_dict,indent=4)
myfile=open("outkogenpath.txt","w+")
myfile.write(json)
myfile.close()

plant_statis={}
ko_statis={}
gene_statis={}
orth_gen_statis={}
orth_count=0
list1=[]
for k,v in plant_dict.items():
    for c,b in v.items():
        #gene_statis[c]=len(b)
        for x,z in b.items():
            #ko_statis[x]=len(z)
            for g,i in z.items():
                print(len(i))
                print(g)
                orth_gen_statis[g]=len(i)
                orth_count=orth_count+len(i)
            ko_statis[x]=orth_gen_statis
        gene_statis[c]=ko_statis
    plant_statis[k]=gene_statis
print(orth_count)
print(orth_gen_statis)
print(ko_statis)
print(gene_statis)
#j=json.dumps(plant_statis,indent=4)
myfile2=open("outstatistic.txt","w+")
myfile2.write(str(plant_statis))
myfile2.close()

list1=[]
for k,v in plant_statis.items():
    for c,b in v.items():
        for x,s in b.items():
            list1.append(list(s.values()))
n=np.array(list1)
print(n)
h=np.sum(n, axis=1)
print(h)

myfile3=open("outgene-koarray.txt","w+")
myfile3.write(n)
myfile3.close()