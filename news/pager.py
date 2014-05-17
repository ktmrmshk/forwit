from django.core.paginator import Paginator

class Pager(object):
    def __init__(self):
        self.pagelist = []
        self.previous = False
        self.next = False
    def add(self, page):
        self.pagelist.append(page)
    def setPrevious(self, flag=True):
        self.previous=flag
    def setNext(self, flag=True):
        self.next = flag
    

def getPager(itemlist, currentpage, path, numperpage=20, username=None):
    p = Paginator(itemlist, numperpage)
    pager={}
    pager['current'] = currentpage
    pager['max'] = p.num_pages
    tmppath=path
    if username != None:#usr=u
        tmppath += '%s/' % username
    
    if currentpage != 1:
        pager['first'] = {'num': '1' , 'url': '%s?page=%d' % (tmppath, 1) }
    if currentpage != p.num_pages: # not lastpage
        pager['last'] = { 'num': p.num_pages, 'url':'%s?page=%d' % (tmppath, p.num_pages) }
    if p.page(currentpage).has_previous():
        pager['prev'] = { 'url': '%s?page=%d' % (tmppath, currentpage - 1) }
    if p.page(currentpage).has_next():
        pager['next'] = { 'url': '%s?page=%d' % (tmppath, currentpage + 1) }
    items = p.page(currentpage).object_list
    return (items, pager)
    
    
    