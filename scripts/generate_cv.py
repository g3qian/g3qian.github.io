"""Build the site's corrected academic CV from supplied facts and shared citations.

Requires reportlab. This creates the website copy and never changes the source CV.
"""
from pathlib import Path
from html import escape
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'files/Guofeng_Qian_CV.pdf'
OUT.parent.mkdir(exist_ok=True)
PAPERS=json.loads((ROOT/'data/publications.json').read_text())
pdfmetrics.registerFont(TTFont('Body','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('BodyBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Serif','/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
INK=colors.HexColor('#1C2430');ACCENT=colors.HexColor('#1F5C7A');MUTED=colors.HexColor('#5B6573')
styles={
 'title':ParagraphStyle('title',fontName='Serif',fontSize=30,leading=35,textColor=INK,spaceAfter=10),
 'h1':ParagraphStyle('h1',fontName='Serif',fontSize=21,leading=25,textColor=ACCENT,spaceBefore=6,spaceAfter=14),
 'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=11,leading=15,textColor=INK,spaceBefore=15,spaceAfter=6,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.4,leading=13.7,textColor=INK,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.6,leading=12.5,textColor=MUTED,spaceAfter=8),
 'pub':ParagraphStyle('pub',fontName='Body',fontSize=9,leading=13.1,textColor=INK,spaceAfter=12),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.4,leading=13.7,textColor=INK,leftIndent=10,firstLineIndent=-8,spaceAfter=5),
}
story=[]
def clean(s):
 return s.replace('–','-').replace('—','-').replace('‑','-').replace('→','to').replace('×','x').replace('’',"'").replace('“','"').replace('”','"')
def p(text,style='body'):
 story.append(Paragraph(clean(text),styles[style]))
def heading(text):p(text,'h2')
def bullet(text):p('- '+text,'bullet')
def page(title):story.append(PageBreak());p(title,'h1')
def citation(item):
 authors=escape(item['authors']).replace('Guofeng Qian','<b>Guofeng Qian</b>')
 year='Accepted' if item.get('status') else str(item['year'])
 text=f'{authors}. <b>{escape(item["title"])}</b>. {escape(item["venue"])} ({year}).'
 if item.get('doi'):text+=f' <link href="https://doi.org/{item["doi"]}" color="#1F5C7A">doi:{item["doi"]}</link>'
 if item.get('award'):text+=' <b>Best Paper (coauthor).</b>'
 if item.get('code'):text+=f' <link href="{item["code"]}" color="#1F5C7A">Open code.</link>'
 p(text,'pub')

p('Guofeng Qian','title')
p('Vancouver, BC, Canada | +1 858 257 8628 | <link href="mailto:g3qian@gmail.com" color="#1F5C7A">g3qian@gmail.com</link><br/><link href="https://scholar.google.com/citations?user=KxP9bSkAAAAJ" color="#1F5C7A">Google Scholar</link> | <link href="https://www.linkedin.com/in/guofeng-qian-a01840207/" color="#1F5C7A">LinkedIn</link>','small')
p('Canadian Permanent Resident; authorized to work in Canada.','small')
heading('Research profile')
p('Structural engineer and researcher developing physics-informed digital twins for infrastructure condition assessment, deterioration prediction, and risk-informed decisions. Expertise in computational mechanics, scientific machine learning, structural monitoring, Bayesian inference, uncertainty quantification, and structural reliability. Experience spans government-supported research and monitoring of operating bridges.')
heading('Education')
p('<b>Ph.D. in Structural Engineering</b> | University of California San Diego<br/>January 2021 - December 2023 | Advisor: Prof. Michael D. Todd')
p('Dissertation: Diagnostics and Prognostics of Pitting Corrosion in Large Civil Infrastructure Using Multi-Scale Simulation and Machine Learning.','small')
p('<b>M.S. in Structural Engineering</b> | University of California San Diego<br/>September 2019 - December 2020 | Health Monitoring and Nondestructive Evaluation')
p('<b>B.Eng. in Civil Engineering</b> | Harbin Institute of Technology<br/>September 2015 - June 2019')
p('<b>Exchange student</b> | Monash University | January - June 2018')
heading('Engineering experience')
p('<b>Research and Development Engineer</b><br/>LPI Ingenieurgesellschaft mbH, Hannover, Germany | September 2025 - August 2026')
bullet('Developed simulation- and monitoring-based bridge assessment workflows combining finite-element modeling, structural dynamics, uncertainty quantification, and long-term field measurements.')
bullet('Automated parametric SOFiSTiK simulations and output-only modal analysis with Python. Compared temperature-dependent dynamics of twin bridges, one with documented tendon breaks.')
bullet('Developed strain-based impact detection and combined strain, displacement, and inclination measurements. Interpretation supported a client decision to maintain a damaged steel bridge\'s closure.')
bullet('Developed acoustic-emission and distributed fiber-optic workflows for wire-break classification, crack localization, and crack-width estimation.')

page('Research and teaching experience')
p('<b>University of California San Diego</b> | La Jolla, United States','small')
heading('Postdoctoral researcher | January 2024 - August 2025')
bullet('Extended a USACE/ERDC-supported digital-twin program from individual structures to population-based diagnostics and changing environmental conditions.')
bullet('Developed domain-adaptation methods for damage diagnostics across structures and temperature conditions. On simulated Bonneville responses, gap MSE fell from 0.069 to 0.015 with target labels withheld during training.')
bullet('Developed normalizing-flow-based Bayesian updating for multiphysics corrosion models and integrated predictions with accelerated corrosion experiments.')
bullet('Presented semiannual sponsor reviews, developed proposal content, and mentored graduate and undergraduate researchers.')
heading('Graduate student researcher | January 2021 - December 2023')
bullet('Built a coupled mechano-electrochemical phase-field model of localized corrosion. Connected pit evolution with structural stress analysis and crack-initiation reliability of miter gates.')
bullet('Automated parametric simulations and developed autoencoder-based reduced models and probabilistic forecasts. Contributed simulation data and the baseline surrogate to physics-constrained morphology forecasting.')
bullet('Combined active learning, importance sampling, and machine-learning surrogates for gate-wide risk maps; the local reliability benchmark used 101 function evaluations versus 674 for AK-MCS.')
bullet('Developed two-stage approximate Bayesian computation and conditional invertible neural networks for updating corrosion models from inspection images and experimental observations.')
heading('Research assistant | January - December 2020')
bullet('Modeled composite wing-spar debonding in Abaqus, automated parametric simulations and result extraction, and developed a deep-learning surrogate for strain across damage locations and severities.')
heading('Teaching assistant | University of California San Diego')
p('<b>SE 168/268 Structural System Testing and Model Correlation</b> | Spring 2022, 2023<br/>Co-taught by Prof. Michael Todd and ATA Engineering.')
bullet('Led labs in test planning, hammer and shaker excitation, accelerometer instrumentation, synchronized acquisition, and data quality.')
bullet('Guided processing of frequency-response functions, coherence and reciprocity checks, modal identification, finite-element correlation, model reduction, and boundary-stiffness updating.')
p('<b>SE 130A/B Structural Analysis I and II</b> | Summer 2021')

page('Journal articles and book chapter')
for item in PAPERS:
 if item['type']=='journal':citation(item)
heading('Book chapter')
for item in PAPERS:
 if item['type']=='book':citation(item)

page('Conference contributions | 2026-2025')
for year in [2026,2025]:
 heading(str(year))
 for item in PAPERS:
  if item['type']=='conference' and item['year']==year:citation(item)

page('Conference contributions and research program')
for year in [2024,2023]:
 heading(str(year))
 for item in PAPERS:
  if item['type']=='conference' and item['year']==year:citation(item)
heading('Research proposal development | 2021-2025')
p('USACE/ERDC, Innovative Technologies in Structural Health Monitoring for Condition Assessment and Reliability Prediction (W9132T-22-20014). Developed research concepts, proposed methods, preliminary results, and subsequent tasks for continuation proposals. Presented directions and progress at semiannual technical reviews.')
for text in ['2025: Multimode multiphysics damage prognostics using physics-based and data-driven simulation.', '2025: Population-based damage diagnostics with multisource information transfer.', '2024: Likelihood-free Bayesian model updating with synthetic image observations.', '2023: Reliability analysis of localized corrosion using multiscale simulation.', '2022: Multiphysics corrosion simulation and machine-learning surrogate modeling.']:bullet(text)

page('Mentoring, service, and skills')
heading('Research mentorship')
p('<b>Haiwei Lin</b>, Ph.D. researcher, UC San Diego | Summer 2024 - Fall 2025')
bullet('Initiated a collaboration with Prof. Shabnam Semnani to connect the corrosion model with phase-field fracture. Mentored formulation, multiphysics implementation, interpretation, and research communication.')
p('<b>Vaibhav Pratap</b>, M.S. independent study, UC San Diego | Spring 2023')
bullet('Provided technical guidance in reliability analysis and uncertainty quantification.')
p('<b>Edward Yu and Peter Le</b>, NSF REU, UC San Diego | Summer 2022')
bullet('Guided cantilever-plate testing and MATLAB finite-element correlation, including accelerometer placement, modal properties, and rotational-spring updating to identify changes in connection stiffness.')
heading('Academic and professional service')
p('Journal reviewer: ASCE-ASME Journal of Risk and Uncertainty, Part B; Journal of Computational Physics; Journal of Verification, Validation and Uncertainty Quantification; Journal of Structural Design and Construction Practice.')
p('Society for Experimental Mechanics (SEM), 2022 - Present.<br/>Earthquake Engineering Research Institute (EERI), 2022 - Present.')
heading('Selected honors and awards')
for text in ['Best Paper, IWSHM 2025, federated-learning paper (coauthor).','Distinguished Graduate Thesis, 2019.','International Study Grant, Monash University, 2018.','Best Paper, International Conference for Integration of Science, Technology and Society, 2016.','"Xu Zengquan" Scholarship, 2016.']:bullet(text)
heading('Technical skills')
p('<b>Machine learning:</b> surrogate modeling, physics-informed learning, CNNs, autoencoders, Bayesian neural networks, Gaussian processes, normalizing flows, domain adaptation, adversarial learning.')
p('<b>Computational and probabilistic methods:</b> finite-element and multiphysics simulation, Bayesian inference, model updating, Monte Carlo methods, uncertainty quantification, structural reliability.')
p('<b>Monitoring:</b> modal analysis, system identification, signal processing, acoustic emission, distributed fiber-optic sensing.')
p('<b>Programming and software:</b> Python, PyTorch, TensorFlow, MATLAB, Abaqus, COMSOL, FEniCSx, SOFiSTiK, Git, LaTeX.')

def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#E5E1D8'));c.line(48,43,564,43)
 c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(48,29,'Guofeng Qian | Curriculum vitae | October 2026');c.drawRightString(564,29,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=60,title='Guofeng Qian - Curriculum Vitae',author='Guofeng Qian')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
