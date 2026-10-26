# Guofeng Qian portfolio

Live website: [g3qian.github.io](https://g3qian.github.io/) · [GitHub repository](https://github.com/g3qian/g3qian.github.io)

A Quarto website implemented from the files in `../plan/`. The previous site is retained as a legacy reference. This folder contains eleven pages, six case studies, research figures, shared data for 23 publications, and a reviewed six-page CV. The current source review and maintenance status are documented in `../plan/`.

```sh
quarto preview
quarto render
```

The static build is written to `_site/`. Serve that directory with any static web server. Quarto 1.10.19 was used for the initial build; no npm installation is required.

## Editing

- Edit the `.qmd` pages for content, `theme.scss` for typography and colors, and `styles.css` for layout.
- Edit `data/publications.json`; a pre-render hook updates publication entries, case-study references, and shared card fragments automatically. You can also run `python3 scripts/generate_content.py` directly.
- `scripts/prepare_media.py` re-extracts the selected raster figures from the source decks and real figures in the old site. The benchmark SVG is maintained directly and recorded in the media manifest. It requires Pillow and python-pptx. The decks are not needed to build or preview the site.
- `scripts/prepare_teaching_media.py` extracts the two selected course equipment photographs using pypdf and Pillow; the teaching diagrams are maintained directly as SVG. Raw course files stay outside the site.
- `scripts/generate_cv.py` rebuilds `files/Guofeng_Qian_CV.pdf` using ReportLab. The publication list is shared with the website. Source PDF files remain unchanged.
- Run `python3 scripts/check_site.py` after rendering to check local assets, internal links and anchors, accessibility metadata, page structure, publication corrections, and image budgets. It also flags stale output: built pages with no source, sources that were not built, images that exist only in `_site/`, and publications that point to a missing case study.
- `python3 scripts/verify_browser.py` (Playwright) checks every page at 390, 768, and 1440 px for broken images, horizontal overflow, console errors, the skip link, the lightbox, and mobile navigation, and writes `data/verification.json`.
- Always use a full `quarto render` before publishing. It clears `_site/`, so renamed or removed pages cannot linger; `quarto preview` alone does not.

## Content decisions

- LPI: September 2025-August 2026, confirmed during implementation.
- The site introduces Guofeng as an engineer and researcher; it is not written as a job application. Bridge monitoring appears first, followed by vibration testing and model correlation, the three connected corrosion studies, and generalized damage diagnosis.
- Home shows Selected Work directly after a short introduction; each card states one concrete result. Case studies open with a figure, a one-paragraph introduction, and a two-part In Brief (What I Did, What We Found).
- Six case studies, in order: Operational Modal Analysis and Temperature Effects on Natural Frequencies; Structural Vibration Testing and Model Correlation; Multiphysics Corrosion Simulation and Surrogate Modeling; Uncertainty Propagation and Reliability Analysis; Bayesian Model Updating with Real Measurements; Generalized Damage Diagnosis Across Similar Structures (federated learning appears as an alternative approach). The bridge case ends its results with the bilinear temperature relationship; residual analysis is omitted. Its Home and Work cards retain the earlier twin-bridge overview photograph.
- The temperature-normalization study (lattice mast, IWSHM 2025) is listed under Other Work rather than in the diagnosis case study.
- US English. Titles, headings, labels, and buttons use title case (`title_case()` in `scripts/generate_content.py` applies the same rule to publication titles); body text uses normal sentence case.
- JCSHM paper: accepted, without the unverified DOI. JRUE-B paper: 2025, 11(1), 011105.
- IWSHM Best Paper is attached to the federated-learning paper and identified as coauthored work. The simulation case emphasizes Guofeng’s contributions, with full authorship retained in the publication references. Stress-based initiation uses the defense pit/stress example and criteria comparison; one combined CNN–GP-NARX workflow precedes the physics-constrained model. The crack-initiation figures are compact, with equal physical-domain sizes in the morphology/stress comparison.
- Figure provenance is in `data/media-sources.json`; credits also appear in the visible captions.
- The confidential LPI field-diagnostics case study is parked in `_drafts/bridge-field-diagnostics/` (Quarto ignores folders that start with an underscore) until more information can be added. The teaching case uses original explanatory SVGs and two credited equipment photographs. Raw teaching files, student data, solutions, and photos requiring permission are excluded.
- No portrait was supplied; the hero uses a real bridge photograph from the approved presentation.

## Current plan and deployment

The content plan is maintained in the sibling `../plan/` folder in the original workspace. It records the implemented pages, source evidence, presentation decisions, and maintenance status.

The website was published to GitHub Pages on October 26, 2026. `main` contains the source; `gh-pages` contains the rendered public site. The configured public address is `https://g3qian.github.io/`. Stop an active preview, render, and run the site audit before publishing future changes. Unpublished drafts and raw supporting material remain outside the public repository.

## Verification

The latest local verification is recorded in `data/verification.json`. The October 2026 source review checked project claims and captions against the relevant papers, dissertation, and slides, then rebuilt the eleven pages and reviewed responsive layouts at 390, 768, and 1440 px. The CV was regenerated with the corrected local-benchmark wording and rendered for visual inspection. External DOI checks in `data/doi-checks.json` retain their own check dates; they are separate from this review.

The model-updating case separates synthetic-image development from real laser-scan observations, then shows the experimental posterior distributions before the held-out forecast.

Key distinctions to preserve: 101 versus 674 counts local reliability benchmark evaluations; −11% versus +51% describes the 95th-percentile pit-opening radius; four-second inference and smaller posterior standard deviations come from the separate image-based benchmark. See `../plan/02-project-map.md` for source locations.
