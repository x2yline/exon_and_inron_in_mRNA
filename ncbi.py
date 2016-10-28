import urllib
from lxml import etree
import os

number = raw_input('Please choose the genID for your target gene:\n')
gene_url='https://www.ncbi.nlm.nih.gov'+'/gene/'+number
print 'loading......'
html = etree.HTML(urllib.urlopen(gene_url).read())


protein_url = 'https://www.ncbi.nlm.nih.gov/protein?LinkName=gene_protein_refseq&from_uid=' + number
RNA_url = 'https://www.ncbi.nlm.nih.gov/nuccore?LinkName=gene_nuccore_refseqrna&from_uid='+ number
DNA_url = 'https://www.ncbi.nlm.nih.gov'+html.xpath('//*[@class="divAccession"]/div/p/a[2]/@href')[0]
imgscr = html.xpath('//*[@id="padded_content"]/div[6]/div[2]/div[2]/div[2]/p/img/@src')[0]
GID = imgscr.split('nuc_gi=')[1].split('&')[0]
DNA_url = DNA_url.split('from=')[-1].split('to=')
DNA_fasta_url = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+GID+'&db=nuccore&report=fasta&from='+DNA_url[0]+'&to='+DNA_url[1]



# print DNA_fasta_url





#print html.read()
#print type(html.read())
#print html.readline()
#print html.info()
#print html.getcode()
#print html.readlines()
#print html.fileno()https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=1036030432&db=nuccore&report=fasta


def seqtype(url):
    global url_header
    url_header = url.split("?")[0]
    #variable = object
    return url_header.split("/")[-1]
    
def GIs(html):
    GIs = html.xpath('//*[@id="maincontent"]/div/div[5]/div/div[2]/div[2]/div/dl/dd[2]/text() ')
    return GIs

def fasta_url(GI):
    t = []
    global object
    if object == 'protein':
        for j in GI:
            t.append( 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+ j +'&db=protein&report=fasta')
    else:
        for j in GI:
            t.append( 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+ j +'&db=nuccore&report=fasta')
            
    #varible = fasta_url
    return t

def genbank_url(fasta_urls):
    t = []
    global object
    if object == 'protein':
        j = 'genpept'
    else:
        j = 'genbank'
    for i in fasta_urls:
        
        t.append(i[:-5] + j)
    #variable = genbank_url
    return t
    





def get_fasta_sq(fasta_urls):
    global object
    new = os.path.join(os.getcwd(),GID+" "+object)
    try:
        os.makedirs(new)
    except:
         print "can't create a new directory"

    for i in fasta_urls:
        t = etree.HTML(urllib.urlopen(i).read())
        # //*[@id="gi_1036030432"]/div/div[2]/p[3]/span[1]
        # //*[@id="gi_1036030432"]/div/div[2]/p[1]/a
        title1 = t.xpath('//*[@id="content"]/div/div[1]/div/div[2]/p[3]/span[1]/text()')[0].split('G')[0]
        title2 = t.xpath('//*[@id="content"]/div/div[1]/div/div[2]/p[1]/a/text()')[0].split('(')[-1]
        title = title2 + ' ' + title1 + 'fasta.txt'
        t = t.xpath('//*[@id="content"]/div/div[2]/text()')[0]
        t.strip('"')
        t.strip()
        title = os.path.join(new,title)
        f = open(title,'w')
        f.write(t)
        f.close()
        print 'Have dowloaded the ' + object + ': ' title


def get_non_DNA_seq(url):
    global object
    html = etree.HTML(urllib.urlopen(url).read())
    object = seqtype(url)
    GI = GIs(html)
    fasta_urls = fasta_url(GI)
    genbank_urls = genbank_url(fasta_urls)
    get_fasta_sq(fasta_urls)



get_non_DNA_seq(RNA_url)
get_non_DNA_seq(protein_url)
object = 'DNA'
get_fasta_sq(DNA_fasta_url)

#print fasta_url
#f = open('html.txt','r')
#f.write(html.read())
#f.close()
#f=open('fasta.txt','r')
#fasta=urllib.urlopen(fasta_url[0]).read()
#f.write(fasta)
#f.close()
#print 'done'
#print fasta'''
