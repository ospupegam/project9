# http://rest.kegg.jp/info/ath #displays the number of gene entries for the KEGG organism
import requests

r1 = requests.get('https://api.kegg.net/conv/ncbi-geneid/ath:AT5G66210')
print(r1.text)

#/idmap/genes/ncbi-geneid/00000001