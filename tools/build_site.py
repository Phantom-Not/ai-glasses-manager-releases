"""Build the product reference from reviewed multilingual content. No dependencies."""
from pathlib import Path
from html import escape
import argparse,json,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
DATA=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
BASE=DATA['base_url'].rstrip('/')
PREFIX='/'+'/'.join(BASE.split('/')[3:])
REPO=DATA['repository']
VERSION=DATA['current_version']
NAV=('home','app-store','camera-filters','files','features','updates','help')

def e(value): return escape(str(value),quote=True)
def path(slug='',lang='en'):
    slug, _, fragment = slug.partition('#')
    return PREFIX+('/'+lang if lang!='en' else '')+('/'+slug if slug and slug!='home' else '')+'/' + ('#'+fragment if fragment else '')
def url(slug='',lang='en'): return BASE+path(slug,lang)[len(PREFIX):]
def asset(name): return PREFIX+'/images/'+name
def write(relative,text):
    target=DOCS/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
def image(name,alt,cls=''):
    return '<figure class="'+cls+'"><a href="'+asset(name)+'"><img src="'+asset(name)+'" alt="'+e(alt)+'" width="480" height="640" loading="lazy" decoding="async"></a></figure>'
def section_html(section,index):
    body=''.join('<p>'+e(text)+'</p>' for text in section['paragraphs'])
    if section.get('bullets'): body+='<ul>'+''.join('<li>'+e(text)+'</li>' for text in section['bullets'])+'</ul>'
    visual=image(section['image'],section['alt'],'section-image') if section.get('image') else ''
    return '<section class="content-section '+('has-image' if visual else '')+'" id="'+e(section['id'])+'"><div class="section-number">'+str(index).zfill(2)+'</div><div class="section-copy"><h2>'+e(section['title'])+'</h2>'+body+'</div>'+visual+'</section>'
def filter_cards(page):
    cards=[]
    for index,row in enumerate(page['filters']):
        photo='<figure class="filter-photo"><a href="'+asset(row['image'])+'"><img src="'+asset(row['preview'])+'" srcset="'+asset(row['preview'])+' '+str(row['preview_width'])+'w, '+asset(row['image'])+' '+str(row['width'])+'w" sizes="(max-width:680px) 180px, 190px" alt="'+e(row['alt'])+'" width="'+str(row['width'])+'" height="'+str(row['height'])+'" loading="lazy" decoding="async"></a></figure>'
        cards.append('<article class="filter-card filter-'+str(index)+'"><div class="filter-heading"><span class="filter-dot" aria-hidden="true"></span><h3>'+e(row['name'])+'</h3></div>'+photo+'<p>'+e(row['description'])+'</p></article>')
    return '<div class="filter-list" id="filter-examples">'+''.join(cards)+'</div><p class="filter-examples-note">'+e(page['examples_note'])+'</p>'
def teaser(lang):
    loc=DATA['locales'][lang]
    return '<aside class="preview-note" id="next"><span class="eyebrow">'+e(loc['preview_badge'])+'</span><h2>'+e(loc['preview_title'])+'</h2><p>'+e(loc['preview'])+'</p></aside>'
def release_cards(lang,limit=None):
    rows=DATA['releases'][:limit] if limit else DATA['releases']
    return '<div class="release-list">'+''.join('<article class="release-row"><div><span class="version">'+e(row['version'])+'</span><time datetime="'+row['published']+'">'+row['published'][:10]+'</time></div><div><h2><a href="'+path('updates/'+row['version'],lang)+'">'+e(row[lang]['title'])+'</a></h2><p>'+e(row[lang]['summary'])+'</p><a class="text-link" href="'+path('updates/'+row['version'],lang)+'">'+e(DATA['locales'][lang]['read_update'])+' <span aria-hidden="true">↗</span></a></div></article>' for row in rows)+'</div>'
def layout(slug,lang,page,body,kind='page',release=None):
    loc=DATA['locales'][lang];ui=loc['ui']
    pageurl=url(slug,lang)
    feed_url=url('updates',lang)+'feed.xml'
    nav=''.join('<a href="'+path(key,lang)+'"'+(' aria-current="page"' if (key==slug or key=='updates' and slug.startswith('updates/')) else '')+'>'+e(loc['nav'][key])+'</a>' for key in NAV)
    langlinks=''.join('<a class="language-link" href="'+path(slug,key)+'" lang="'+item['lang']+'" hreflang="'+item['lang']+'"'+(' aria-current="page"' if key==lang else '')+'>'+e(item['label'])+'</a>' for key,item in DATA['locales'].items())
    globe='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 7h14M5 17h14"/></svg>'
    langmenu='<details class="language-menu"><summary aria-label="'+e(ui['choose_language'])+'">'+globe+'<span>'+e(loc['short_label'])+'</span></summary><nav aria-label="'+e(ui['choose_language'])+'">'+langlinks+'</nav></details>'
    alternates=''.join('<link rel="alternate" hreflang="'+item['lang']+'" href="'+url(slug,key)+'">' for key,item in DATA['locales'].items())+'<link rel="alternate" hreflang="x-default" href="'+url(slug,'en')+'">'
    graph=[{'@type':'WebPage','@id':pageurl+'#page','url':pageurl,'name':page['title'],'description':page['description'],'inLanguage':loc['lang'],'isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#app'}}]
    if slug=='home':
        graph += [{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'AI Glasses Manager','alternateName':'Rokid Manager','inLanguage':[item['lang'] for item in DATA['locales'].values()]},
        {'@type':'MobileApplication','@id':BASE+'/#app','name':'AI Glasses Manager','alternateName':'Rokid Manager','url':BASE+'/','icon':BASE+'/assets/manager-icon.png','softwareVersion':VERSION,'operatingSystem':'Android 8.0 or later on Rokid Glasses','applicationCategory':'UtilitiesApplication','author':{'@type':'Person','name':'Bruce','url':'https://github.com/Phantom-Not'},'downloadUrl':REPO+'/releases/latest','releaseNotes':BASE+'/updates/'+VERSION+'/','screenshot':[BASE+'/images/home.png',BASE+'/images/app-store.png',BASE+'/images/camera-photo.png'],'featureList':['Android App Store','Matrix, Cyber Glitch and Prism camera filters','Gallery','File Explorer','Wi-Fi Drop','Device and volume controls','Live IMU','Manager Shortcuts'],'offers':{'@type':'Offer','price':'1.99','priceCurrency':'USD','description':'One-time activation for one device after a three-day free trial','url':BASE+'/help/'}}]
    else:
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'AI Glasses Manager','item':url('home',lang)},{'@type':'ListItem','position':2,'name':page['h1'],'item':pageurl}]})
    if release:
        graph.append({'@type':'TechArticle','headline':page['h1'],'datePublished':release['published'],'dateModified':release.get('updated',release['published']),'author':{'@type':'Person','name':'Bruce'},'mainEntityOfPage':pageurl,'inLanguage':loc['lang']})
    jsonld=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<',r'\u003c')
    year=DATA['updated'][:4]
    return '<!doctype html>\n<html lang="'+loc['lang']+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(page['title'])+'</title><meta name="description" content="'+e(page['description'])+'"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="'+pageurl+'">'+alternates+'<link rel="alternate" type="application/atom+xml" title="'+e('AI Glasses Manager '+ui['feed_title'])+'" href="'+feed_url+'"><meta property="og:type" content="'+('article' if release else 'website')+'"><meta property="og:site_name" content="AI Glasses Manager"><meta property="og:title" content="'+e(page['title'])+'"><meta property="og:description" content="'+e(page['description'])+'"><meta property="og:url" content="'+pageurl+'"><meta property="og:image" content="'+BASE+'/images/home.png"><meta property="og:image:alt" content="'+e(ui['social_alt'])+'"><meta property="og:locale" content="'+loc['og_locale']+'"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="'+e(page['title'])+'"><meta name="twitter:description" content="'+e(page['description'])+'"><meta name="twitter:image" content="'+BASE+'/images/home.png"><meta name="theme-color" content="#f7f8f5"><link rel="icon" href="'+PREFIX+'/assets/manager-icon.png" type="image/png"><link rel="apple-touch-icon" href="'+PREFIX+'/assets/manager-icon.png"><link rel="stylesheet" href="'+PREFIX+'/assets/site.css"><script type="application/ld+json">'+jsonld+'</script></head><body><a class="skip-link" href="#main">'+e(loc['skip'])+'</a><header class="site-header"><div class="nav-wrap"><a class="brand" href="'+path('home',lang)+'"><img src="'+PREFIX+'/assets/manager-icon.png" width="48" height="48" alt=""><span>AI Glasses<span class="brand-second">Manager</span></span></a><nav class="desktop-nav" aria-label="'+e(ui['main_navigation'])+'">'+nav+'</nav>'+langmenu+'<details class="mobile-menu"><summary aria-label="'+e(ui['open_navigation'])+'"><span aria-hidden="true">☰</span></summary><nav aria-label="'+e(ui['mobile_navigation'])+'">'+nav+'</nav></details></div></header><main id="main" class="'+kind+'">'+body+'</main><footer class="site-footer"><div class="footer-main"><div><strong>AI Glasses Manager</strong><p>'+e(loc['footer'])+'</p></div><div class="footer-links"><a href="'+REPO+'/issues">'+e(loc['support'])+'</a><a href="'+REPO+'">'+e(loc['source'])+'</a><a href="'+path('updates',lang)+'">'+e(loc['nav']['updates'])+'</a><a href="'+feed_url+'" title="Atom">'+e(loc['feed'])+'</a>'+langlinks+'</div></div><p class="privacy-note">'+e(loc['privacy'])+'</p><p class="copyright">© '+year+' Bruce · AI Glasses Manager</p></footer></body></html>\n'
def home(lang,page):
    loc=DATA['locales'][lang];ui=loc['ui']
    firstimage='<div class="screenshot-stack"><figure class="shot back"><img src="'+asset('home.png')+'" alt="'+e(ui['home_alt'])+'" width="480" height="640" decoding="async"></figure><figure class="shot front"><img src="'+asset('app-store.png')+'" alt="'+e(ui['store_alt'])+'" width="480" height="640" decoding="async"></figure><span class="screen-label">'+e(ui['actual_screens'])+'</span></div>'
    hero='<section class="hero"><div class="hero-copy"><span class="eyebrow">'+e(page['eyebrow'])+'</span><h1>'+''.join('<span>'+e(line)+'</span>' for line in page['h1_lines'])+'</h1><p class="hero-lede">'+e(page['lede'])+'</p><div class="hero-actions"><a class="button primary" href="'+REPO+'/releases/latest">'+e(loc['download'])+' <span aria-hidden="true">↗</span></a><a class="button secondary" href="'+path('features',lang)+'">'+e(page['secondary'])+'</a></div><p class="identity">'+e(page['identity'])+'</p><p class="price-note">'+e(ui['price_note'])+'</p></div>'+firstimage+'</section>'
    metrics='<div class="metrics">'+''.join('<div><strong>'+e(value)+'</strong><span>'+e(label)+'</span></div>' for value,label in page['metrics'])+'</div>'
    introduction='<div class="intro-note"><span class="initial" aria-hidden="true">B</span><p>'+e(page['intro'])+'</p></div>'
    store='<section class="home-feature"><div><span class="eyebrow">'+e(loc['nav']['app-store'])+'</span><h2>'+e(page['store_head'])+'</h2><p>'+e(page['store_body'])+'</p><a class="text-link" href="'+path('app-store',lang)+'">'+e(loc['more'])+' ↗</a></div><div class="store-explainer"><div><span class="small-label">'+e(ui['android_apps'])+'</span><h3>'+e(ui['catalogue_title'])+'</h3><p>'+e(ui['catalogue_body'])+'</p></div><div><span class="small-label">'+e(ui['rokid_projects'])+'</span><h3>'+e(ui['developer_title'])+'</h3><p>'+e(ui['developer_body'])+'</p></div></div></section>'
    camera='<section class="home-camera"><div class="section-top"><span class="eyebrow">'+e(loc['nav']['camera-filters'])+'</span><h2>'+e(page['camera_head'])+'</h2><p>'+e(page['camera_body'])+'</p><a class="text-link" href="'+path('camera-filters#how-to',lang)+'">'+e(page['camera_link'])+' ↗</a></div>'+filter_cards(DATA['pages']['camera-filters'][lang])+'</section>'
    daily='<section class="home-feature daily"><div><span class="eyebrow">'+e(loc['nav']['features'])+'</span><h2>'+e(page['daily_head'])+'</h2><p>'+e(page['daily_body'])+'</p><a class="text-link" href="'+path('features',lang)+'">'+e(page['secondary'])+' ↗</a></div><div class="tool-links">'+''.join('<a href="'+path(target,lang)+'"><span>'+e(label)+'</span><span aria-hidden="true">↗</span></a>' for target,label in [('files',loc['nav']['files']),('features#sound',ui['sound_tools']),('features#shortcuts',ui['shortcuts']),('help',loc['nav']['help'])])+'</div></section>'
    updates='<section class="home-updates"><span class="eyebrow">'+e(loc['nav']['updates'])+'</span><h2>'+e(page['updates_head'])+'</h2><p>'+e(page['updates_body'])+'</p>'+release_cards(lang,2)+'<a class="text-link" href="'+path('updates',lang)+'">'+e(loc['all_updates'])+' ↗</a></section>'
    return hero+metrics+introduction+store+camera+daily+updates+teaser(lang)
def standard(lang,page,slug):
    loc=DATA['locales'][lang]
    head='<header class="page-heading"><span class="eyebrow">'+e(page['eyebrow'])+'</span><h1>'+e(page['h1'])+'</h1><p>'+e(page['lede'])+'</p></header>'
    if slug=='updates': return head+release_cards(lang)+teaser(lang)
    sections=page.get('sections',[])
    toc='<nav class="page-toc" aria-label="'+e(loc['on_this_page'])+'">'+''.join('<a href="#'+e(row['id'])+'">'+e(row['title'])+'</a>' for row in sections)+'</nav>' if len(sections)>3 else ''
    body=head+toc
    if page.get('how_to'):
        guide=page['how_to']
        body+='<section class="filter-guide" id="how-to"><h2>'+e(guide['title'])+'</h2><ol>'+''.join('<li>'+e(step)+'</li>' for step in guide['steps'])+'</ol></section>'
    if page.get('filters'):body+=filter_cards(page)
    body+=''.join(section_html(section,i+1) for i,section in enumerate(sections))
    if page.get('faq'):
        body+='<pre class="install-command"><code>adb install -r AI-Glasses-Manager-'+e(VERSION)+'.apk</code></pre><div class="faq-list">'+''.join('<details><summary>'+e(question)+'</summary><p>'+e(answer)+'</p></details>' for question,answer in page['faq'])+'</div>'
    if any(row.get('image') for row in sections):body+='<p class="screen-note">'+e(loc['screen_note'])+'</p>'
    return body

def build():
    urls=[]
    for lang in DATA['locales']:
        for slug,translations in DATA['pages'].items():
            page=translations[lang];body=home(lang,page) if slug=='home' else standard(lang,page,slug)
            relative=('/'.join(filter(None,[(lang if lang!='en' else ''),('' if slug=='home' else slug),'index.html'])))
            write(relative,layout(slug,lang,page,body,'home-page' if slug=='home' else 'reference-page'))
            urls.append(url(slug,lang))
        for release in DATA['releases']:
            version=release['version'];localized=release[lang];slug='updates/'+version
            page={'title':'AI Glasses Manager '+version+' | '+localized['title'],'description':localized['summary'],'h1':'AI Glasses Manager '+version}
            headings='<header class="page-heading release-heading"><a class="text-link" href="'+path('updates',lang)+'">'+e(DATA['locales'][lang]['all_updates'])+'</a><p class="eyebrow"><time datetime="'+release['published']+'">'+release['published'][:10]+'</time></p><h1>'+e(page['h1'])+'</h1><h2>'+e(localized['title'])+'</h2><p>'+e(localized['summary'])+'</p></header>'
            body=headings+''.join(section_html({'id':'change-'+str(i),'title':title,'paragraphs':[],'bullets':items},i+1) for i,(title,items) in enumerate(localized['items']))
            body+='<div class="release-source"><p>'+e(DATA['locales'][lang]['ui']['release_source'])+'</p><a class="button secondary" href="'+REPO+'/releases/tag/v'+version+'">'+e(DATA['locales'][lang]['ui']['original_release'])+' ↗</a></div>'
            relative='/'.join(filter(None,[(lang if lang!='en' else ''),'updates',version,'index.html']))
            write(relative,layout(slug,lang,page,body,'reference-page',release));urls.append(url(slug,lang))
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);sitemap=ET.Element('{'+ns+'}urlset')
    release_dates={url('updates/'+r['version'],lang):r.get('updated',r['published']) for r in DATA['releases'] for lang in DATA['locales']}
    for address in urls:
        entry=ET.SubElement(sitemap,'{'+ns+'}url');ET.SubElement(entry,'{'+ns+'}loc').text=address;ET.SubElement(entry,'{'+ns+'}lastmod').text=release_dates.get(address,DATA['updated'])
    write('sitemap.xml',ET.tostring(sitemap,encoding='unicode',xml_declaration=True))
    ns='http://www.w3.org/2005/Atom';ET.register_namespace('',ns)
    for lang in DATA['locales']:
        feed=ET.Element('{'+ns+'}feed',{'{http://www.w3.org/XML/1998/namespace}lang':DATA['locales'][lang]['lang']})
        def atom(parent,name,text):ET.SubElement(parent,'{'+ns+'}'+name).text=text
        feed_url=url('updates',lang)+'feed.xml'
        atom(feed,'id',url('updates',lang));atom(feed,'title','AI Glasses Manager '+DATA['locales'][lang]['ui']['feed_title']);atom(feed,'updated',max(r.get('updated',r['published']) for r in DATA['releases']));ET.SubElement(feed,'{'+ns+'}link',href=feed_url,rel='self');ET.SubElement(feed,'{'+ns+'}link',href=url('updates',lang));author=ET.SubElement(feed,'{'+ns+'}author');atom(author,'name','Bruce')
        for release in DATA['releases']:
            entry=ET.SubElement(feed,'{'+ns+'}entry');address=url('updates/'+release['version'],lang);atom(entry,'id',address);atom(entry,'title','AI Glasses Manager '+release['version']+': '+release[lang]['title']);atom(entry,'published',release['published']);atom(entry,'updated',release.get('updated',release['published']));ET.SubElement(entry,'{'+ns+'}link',href=address);atom(entry,'summary',release[lang]['summary'])
        write((lang+'/' if lang!='en' else '')+'updates/feed.xml',ET.tostring(feed,encoding='unicode',xml_declaration=True))
    write('.nojekyll','')
    write('404.html','<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | AI Glasses Manager</title><body><h1>That page is not here.</h1><p><a href="'+PREFIX+'/">Open AI Glasses Manager</a></p></body></html>')
    print('Built',len(urls),'localized pages, sitemap and release feeds.')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=DOCS,help='Output directory for generated files')
    args=parser.parse_args()
    DOCS=args.output.resolve()
    build()
