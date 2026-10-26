"""Regenerate shared page fragments from the canonical publication list.

Run with Python 3 from any directory. No third-party dependencies are required.
"""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "includes"
PAPERS = json.loads((ROOT / "data/publications.json").read_text())
MINOR = {"a","an","and","as","at","but","by","for","from","in","into","nor","of","on","or","per","the","to","via","vs","with"}

def title_case(text):
    """Capitalize the main words of a title; keep acronyms, units, and minor words."""
    words = text.split(" ")
    out = []
    for i, word in enumerate(words):
        first = i == 0 or out[-1].endswith(":")
        last = i == len(words) - 1
        parts = word.split("-")
        fixed = []
        for j, part in enumerate(parts):
            core = part.strip("()\"'“”‘’,.;")
            if not core or any(c.isupper() for c in core[1:]) or not core[0].isalpha():
                fixed.append(part)  # acronyms (MSSP, cINN), numbers, mixed case
            elif core.lower() in MINOR and not ((first or last) and j == 0) and not (j > 0 and j == len(parts) - 1 and last):
                fixed.append(part.replace(core, core.lower(), 1))
            else:
                fixed.append(part.replace(core, core[0].upper() + core[1:], 1))
        out.append("-".join(fixed))
    return " ".join(out)

# Bridge monitoring first, followed by the connected corrosion studies and generalized diagnosis.
CASES = [
    dict(slug="bridge-oma-temperature", title="Operational Modal Analysis and Temperature Effects on Natural Frequencies", meta="Engineering Practice · LPI · 2025–2026", result="Automated modal identification on twin bridges: the damaged one vibrates lower (3.44 vs 3.52 Hz) and responds differently to temperature.", tag="Operational Modal Analysis · Monitoring", image="card.webp", alt="Aerial view of the twin highway bridges with photographs of T1 and T2"),
    dict(slug="corrosion-simulation", title="Multiphysics Corrosion Simulation and Surrogate Modeling", meta="Doctoral Research · UC San Diego · 2021–2023", result="Stress-aware simulations of how pits grow into cracks, and surrogates that forecast 200 time steps in 1.3–5.4 seconds after training.", tag="Phase-Field Modeling · Machine Learning", image="card.webp", alt="Simulated pit shapes and hydrostatic stress under tension and compression"),
    dict(slug="corrosion-reliability", title="Uncertainty Propagation and Reliability Analysis", meta="Doctoral Research · UC San Diego · 2022–2023", result="A gate-wide crack-initiation risk map, with 6.7× fewer evaluations in the local reliability benchmark.", tag="Reliability · Adaptive Surrogates", image="card.webp", alt="Model-predicted crack-initiation probability over the Greenup miter gate"),
    dict(slug="corrosion-model-updating", title="Bayesian Model Updating with Real Measurements", meta="Doctoral and Postdoctoral Research · UC San Diego with Cal Poly · 2022–2025", result="Four-second model updates, and a laboratory forecast of the 95th-percentile pit-opening radius with 11% error, versus 51% for a power law.", tag="Bayesian Inference · Experiments", image="card.webp", alt="Laboratory corrosion depth maps at successive exposure times"),
    dict(slug="generalized-damage-diagnosis", title="Generalized Damage Diagnosis Across Similar Structures", meta="Postdoctoral Research · UC San Diego · 2024–2025", result="On simulated gate responses, transferring knowledge from The Dalles cut gap-prediction error on Bonneville by 78%.", tag="Domain Adaptation · Population-Based SHM", image="card.webp", alt="The Dalles and Bonneville gate finite-element models, source and target"),

]

def write(name, content):
    # Raw HTML keeps Pandoc from reparsing block-level links in whole-card anchors.
    (OUT / name).write_text("```{=html}\n" + content + "\n```\n")

def card(case):
    return f'''<a class="project-card" href="work/{case['slug']}.html">
  <div class="card-media"><img src="images/{case['slug']}/{case['image']}" width="1200" height="800" alt="{e(case['alt'])}" loading="lazy"></div>
  <div class="card-body"><div class="eyebrow">{e(case['meta'])}</div><h3>{e(case['title'])}</h3><p>{e(case['result'])}</p><div class="card-end"><span>{e(case['tag'])}</span><span aria-hidden="true">↗</span></div></div>
</a>'''

write("work-cards.html", '<div class="card-grid">\n' + "\n".join(map(card, CASES)) + "\n</div>")
write("home-cards.html", '<div class="card-grid">\n' + "\n".join(map(card, CASES)) + "\n</div>")

write("facts-bridge.html", '''<dl class="fact-strip"><div><dt>My Role</dt><dd>R&amp;D Engineer, lead author</dd></div><div><dt>Methods</dt><dd>Automated OMA (FDD, SSI-COV), bootstrap, bilinear regression</dd></div><div><dt>Publication</dt><dd>EWSHM 2026, Toulouse<br>With J.-H. Bartels, C. Tomann, N. Dieckmann</dd></div></dl>''')
write("glance-bridge.html", '''<div class="glance" role="region" aria-labelledby="glance-title"><h2 id="glance-title">In Brief</h2><dl><dt>What I Did</dt><dd>Built an automated operational modal analysis pipeline with uncertainty bounds, and related months of frequency estimates to temperatures measured inside the concrete.</dd><dt>What We Found</dt><dd>The damaged bridge vibrates lower, and the frequency–temperature relationship is bilinear, with a different slope for each bridge.</dd></dl></div>''')

def publication(p):
    pills = []
    if p.get('status'): pills.append(f'<span class="pill accepted">{e(p["status"])}</span>')
    if p.get('doi'): pills.append(f'<a class="pill" href="https://doi.org/{p["doi"]}" aria-label="DOI for {e(p["title"])}">DOI ↗</a>')
    if p.get('code'): pills.append(f'<a class="pill" href="{p["code"]}">Code ↗</a>')
    if p.get('award'): pills.append(f'<span class="pill award">{e(p["award"])}</span>')
    target = 'work.html#other-work' if p['case'] == 'other-work' else f'work/{p["case"]}.html'
    related = 'Related Work' if p['case'] == 'other-work' else 'Related Case Study'
    pills.append(f'<a class="related" href="{target}">{related} →</a>')
    authors = e(p['authors']).replace('Guofeng Qian', '<strong>Guofeng Qian</strong>')
    year = 'Accepted' if p.get('status') else p['year']
    return f'''<article class="publication" id="{p['id']}"><h3>{e(title_case(p['title']))}</h3><p>{authors}.</p><p class="venue"><i>{e(p['venue'])}</i> · {year}</p><div class="publication-links">{''.join(pills)}</div></article>'''

parts = []
for typ, heading in [('journal', 'Journal Articles'), ('book', 'Book Chapter'), ('conference', 'Conference Contributions')]:
    parts.append(f'<section aria-labelledby="{typ}-heading"><h2 id="{typ}-heading">{heading}</h2>')
    last_year = None
    for p in PAPERS:
        if p['type'] != typ: continue
        if typ == 'conference' and p['year'] != last_year:
            parts.append(f'<h3>{p["year"]}</h3>'); last_year = p['year']
        parts.append(publication(p))
    parts.append('</section>')
write('all-publications.html', '\n'.join(parts))

selected = [
    ('journal-physics', 'The Physics of a Growing Pit', 'A stress-aware model of corrosion and crack initiation.', 'corrosion-simulation/stress-and-pit-shape.webp', 'Scientific Reports · 2022'),
    ('journal-reliability', 'A Risk Map of a Whole Gate', 'Adaptive surrogates make structural reliability practical.', 'corrosion-reliability/gate-risk-map.webp', 'MSSP · 2023'),
    ('journal-cinn', 'Model Updating in Seconds', 'Fast Bayesian inference with conditional invertible networks.', 'corrosion-model-updating/inference-workflow.webp', 'JRUE-B · 2025'),
    ('journal-hybrid', 'Checked Against Experiments', 'Blind predictions of corrosion severity on real specimens.', 'corrosion-model-updating/pit-depth-maps.webp', 'JCSHM · Accepted'),
]
write('selected-publications.html', '<div class="selected-publications">' + ''.join(f'<a class="selected-paper" href="#{pid}"><img src="images/{img}" alt="" width="110" height="110" loading="lazy"><div><div class="eyebrow">{e(venue)}</div><h3>{e(title)}</h3><p>{e(summary)}</p></div></a>' for pid,title,summary,img,venue in selected) + '</div>')

for slug, filename in [('corrosion-simulation', 'simulation'), ('corrosion-reliability', 'reliability'), ('corrosion-model-updating', 'updating'), ('generalized-damage-diagnosis', 'diagnosis')]:
    refs = ['<section class="case-references"><h2>Publications</h2><ul>']
    for p in PAPERS:
        if p['case'] != slug: continue
        status = 'accepted' if p.get('status') else str(p['year'])
        doi = f' <a href="https://doi.org/{p["doi"]}">DOI ↗</a>' if p.get('doi') else ''
        award = ' · Best Paper (coauthor)' if p.get('award') else ''
        refs.append(f'<li><a href="../publications.html#{p["id"]}">{e(title_case(p["title"]))}</a>. <i>{e(p["venue"])}</i>, {status}{award}.{doi}</li>')
    refs.append('</ul></section>');write(f'references-{filename}.html', '\n'.join(refs))

print(f'Generated cards and references for {len(CASES)} case studies and {len(PAPERS)} publications.')
