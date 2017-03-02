import operator
import os

def endsorStartsWith(string):
    endings = ['xlsx', 'doc', 'DOC', 'XLSX', 'XLS','DOCX', 'docx', 'DOC.txt', 'pdf','layout.txt']
    beginnings = ['read', 'READ']
    res = map(lambda x: string.endswith(x), endings)
    r1 = map(lambda x: string.startswith(x), beginnings)
    if True in res:
        return True
    else:
        return False

def combineDateState(fstring):
    n = fstring['this_dir'].split('/')[-2:]
    states = ['DC', 'CT', 'DE', 'FL', 'GA' 'MI', 'NC', 'UT', 'RI', 'OK', 'CO', 'WA']
    if n[1] in states:
        return n[1] + '/'
    else:
        return '/'.join(n) + '_'

def createNeeded(fstring):
    pth = '/'.join(['..','docs','voter_files']) 
    state = fstring.split('/')[1]
    if os.path.exists(pth + '/' + state):
        pass
    else:
        os.mkdir(pth + '/' + state)
 

docs_p = '/'.join(['..','docs','voter_files']) + '/'
create_dest_files = lambda x: map(lambda y: docs_p + combineDateState(x) + y.replace(' ', '_'), x['docs'])
create_orig = lambda x: map(lambda y: x['this_dir'] + '/' + y, x['docs'])
has_docs = lambda x: x['docs'] != []
doc = lambda x: endsorStartsWith(x) == True

if __name__ == '__main__':
    f=list(os.walk('.'))
    l = filter(has_docs, map(lambda x: 
        {'docs': filter(doc, x[-1]), 
            'this_dir':x[0], 'dirs_here':x[1]}, f))
    dst = reduce(operator.add, map(create_dest_files, l))
    orig = reduce(operator.add, map(create_orig, l))
    s = map(createNeeded, orig)
    s = map(lambda x: os.rename(x[0], x[1]), zip(orig, dst)) 

