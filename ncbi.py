import urllib
from lxml import etree
import os

def seqtype(url):
    global url_header
    url_header = url.split("?")[0]
    #variable = object
    return url_header.split("/")[-1]
    
def GIs(html):
    #html is 
    GI = html.xpath('//*[@id="maincontent"]/div/div[5]/div/div[2]/div[2]/div/dl/dd[2]/text() ')
    return GI

def fasta_url(GI):
    # GI is not geneID in the ncbi
    t = []
    global object
    if object == 'protein' and type(GI) == type([]):
        for j in GI:
            t.append( 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+ j +'&db=protein&report=fasta')
    elif object != 'protein' and type(GI) == type([]):
        for j in GI:
            t.append( 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+ j +'&db=nuccore&report=fasta')
    else:
        t.append( 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+ GI +'&db=nuccore&report=fasta')

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
    #fasta_urls is the urls modified by function fasta_url
    global object,GID,gene_name

    new = os.path.join(os.getcwd(),gene_name +" "+object)
    try:
        os.makedirs(new)
        # print 'have create the new directory ' + str(new)
    except:
        print "can't create a new directory"
    if type(fasta_urls) == type([]):
        for i in fasta_urls:
            t = etree.HTML(urllib.urlopen(i).read())
            # print 'have got the fasta page'
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
            # print 'Have dowloaded the ' + object + ': ' + title
    else:
        t = etree.HTML(urllib.urlopen(fasta_urls).read())
        # print 'have got the fasta page'
        # //*[@id="gi_1036030432"]/div/div[2]/p[3]/span[1]
        # //*[@id="gi_1036030432"]/div/div[2]/p[1]/a
        title1 = t.xpath('//*[@class="aux"]/span[1]/text()')[0].split('G')[0]
        title2 = t.xpath('//*[@class="title"]/a/text()')[0].split('(')[-1]
        t = t.xpath('//*[@id="content"]/div/div[2]/text()')[0]
        title = title2 + ' ' + title1 + 'fasta.txt'
        t.strip('"')
        t.strip()
        title = os.path.join(new,title)
        f = open(title,'w')
        f.write(t)
        f.close()
        # print 'Have dowloaded the ' + object + ': ' + title 


def get_non_DNA_seq(url):

    global object
    html = etree.HTML(urllib.urlopen(url).read())
    object = seqtype(url)
    GI = GIs(html)
    fasta_urls = fasta_url(GI)

    get_fasta_sq(fasta_urls)


def get_DNA_seq(fasta_urls):
    #fasta_urls is DNA_fasta_url like: https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=1036030432&db=nuccore&report=fasta&from=0&to=20
    global object, gene_name
    global GID
    new = os.path.join(os.getcwd(), gene_name +" "+object)
    try:
        os.makedirs(new)
        # print 'have create the new directory ' + str(new)
    except:
         print "can't create a new directory"

    t = etree.HTML(urllib.urlopen(fasta_urls).read())
    # print 'have got the fasta page'
        # //*[@id="gi_1036030432"]/div/div[2]/p[3]/span[1]
        # //*[@id="gi_1036030432"]/div/div[2]/p[1]/a
    title1 = t.xpath('//*[@class="aux"]/span[1]/text()')[0].split('G')[0]
    title2 = t.xpath('//*[@class="title"]/a/text()')[0].split('(')[-1]
    t = t.xpath('//*[@id="content"]/div/div[2]/text()')[0]
    title = title2 + ' ' + title1 + 'fasta.txt'
    t.strip('"')
    t.strip()
    title = os.path.join(new,title)
    f = open(title,'w')
    f.write(t)
    f.close()
    # print 'Have dowloaded the ' + 'DNA' + ': ' + title 








def main(number):
    global object, GID, gene_name
    try:
        # print 'Checking your internet...\n'
        # urllib.urlopen('https://www.baidu.com/')
        # print 'your Internet Works Well\n'
        
        if number[0] == '0' or number[0] == '1' or number[0] == '2' or number[0] == '3' or number[0] == '4' or number[0] == '5' or number[0] == '6' or number[0] == '7' or number[0] == '8' or number[0] == '9':
            gene_url='https://www.ncbi.nlm.nih.gov'+'/gene/'+number
            print '\nloading......\n'
            html = etree.HTML(urllib.urlopen(gene_url).read())
            gene_name = html.xpath('//*[@id="summaryDl"]/dd[1]/text()')[0]
            protein_url = 'https://www.ncbi.nlm.nih.gov/protein?LinkName=gene_protein_refseq&from_uid=' + number
            RNA_url = 'https://www.ncbi.nlm.nih.gov/nuccore?LinkName=gene_nuccore_refseqrna&from_uid='+ number
            DNA_url = 'https://www.ncbi.nlm.nih.gov'+html.xpath('//*[@class="divAccession"]/div/p/a[2]/@href')[0]
            imgscr = html.xpath('//*[@id="padded_content"]/div[6]/div[2]/div[2]/div[2]/p/img/@src')[0]
            GID = imgscr.split('nuc_gi=')[1].split('&')[0]
            DNA_url = DNA_url.split('from=')[-1].split('to=')
            DNA_fasta_url = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id='+GID+'&db=nuccore&report=fasta&from='+DNA_url[0]+'to='+DNA_url[1]
            
            get_non_DNA_seq(RNA_url)
            print 'have done all things with RNA\n'
            get_non_DNA_seq(protein_url)
            print 'have done all things with Protein\n'
            object = 'DNA'
            # print 'Begin with DNA...' +  DNA_fasta_url
            get_DNA_seq(DNA_fasta_url)
            print 'have done all things with DNA\n'

        else:
            object = number
            url = "https://www.ncbi.nlm.nih.gov/nuccore/" + number
            print '\nloading......\n'
            html = etree.HTML(urllib.urlopen(url).read())
            # gene_name = html.xpath('//*[@id="EntrezForm"]/div[1]/div[6]/div/div[8]/div[1]/div/h3/text()')[0]
            gene_name = ' '
            # print 'page got'
            GID = html.xpath('//*[@class="dblinks"]/@href')[0].split('/')[-1].split('?')[0]
            print 'the current dowloading GI is ' + GID
            fasta_urls = fasta_url(GID)[0]
            # print fasta_urls
            get_fasta_sq(fasta_urls)
            
    except Exception as e:
        print e

input = os.path.join(os.getcwd(),'input.txt')
f=open(input,'r')
numbers = f.readlines()
f.close()
try:
    print 'Checking your internet...'
    urllib.urlopen('https://www.baidu.com/')
    print 'your Internet Works Well\n'
    for i in numbers:
        i.strip()
        i = i.split()
        for j in i:
            j = j.split('\n')
            for p in j:
                if p:
                    main(p)

    raw_input('Done all things plese press ENTER to quit :)')

except Exception as e:
    print e
    raw_input("It don't work plese press ENTER to quit :(")
