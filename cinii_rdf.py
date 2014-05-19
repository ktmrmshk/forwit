import rdflib, sys
FOAF=rdflib.Namespace("http://xmlns.com/foaf/0.1/")
DC=rdflib.Namespace("http://purl.org/dc/elements/1.1/")
PRISM=rdflib.Namespace("http://prismstandard.org/namespaces/basic/2.0/")
CON=rdflib.Namespace("http://www.w3.org/2000/10/swap/pim/contact#")


class CiniiRDF(object):
    def __init__(self, url):
        self.url=url
        g = rdflib.Graph()
        g.load(self.url)
        
        self.title=''

        for s,p,o in g.triples((None, FOAF['isPrimaryTopicOf'], None)):
            assert(self.title=='')
            self.title = s

            
        try:      
            self.abst=''
            for s,p,o in g.triples((self.title, DC.description, None)):
                assert(self.abst=='')
                self.abst = '%s' % o
        except:
            print sys.exc_info()[0]         
    
        self.person=[]
        for s,p,o in g.triples((None, None, FOAF.Person)):
            self.person.append(s)
    

        self.author=[]
        for psn in self.person:
            tmp={}
            for s,p,o in g.triples((psn, FOAF.name, None)):
                tmp['name'] =  '%s' % o 
            for s,p,o in g.triples((psn, CON.organization, None)):
                tmp_org = o
                tmp['org']=[]
                for s,p,o in g.triples((tmp_org, FOAF.name, None)):
                    tmp['org'].append( '%s' % o )
                #for s,p,o in g.triples((tmp_org, FOAF.name, None)):
            self.author.append(tmp)

    

if __name__ == '__main__':
    c = CiniiRDF('http://ci.nii.ac.jp/naid/10025953523.rdf')
    if c.abst!='':
        print c.abst
        
    for a in c.author:
        print a['name'],
        if 'org' in a:
            print a['org'][0]
        print