import os
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool




def findLinks(url):
    s = BeautifulSoup(requests.get(url).content)
    t = s.findAll('td')
    check, fix = None, None
    if url.find('dela') > -1:
        fixed_date = '2012_04_26' 
    elif url.find('conn') > -1:
        fixed_date = '2013_06_01'        
    elif url.find('flvoters') > -1:
        fixed_date = '2012_05_31'
        check = lambda x: x['source'].find('Voter_File_Request_for_Info') == -1
    elif url.find('michi') > -1:
        fixed_date = None
    elif url.find('okla') > -1:
        fixed_date = None
        check = lambda x: x['source'].find('downloads/201') > -1
    elif url.find('colora') > -1:
        fixed_date = '2013_05_01'
    h = map(lambda x: {'dir_name': ''.join(filter(lambda x: x.startswith('2'), x.split('/'))), 'source':x},
                map(lambda x: x['href'], s.findAll('a')))
    fixed = map(lambda x: {'dir_name': fixed_date, 'source':x['source']}, filter(lambda x: x['dir_name'] == '', h))
    g = map(lambda x: {'dir_name': x['dir_name'][:4] + '_' + x['dir_name'][4:6] + '_' + x['dir_name'][6:],
        'source':x['source']},
        filter(lambda x: x['dir_name'] != '', h)) 
    links_and_destinations = g + fixed
    if check:
        links_and_destinations = filter(check, links_and_destinations)
    if fix:
        links_and_destinations = map(fix, links_and_destinations)
    return links_and_destinations

def downloadAndWriteOne(item):
    try:
        fname = item['source'].split('/')[-1]
        try:
            print 'attempting to download %s' % item['source']
            z = requests.get(item['source'])
        except: 
            print 'download of %s failed due to %s' % (item['source'], z.reason)
        if not os.path.exists(item['dir_name']):
            os.mkdir(item['dir_name'])
        try:
            p = item['dir_name'] + '/' + fname 
            print 'attempting to write content from %s to %s' % (item['source'], p)
            with open(p, 'w') as f:
                f.write(z.content)
        except:
            print 'failed to write content from %s to %s' % (item['source'], p)
    except:
        print 'error: attempting to download from %s and write to %s' % (item['source'], item['dir_name'])

def downloadAndWriteMany(items, cores=6):
    domain = filter(lambda x: x.endswith('com') or 
            x.endswith('info') or x.endswith('org'), 
            items[-1]['source'].split('/'))[0]
    #print domain
    print 'starting %s' % domain
    p = Pool(int(cores))
    res = p.map(downloadAndWriteOne, items)
    p.close()
    p.join()
    print 'finished %s' % domain


if __name__ == '__main__':
    import argparse
    desc = 'scrapes links & downloads corresponding items from sites like connvoters.com'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', help="Give starting page to get links to download")
    parser.add_argument('-n', help="Number of threads used to download files in parallel, defaults to 6", default=12)
    parser.add_argument('-t', help="If set to True, then the script will first test one download in serial mode, then will test a limited number of links in parallel mode")
    args = parser.parse_args()
    if not args.s:
        print 'requires a starting url'
    elif args.t:
        print 'test flag set to True'
        items = findLinks(args.s)
        print 'gathered links, displaying examples'
        print items[:2]
        print 'attempting a single serial download'
        downloadAndWriteOne(items[0])
        print 'attempting to parallel download first four and last four items'
        #it = items[:20]
        it = items[:4] + items[-4:]
        downloadAndWriteMany(it, args.n)
    else:
        items = findLinks(args.s)
        downloadAndWriteMany(items, args.n)

