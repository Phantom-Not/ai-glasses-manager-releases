"""Validate the generated product site without a browser or third-party packages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET,re,sys,subprocess,uuid,shutil

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
DATA=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
BASE=DATA['base_url'].rstrip('/');PREFIX=urlsplit(BASE).path
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True);self.lang=None;self.h1=0;self.ids=set();self.links=[];self.images=[];self.meta={};self.alternates={};self.canonical=[];self.feed_links=[];self.title='';self.in_title=False;self.json_scripts=[];self.in_json=False;self.script='';self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if a.get('id'):
            assert a['id'] not in self.ids,('duplicate id',a['id']);self.ids.add(a['id'])
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='img':self.images.append(a)
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link':
            if a.get('type')=='application/atom+xml':self.feed_links.append(a.get('href'))
            if a.get('rel')=='canonical':self.canonical.append(a.get('href'))
            if a.get('rel')=='alternate' and a.get('hreflang'):self.alternates[a['hreflang']]=a.get('href')
            if a.get('href'):self.links.append(a['href'])
        if tag=='title':self.in_title=True
        if tag=='script':
            assert a.get('type')=='application/ld+json','Unexpected executable script'
            self.in_json=True;self.script=''
        assert tag!='form','No checkout, login or tracking forms are expected'
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_json:self.json_scripts.append(json.loads(self.script));self.in_json=False
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_json:self.script+=data

def local_target(link,current):
    parsed=urlsplit(link)
    if parsed.scheme or parsed.netloc:
        if link.startswith(BASE+'/') or link==BASE:raw=parsed.path
        else:
            assert parsed.scheme=='https',('Non-HTTPS external URL',link)
            return None,None
    else:raw=parsed.path
    if not raw:target=current
    elif raw.startswith('/'):
        assert raw==PREFIX or raw.startswith(PREFIX+'/'),('Link escaped project site',link)
        target=DOCS/raw[len(PREFIX):].lstrip('/')
    else:target=current.parent/raw
    target=target.resolve()
    assert target==DOCS.resolve() or DOCS.resolve() in target.parents,('Path escaped docs',link)
    if target.is_dir() or not target.suffix:target=target/'index.html'
    return target,unquote(parsed.fragment)

def check():
    generated=(ROOT/('.site-check-'+uuid.uuid4().hex)).resolve()
    if generated.parent!=ROOT.resolve() or not generated.name.startswith('.site-check-'):
        raise ValueError('Temporary output must stay inside this repository')
    generated.mkdir()
    try:
        subprocess.run([sys.executable,str(ROOT/'tools/build_site.py'),'--output',str(generated)],check=True,capture_output=True)
        for output in generated.rglob('*'):
            if output.is_file():
                actual=DOCS/output.relative_to(generated)
                assert actual.is_file() and actual.read_bytes()==output.read_bytes(),('Generated output is stale; run tools/build_site.py',actual)
    finally:
        if generated.resolve().parent!=ROOT.resolve() or not generated.name.startswith('.site-check-'):
            raise ValueError('Refusing cleanup outside the temporary output directory')
        shutil.rmtree(generated)
    pages={p.resolve():Page(p.read_text(encoding='utf-8')) for p in DOCS.rglob('*.html') if p.name!='404.html'}
    expected=(len(DATA['pages'])+len(DATA['releases']))*len(DATA['locales'])
    assert len(pages)==expected,(len(pages),expected)
    titles=set();descriptions=set();addresses=set()
    for file,page in pages.items():
        text=file.read_text(encoding='utf-8')
        assert '\u2013' not in text and '\u2014' not in text,('Long dash',file)
        assert page.h1==1 and 'main' in page.ids,('Landmark/title',file)
        language_keys={item['lang']:key for key,item in DATA['locales'].items()}
        assert page.lang in language_keys,file
        key=language_keys[page.lang]
        locale=key+'/' if key!='en' else ''
        expected_feed=BASE+'/'+locale+'updates/feed.xml'
        assert page.feed_links==[expected_feed] and expected_feed in page.links,('Wrong localized feed',file)
        if file.parent.name=='help':assert 'adb install -r AI-Glasses-Manager-'+DATA['current_version']+'.apk' in text,('Outdated install command',file)
        assert page.title and page.title not in titles,('Missing/duplicate title',file);titles.add(page.title)
        description=page.meta.get('description','');assert description and description not in descriptions,('Missing/duplicate description',file);descriptions.add(description)
        assert len(page.canonical)==1 and page.canonical[0].startswith(BASE+'/'),file
        addresses.add(page.canonical[0]);assert set(page.alternates)==set(language_keys)|{'x-default'},file
        assert page.meta.get('og:url')==page.canonical[0] and page.meta.get('og:title')==page.title,file
        assert page.meta.get('robots','').startswith('index,follow'),file
        for alternate in page.alternates.values():
            target,_=local_target(alternate,file);assert target in pages,('Missing language alternate',file,alternate)
            assert pages[target].alternates==page.alternates,('Nonreciprocal language alternate',file,alternate)
        for link in page.links:
            target,fragment=local_target(link,file)
            if target is None:continue
            assert target.is_file(),('Broken link',file,link,target)
            if fragment:assert target in pages and fragment in pages[target].ids,('Broken fragment',file,link)
        for img in page.images:
            assert 'alt' in img and 'width' in img and 'height' in img,('Image dimensions/alt',file,img)
            target,_=local_target(img.get('src',''),file);assert target and target.is_file(),('Missing image',file,img)
            for candidate in img.get('srcset','').split(','):
                if not candidate.strip():continue
                source,descriptor=candidate.strip().split()
                assert re.fullmatch(r'[1-9][0-9]*w',descriptor),('Invalid responsive image width',file,candidate)
                target,_=local_target(source,file);assert target and target.is_file(),('Missing responsive image',file,source)
        assert len(page.json_scripts)==1,file
        graph=page.json_scripts[0]['@graph'];assert graph[0]['url']==page.canonical[0],file
        for item in graph:
            assert 'aggregateRating' not in item and 'review' not in item,'No fabricated ratings'
            if item.get('@type')=='MobileApplication':
                assert item['softwareVersion']==DATA['current_version']
                assert any(price in text for price in ['$1.99','1.99 美元','1.99 米ドル']),'Offer must match visible pricing'
        assert not re.search(r'\b(VHS|Temporal Lights|Arabic)\b',text,re.I),('Unreleased specific feature',file)
    sitemap=ET.parse(DOCS/'sitemap.xml').getroot();listed={row.text for row in sitemap.findall('{*}url/{*}loc')}
    assert listed==addresses,('Sitemap mismatch',listed^addresses)
    dates={row.find('{*}loc').text:row.find('{*}lastmod').text for row in sitemap}
    for release in DATA['releases']:
        for locale in ['' if key=='en' else key+'/' for key in DATA['locales']]:
            assert dates[BASE+'/'+locale+'updates/'+release['version']+'/']==release.get('updated',release['published'])
    for locale in ['' if key=='en' else key+'/' for key in DATA['locales']]:
        feed=ET.parse(DOCS/locale/'updates/feed.xml').getroot();entries=feed.findall('{*}entry');assert len(entries)==len(DATA['releases'])
        assert feed.find('{*}updated').text==max(r.get('updated',r['published']) for r in DATA['releases'])
        for entry,release in zip(entries,DATA['releases']):
            assert entry.find('{*}published').text==release['published']
            assert entry.find('{*}updated').text==release.get('updated',release['published']),('Release timestamp drift',release['version'])
    assert {s['id'] for s in DATA['pages']['features']['en']['sections']}=={'store','camera','gallery','files','settings','sound','tools','ai','shortcuts','interface'}
    for slug,translations in DATA['pages'].items():
        assert set(translations)==set(DATA['locales']),slug
        for locale in DATA['locales']:
            for text in [translations[locale]['title'],translations[locale]['description'],translations[locale].get('h1','')]:assert '\u2013' not in text and '\u2014' not in text
        for locale in DATA['locales']:
            assert set(translations[locale])==set(translations['en']),('Missing localized fields',slug,locale)
            if 'sections' in translations['en']:assert [s['id'] for s in translations['en']['sections']]==[s['id'] for s in translations[locale]['sections']],(slug,locale)
            if 'faq' in translations['en']:assert len(translations[locale]['faq'])==len(translations['en']['faq']),(slug,locale)
    for locale,settings in DATA['locales'].items():
        assert set(settings['ui'])==set(DATA['locales']['en']['ui']),('Missing localized UI',locale)
    manifest=json.loads((ROOT/'manager-update.json').read_text(encoding='utf-8-sig'));assert manifest['versionName']==DATA['current_version'],'Update the website content when publishing a new public release'
    assert DATA['releases'][0]['version']==DATA['current_version']
    key=json.loads((ROOT/'content/indexnow.json').read_text());assert (DOCS/(key['key']+'.txt')).read_text()==key['key']
    assert not any((DOCS/name).exists() for name in ['.env','manager-update.json','AGENTS.md'])
    readme=(ROOT/'README.md').read_text(encoding='utf-8');assert '\u2013' not in readme and '\u2014' not in readme
    for match in re.findall(r'(?:src=")[^"]+(?:")',readme):
        rel=match[5:-1]
        if not rel.startswith('https:'):assert (ROOT/rel).is_file(),('README image missing',rel)
    print('PASS',len(pages),'pages: links/fragments, language parity, metadata/schema, sitemap/feeds, feature coverage, released version and no long dashes.')
if __name__=='__main__':check()
