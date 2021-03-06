import feedparser as fp
import urllib
import re

CINII_URL = 'http://ci.nii.ac.jp/opensearch/search?'
LINK_PREFIX = 'http://ci.nii.ac.jp/naid/'
APPID = '5nIg0LMJGgsg4MpFzgaF'

class Publist(object):
    def __init__(self):
        self.url = ''
        self.res = u''
        self.dat = None
        self.author =''
        self.q=''
        self.cnt_ret=0
    def setparam(self, q='', author='', fmt='atom', count=200, start=0):
        if author != '':
            self.author = author
        if q != '':
            self.q = q
        self.fmt = fmt
        self.count = count
        self.start = start
        self.query = {}
        if self.q != '':
            self.query['q'] = self.q.encode('utf-8')
        if self.author != '':
            self.query['author'] = self.author.encode('utf-8')
        self.query['format'] = self.fmt
        self.query['count'] = self.count
        self.query['start'] = self.start
        self.query['appid'] = APPID
        
        #DEBUG
        print urllib.urlencode(self.query)
        self.url = CINII_URL + urllib.urlencode(self.query)
    def get(self):
        self.dat = fp.parse(self.url)
        self.cnt_ret = int(self.dat['feed']['opensearch_totalresults'])
    def loadfile(self, filename):
        self.filename = filename
        self.dat = fp.parse(filename)
        self.cnt_ret = int(self.dat['feed']['opensearch_totalresults'])
    def print_authors(self, authors):
        for a in authors:
            self.res += a.name + u', '
        else:
            self.res += u'\n'
    def print_entry(self, entry):
        self.res += entry.title + u'\n'
        self.print_authors(entry.authors)
        self.res += entry.get('publisher', '') + u' '
        self.res += entry.get('prism_publicationname', '') + u' '
        self.res += u'Vol.' + entry.get('prism_volume', '') + u', '
        self.res += u'Num.' + entry.get('prism_number', '') + u', '
        self.res += u'P.' + entry.get('prism_pagerange', '') + u', '
        self.res += entry.get('prism_publicationdate', '') + u'\n\n'
        print self.res
    def parse_dat(self, entry):
        ret = {}
        m = re.search(r'http://.+/([0-9]+)', entry.id)
        ret['id'] = str( m.group(1) )
        #print '>> %s type=%s' % (ret['id'], type(ret['id']) )
        #ret['id'] = entry.id
        ret['link'] = entry.id
        ret['title'] = entry.get('title', 'No Title')
        ret['authors'] = entry.get('authors', 'N/A')
        ret['publisher'] = entry.get('publisher', 'N/A')
        ret['prism_publicationname'] = entry.get('prism_publicationname', 'N/A')
        ret['prism_volume'] = entry.get('prism_volume', 'N/A')
        ret['prism_number'] = entry.get('prism_number', 'N/A')
        ret['prism_pagerange'] = entry.get('prism_pagerange', 'N/A')
        ret['prism_publicationdate'] = entry.get('prism_publicationdate', 'N/A')
        ret['prism_issn'] = entry.get('prism_issn', 'N/A')
        
        return ret
    def parse_dat_all(self):
        ret = []
        for e in self.dat.entries:
            ret.append(self.parse_dat(e))
        self.res=ret
        return ret
    
    def print_all(self):
        for e in self.dat.entries:
            self.print_entry(e)
    def show(self):
        print self.res#.encode('utf-8')
    
    def get_rdf(self):
        pass



if __name__ == '__main__':
    def sample_main_from_web():
        pub = Publist()
        pub.setparam(u'kitamura masahiko')
        pub.get()
        print pub.url
        # pub.loadfile('kekka.atom')
        pub.print_all()
        pub.show()
        
    def main_from_file(filename):
        pub = Publist()
        pub.loadfile(filename)
        pub.parse_dat_all()
        #pub.show()
        print pub.res[0]['id']
        return pub
    
    #pub = main_from_file('appid.atom')    
    sample_main_from_web()
# d = fp.parse('kekka.atom')

# cnt=0
# for e in d.entries:
    # print cnt, e.title, 
    
    # cnt+=1


