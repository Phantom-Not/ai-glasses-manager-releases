"""Dry-run or submit this project's sitemap URLs to IndexNow."""
from pathlib import Path
from urllib.parse import urlsplit
import argparse,json,urllib.request,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--submit',action='store_true',help='Verify the live key and send the URLs')
    args=parser.parse_args()
    site=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
    config=json.loads((ROOT/'content/indexnow.json').read_text(encoding='utf-8'))
    base=site['base_url'].rstrip('/')+'/'
    urls=[row.text for row in ET.parse(ROOT/'docs/sitemap.xml').findall('{*}url/{*}loc')]
    if not urls or not all(address.startswith(base) for address in urls):
        raise ValueError('Only this project site can be submitted')
    if urlsplit(base).hostname!=config['host']:
        raise ValueError('The configured host must match the project site')
    if config['keyLocation']!=base+config['key']+'.txt':
        raise ValueError('The verification key must stay inside the project site')
    payload=dict(config,urlList=urls)
    print(('SUBMIT' if args.submit else 'DRY RUN')+': '+str(len(urls))+' URLs under '+base)
    if not args.submit:
        print('Use --submit after the site and public key are deployed.');return
    request=urllib.request.Request(config['keyLocation'],headers={'User-Agent':'AI-Glasses-Manager-Site'})
    with urllib.request.urlopen(request,timeout=30) as response:
        if response.read().decode().strip()!=config['key']:
            raise ValueError('Live verification key does not match')
    request=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8','User-Agent':'AI-Glasses-Manager-Site'},method='POST')
    with urllib.request.urlopen(request,timeout=30) as response:
        print('IndexNow HTTP '+str(response.status)+'. Notification accepted; indexing and ranking are not guaranteed.')
if __name__=='__main__':main()
