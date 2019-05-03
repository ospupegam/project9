import requests
import pyham
import logging

orth = requests.get('http://rest.kegg.jp/link/ko/ath:AT1G01120')
print(str(orth.text)

r1 = requests.get('https://api.kegg.net/conv//ncbi-geneid/ath:AT1G01120')
print(str(r1.text))

# con = requests.get('http://rest.kegg.jp/conv/ncbi-geneid/ath:AT1G01120')
# print(con.text)
# ath:AT1G01120	ncbi-geneid:839395
#
# print('=='*30)
# my_gene_query = 'P53_RAT'
# database_to_query = 'oma'
# pyham_analysis = pyham.Ham(query_database=my_gene_query, use_data_from=database_to_query)
# ham_analysis = pyham.Ham(tree_str, orthoxml_path, use_internal_name=True)
# #f=open("pyhamanalysis.txt",'w')
# #f.write(pyham_analysis)
#
# # Get the ancestral genome by name
# rodents_genome = ham_analysis.get_ancestral_genome_by_name("Rodents")
#
# # Get the related ancestral genes (HOGs)
# rodents_ancestral_genes = rodents_genome.genes
#
# # Get the number of ancestral genes at level of Rodents
# print(len(rodents_ancestral_genes))