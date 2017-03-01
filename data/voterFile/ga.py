import os
import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup

def createRequests(year):
    url = 'http://elections.sos.ga.gov/Elections/downLoadVPHFile.do'
    if year >= 2013:
        d = {'nbElecYear':year, 'cdElecCat':None, 
                'idElection':0, 'cdFileType': 'VPH', 
                'flFullFile':'Y', 'cdStaticFile':None}
    else: 
        d = {'idElection':year, 'cdFileType': 'VPH', 'cdStaticFile':None}
    return {'requestData': d, 'url': url, 'year': str(year)}

def makeRequestWriteResult(req):
    print 'downloading %s from %s' % (req['year'], req['url'])
    r = requests.post(req['url'], data=req['requestData'])
    print 'writing %s from %s' % (req['year'], req['url'])
    if not os.path.exists(req['year']):
        os.mkdir(req['year'])
    with open(req['year'] + '/' + 'GA' + '_' + req['year'] + '.txt', 'w') as f:
        f.write(r.content)

def makeRequestsWriteResultsParallel(reqs, threads=10, test=False):
    if test:
        reqs = reqs[:3] + reqs[-3:]
    p = Pool(10)
    res = p.map(makeRequestWriteResult, reqs)
    p.close()
    p.join()

if __name__ == '__main__':
    reqs = map(lambda x: createRequests(x), range(1996, 2018))
    makeRequestsWriteResultsParallel(reqs,25)
    
