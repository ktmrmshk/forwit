# -*- coding: utf-8 -*-

import rdflib, sys
FOAF=rdflib.Namespace("http://xmlns.com/foaf/0.1/")
DC=rdflib.Namespace("http://purl.org/dc/elements/1.1/")
PRISM=rdflib.Namespace("http://prismstandard.org/namespaces/basic/2.0/")
CON=rdflib.Namespace("http://www.w3.org/2000/10/swap/pim/contact#")


class CiniiRDF(object):
    def __init__(self, url):
        self.url=url
        self.g = rdflib.Graph()
        self.g.load(self.url)
        
        self.title=''
        self.abst=''

        for s,p,o in self.g.triples((None, FOAF['isPrimaryTopicOf'], None)):
            assert(self.title=='')
            self.title = s

        try:      
            self.abst=''
            for s,p,o in self.g.triples((self.title, DC.description, None)):
                assert(self.abst=='')
                self.abst = '%s' % o
        except:
            print sys.exc_info()[0]
    
        self.person=[]
        for s,p,o in self.g.triples((None, None, FOAF.Person)):
            self.person.append(s)

        self.author=[]
        for psn in self.person:
            tmp={}
            for s,p,o in self.g.triples((psn, FOAF.name, None)):
                tmp['name'] =  '%s' % o 
            for s,p,o in self.g.triples((psn, CON.organization, None)):
                tmp_org = o
                tmp['org']=[]
                for s,p,o in self.g.triples((tmp_org, FOAF.name, None)):
                    tmp['org'].append( '%s' % o )
                #for s,p,o in g.triples((tmp_org, FOAF.name, None)):
            self.author.append(tmp)
        
    def getAffiliation(self, name):
        org_str=''
        for s,p,o in self.g.triples((None, FOAF.name, rdflib.term.Literal(name) )):
            me = s
            print s
            for s,p,o in self.g.triples((me, CON.organization, None )):
                org = o
                for s,p,o in self.g.triples((org, FOAF.name, None )):
                    org_str = '%s' % o
        return org_str
        


if __name__ == '__main__':
    c = CiniiRDF('2.rdf')
    if c.abst!='':
        print c.abst
        
    for a in c.author:
        print a['name'],
        if 'org' in a:
            print a['org'][0]
        print
    
    print c.getAffiliation( u'園生遥 ' )
    