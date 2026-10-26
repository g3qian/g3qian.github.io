"""Browser verification of the built site (requires Playwright and Chromium); writes data/verification.json.

Run after `quarto render`: python3 scripts/verify_browser.py
"""
import asyncio, json, sys, subprocess, http.server, threading, functools, datetime
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]; SITE=ROOT/'_site'
routes=['/','/work.html','/experience.html','/publications.html','/about.html']+[f'/work/{p.stem}.html' for p in sorted((ROOT/'work').glob('*.qmd'))]
handler=functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
handler=functools.partial(Quiet, directory=str(SITE))
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler); port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{port}'
async def main():
    out=dict(checked_on=str(datetime.date.today()),pages=len(routes))
    check=json.loads(subprocess.run(['python3',str(ROOT/'scripts/check_site.py')],capture_output=True,text=True).stdout)
    out['local_references_checked']=check['local_references_checked']; out['check_site_errors']=check['errors']
    out['registered_dois']=sum(1 for p in json.loads((ROOT/'data/publications.json').read_text()) if p.get('doi'))
    errors=[]; resp=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in (390,768,1440):
            pg=await b.new_page(viewport={'width':w,'height':900})
            pg.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
            pg.on('pageerror',lambda e: errors.append(str(e)))
            for r in routes:
                await pg.goto(base+r); await pg.wait_for_load_state('networkidle')
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(250)
                info=await pg.evaluate("""() => ({
                  brokenImages:[...document.querySelectorAll('main img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src')),
                  h1:document.querySelectorAll('main h1, header h1').length,
                  pageWidth:document.documentElement.scrollWidth,
                  glanceWidth:(document.querySelector('.glance')||{}).offsetWidth||null,
                  firstFigureY:(()=>{const i=document.querySelector('main img');return i?Math.round(i.getBoundingClientRect().top+scrollY):null})()})""")
                info={k:v for k,v in info.items() if v is not None}
                resp.append(dict(width=w,route=r,**info))
            await pg.close()
        pg=await b.new_page(viewport={'width':1440,'height':900}); await pg.goto(base+'/')
        await pg.keyboard.press('Tab'); skip=await pg.evaluate("document.activeElement && /skip/i.test(document.activeElement.textContent||'')")
        await pg.goto(base+'/work/corrosion-simulation.html')
        lightbox=await pg.evaluate("!!document.querySelector('a.lightbox, .glightbox, [data-glightbox]')")
        pg2=await b.new_page(viewport={'width':390,'height':900}); await pg2.goto(base+'/')
        tog=await pg2.query_selector('.navbar-toggler'); nav='failed'
        if tog:
            await tog.click(); await pg2.wait_for_timeout(500)
            nav='passed' if await pg2.evaluate("[...document.querySelectorAll('.navbar-collapse a')].some(a=>a.offsetParent!==null)") else 'failed'
        await b.close()
    out.update(keyboard_skip_link='passed' if skip else 'failed', figure_lightbox='passed' if lightbox else 'failed', mobile_navigation=nav, console_errors=sorted(set(errors)), responsive=resp)
    out['overflow']=[f"{x['route']}@{x['width']}" for x in resp if x['pageWidth']>x['width']]
    out['broken_images']=[f"{x['route']}@{x['width']}" for x in resp if x.get('brokenImages')]
    (ROOT/'data/verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='responsive'},indent=1))
asyncio.run(main())
