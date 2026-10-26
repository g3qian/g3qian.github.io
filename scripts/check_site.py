"""Audit the rendered static site using only the Python standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Node:
    def __init__(self,tag='',attrs=(),parent=None):
        self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[]
    def all(self,tag=None):
        for c in self.children:
            if isinstance(c,Node):
                if tag is None or c.tag==tag:yield c
                yield from c.all(tag)
    def text(self):
        return ' '.join(c.text() if isinstance(c,Node) else c for c in self.children if not isinstance(c,Node) or c.tag not in {'script','style'})

class Document(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(node)
        if tag not in VOID:self.stack.append(node)
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)

pages=sorted([*SITE.glob('*.html'),*(SITE/'work').glob('*.html')])
docs={p:Document(p).root for p in pages}
errors=[];links=0;counts={}
if len(pages)!=10:print(f'Note: expected 10 pages; found {len(pages)}')
for path,doc in docs.items():
    rel=str(path.relative_to(SITE));mains=list(doc.all('main'))
    if len(mains)!=1:errors.append(f'{rel}: expected one main landmark');continue
    main=mains[0]
    if len(list(main.all('h1')))!=1:errors.append(f'{rel}: expected one H1')
    if not any(n.attrs.get('name')=='description' and n.attrs.get('content') for n in doc.all('meta')):errors.append(f'{rel}: missing description')
    for n in main.all('img'):
        if 'alt' not in n.attrs:errors.append(f'{rel}: image lacks alt: {n.attrs.get("src")}')
    for n in main.all('a'):
        if not n.text().strip() and not n.attrs.get('aria-label') and not list(n.all('img')):errors.append(f'{rel}: empty link: {n.attrs.get("href")}')
    for n in doc.all():
        for attr in ('href','src'):
            val=n.attrs.get(attr)
            if not val:continue
            url=urlsplit(val)
            if url.scheme or url.netloc:continue
            links+=1
            dest=(SITE/unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
            if not url.path:dest=path
            if dest.is_dir():dest=dest/'index.html'
            dest=dest.resolve()
            if not dest.is_file():errors.append(f'{rel}: missing {val}');continue
            if url.fragment and dest.suffix=='.html':
                target=docs.get(dest) or Document(dest).root
                if not any(x.attrs.get('id')==unquote(url.fragment) or x.attrs.get('name')==unquote(url.fragment) for x in target.all()):errors.append(f'{rel}: missing anchor {val}')
    text=main.text()
    if re.search(r'placeholder|replace with|draft gallery',text,re.I):errors.append(f'{rel}: unfinished copy')
    if 'work/' in rel:
        # Count the narrative only; bibliographic reference lists are excluded.
        refs=' '.join(n.text() for n in main.all() if 'case-references' in n.attrs.get('class',''))
        count=len(text.split())-len(refs.split());counts[rel]=count
        limit=900
        if count>limit:errors.append(f'{rel}: case study is too long ({count} words)')
    for p in main.all('p'):
        # Publication titles and author lists are bibliographic records, not body paragraphs.
        ancestor=p.parent; bibliographic=False
        while ancestor:
            if ancestor.tag=='article' or 'case-references' in ancestor.attrs.get('class',''):bibliographic=True
            ancestor=ancestor.parent
        if not bibliographic and len(p.text().split())>65:errors.append(f'{rel}: body paragraph exceeds 65 words')

# Stale output can mask a renamed or removed page: every built page needs a source, and every source a built page.
for page in pages:
    src=ROOT/page.relative_to(SITE).with_suffix('.qmd')
    if not src.is_file():errors.append(f'Built page has no source (stale _site; run a full quarto render): {page.relative_to(SITE)}')
for src in [*ROOT.glob('*.qmd'),*(ROOT/'work').glob('*.qmd')]:
    if not (SITE/src.relative_to(ROOT).with_suffix('.html')).is_file():errors.append(f'Source page was not built: {src.relative_to(ROOT)}')
# Images must exist in the source tree, not only in an older build.
for path,doc in docs.items():
    for n in doc.all('img'):
        src=n.attrs.get('src','')
        if src.startswith(('http','data:')) or 'site_libs' in src:continue
        target=(path.parent/unquote(src)).resolve()
        try:rel=target.relative_to(SITE.resolve())
        except ValueError:continue
        if str(rel).startswith('images') and not (ROOT/rel).is_file():errors.append(f'{path.relative_to(SITE)}: image missing from source images/: {rel}')
cases={c.stem for c in (ROOT/'work').glob('*.qmd')}

pubs=json.loads((ROOT/'data/publications.json').read_text())
for p in pubs:
    if p['case']!='other-work' and p['case'] not in cases:errors.append(f"Publication {p['id']} points to a missing case study: {p['case']}")
if len(pubs)!=23 or len({p['id'] for p in pubs})!=23:errors.append('Publication list is incomplete or contains duplicate IDs')
accepted=next(p for p in pubs if p['id']=='journal-hybrid')
if accepted.get('doi') or accepted.get('status')!='Accepted':errors.append('JCSHM status/DOI correction lost')
cinn=next(p for p in pubs if p['id']=='journal-cinn')
if cinn['year']!=2025 or '011105' not in cinn['venue']:errors.append('JRUE-B citation correction lost')
awards=[p['id'] for p in pubs if p.get('award')]
if awards!=['conf-federated']:errors.append('Best Paper assigned to the wrong publication')

for path in (ROOT/'images').rglob('*'):
    if path.is_file() and path.stat().st_size>400_000:errors.append(f'Image exceeds 400 KB: {path.relative_to(ROOT)}')
home=docs[SITE/'index.html']
payload=sum((SITE/n.attrs['src']).stat().st_size for n in next(home.all('main')).all('img'))
if payload>2_000_000:errors.append('Home image payload exceeds 2 MB')
for p in SITE.rglob('*'):
    if p.is_file() and (p.suffix.lower() in {'.mat','.pptx','.docx','.m'} or 'supporting-material' in str(p)):errors.append(f'Non-public source file in build: {p}')

print(json.dumps({'pages':len(pages),'local_references_checked':links,'publications':len(pubs),'home_images_kb':round(payload/1024),'case_words':counts,'errors':errors},indent=2))
raise SystemExit(bool(errors))
