import os
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool


def getLinks(url, condition, folder=False):
    s = BeautifulSoup(requests.get(url).content)
    if folder:
        q = 'prefix'
    else:
        q = 'key'
    l = filter(condition, map(lambda x: x.text, s.findAll(q)))
    return l

def downloadFile(suffix):
    base_url = 'https://s3.amazonaws.com/dl.ncsbe.gov/'
    file_source = base_url + suffix
    print 'requesting from %s' % file_source
    r = requests.get(file_source)
    print 'writing %s' % suffix
    with open(suffix.replace('/', '_'), 'w') as f:
        f.write(r.content)

def downloadMultiples(suffix_list, threads=10, test=False):
    if test:
        suffix_list = suffix_list[:2] + suffix_list[-2:]
        print 'in test mode, running serial download of %s' % suffix_list[0]
        downloadFile(suffix_list[0])
        print 'on to parallel'
    else:
        pass
    p = Pool(threads)
    res = p.map(downloadFile, suffix_list)
    p.close()
    p.join()


if __name__ == '__main__':
    import operator
    base_url = 'https://s3.amazonaws.com/dl.ncsbe.gov?delimiter=%2F&prefix='
    st = lambda x: x.endswith('Statewide.zip')
    data_main = 'https://s3.amazonaws.com/dl.ncsbe.gov?delimiter=%2F&prefix=data%2F'
    state_wide = getLinks(data_main, st)
    leg_du = 'http://dl.ncsbe.gov/index.html?prefix=data/legislative_districts/base_data/'
    lf = lambda x: x.startswith('VOTER_')
    leg_dist = getLinks(leg_du, lf)
    sn_u = 'https://s3.amazonaws.com/dl.ncsbe.gov?delimiter=%2F&prefix=data%2FSnapshots%2F'
    snaps = getLinks(sn_u, None)
    res_u = 'https://s3.amazonaws.com/dl.ncsbe.gov?delimiter=%2F&prefix=ENRS%2F'
    res_f = lambda x: x.startswith('ENRS/201')
    e_res = getLinks(res_u, res_f, True)
    e_res_f = lambda x: x.endswith('/') == False
    elecs = reduce(operator.add, map(lambda x: getLinks(base_url + x.replace('/', '%2F'), e_res_f), e_res[1:-1]))
    links = state_wide + leg_dist + snaps + elecs
    downloadMultiples(links, 20)
