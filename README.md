# Nomography for mineral processing — scripts and verification (release v1.1)

This repository contains the Python scripts used to generate the nomograms of the article
*Reproducible nomogram-based tools for rapid analysis and design of mineral processing operations*
(Minerals, MDPI; manuscript minerals-4630640), together with the code used to assess their accuracy.

## Contents

| Script | Nomogram (article figure) | Equation | Construction |
|---|---|---|---|
| `Law_of_Bond_Nomogram.py` | Bond's law (Figs. 3, 9) | Eq. (1) | PyNomo Type 1 + Type 2 (+ Type 2/8 metric scales) |
| `Modified_Hogg_Fuerstenau_Nomogram.py` | Modified Hogg & Fuerstenau mill power (general chart) | Eq. (2) | PyNomo Type 3 (+ Type 8, D in m) |
| `Modified_Hogg_Fuerstenau_Figure5.py` | Same chart with the example of Fig. 5 (Pnet unknown: 3213 kW) | Eq. (2) | PyNomo Type 3 (+ Type 8) |
| `Modified_Hogg_Fuerstenau_Figure11.py` | Same chart with the sizing example of Fig. 11 (D unknown: 23.27 ft) | Eq. (2) | PyNomo Type 3 (+ Type 8) |
| `Circulating_Load_Nomogram.py` | Circulating load (Fig. 6) | Eq. (3) | PyNomo Type 9 (S2–S3 grid) |
| `Azzaroni_Nomogram.py` | Azzaroni make-up ball size (Fig. 7) | Eq. (4) | PyNomo Type 3 (+ Type 8, D in m) |
| `Valuable_Recovery_Nomogram.py` | Two-product recovery (Fig. 8) | Eq. (5) | Nomogen (Type 9) |
| `Mill_Speed_Nomogram.py` | Mill speed (Fig. A1) | Eq. (A.1) | PyNomo Type 2 (+ Type 8) |
| `Apparent_Mill_Charge_Density_Nomogram.py` | Apparent charge density (Figs. 10, A2) | Eq. (A.5), f_sv = 0.50 | PyNomo Type 10 |
| `Mill_Weight_Percentage_of_Solids_Nomogram.py` | Slurry density (Fig. A3) | Eq. (A.6) | Nomogen (Type 9) |
| `Mill_Volume_Percentage_of_Solids_Nomogram.py` | Volume % solids (Fig. A4) | Eq. (A.7) | Nomogen (Type 9) |
| `Mill_Weight_of_Solids_in_a_Litre_Nomogram.py` | Solids per litre (Fig. A5) | Eq. (A.8) | Nomogen (Type 9) |
| `verify_nomograms.py` | Accuracy assessment (Table 4) | — | — |
| `Example_Bond_Mill Sizing.xlsx` | Moly-Cop Tools™ v3.02 Ball Mill Sizing, original example (D = 24 ft) | — | — |
| `Example_Bond_Mill Sizing_D23.3ft.xlsx` | Same spreadsheet evaluated for the graphically sized mill (D = 23.3 ft; Fig. 12) | — | — |
| `pdf/` | Vector PDFs regenerated from the revised scripts (before annotation) | — | — |

## Changes in v1.1 (revision R1 of the article)

* `Modified_Hogg_Fuerstenau_Nomogram.py`: the scales now implement Eq. (2) of the article exactly,
  `Pnet = 0.267 · D^3.5 · (L/D) · Nc · ρap · (Jc − Jc²) · sin α`.
  The previous version had been generated with an earlier calibration of the model
  (`0.238` and `Jc − 1.065·Jc²`), which gives powers about 14 % lower (diameters about 4 % larger)
  than Eq. (2). Scale ranges now match the published figures (Jc 0.20–0.40, L/D 0.5–2.0, α 25–45°, ρap 2–6 t/m³).
  Two additional scripts draw the worked examples of Figures 5 and 11; all three produce identical scale
  geometry and differ only in the isopleth drawn.
* `Law_of_Bond_Nomogram.py`: the metric scales (kWh/t) now use the correct conversion
  1 kWh/t = 0.90718 kWh/sht. The factor was previously inverted on both metric scales; because both
  scales used the same factor, computed energies were unaffected, but cross-reading between kWh/t
  and kWh/sht was wrong.
* New `verify_nomograms.py` and `verification_results.json` (see below).

## Software versions

Results in the article were obtained with:

* Python 3.13
* PyNomo 0.3.6 with Nomogen, from <https://github.com/tevorbl/pynomo> at commit `dd19620`
* PyX 0.17, NumPy 2.5, SciPy 1.18
* A LaTeX installation (used by PyX for text rendering)

See `requirements.txt`.

## Regenerating the nomograms

```bash
git clone https://github.com/tevorbl/pynomo.git          # PyNomo + Nomogen
cd pynomo && git checkout dd19620 && pip install . && cd ..
pip install -r requirements.txt
python Law_of_Bond_Nomogram.py                            # -> Law_of_Bond_Nomogram.pdf
python Modified_Hogg_Fuerstenau_Nomogram.py               # general chart
python Modified_Hogg_Fuerstenau_Figure5.py                 # example of Fig. 5
python Modified_Hogg_Fuerstenau_Figure11.py                # sizing example of Fig. 11
# Nomogen scripts need the nomogen folder on the Python path:
PYTHONPATH=pynomo/nomogen python Valuable_Recovery_Nomogram.py
```

Each script writes a vector PDF. The figures in the article were annotated afterwards
(titles, legends, worked-example isopleths) in a vector-graphics editor without altering the scale geometry.

## Reproducing the accuracy assessment (Table 4 of the article)

```bash
python verify_nomograms.py . pynomo/nomogen results 2000
```

For every nomogram the script rebuilds the chart, recovers the scale geometry in paper coordinates from the
PyNomo objects, and, for 2000 random input combinations:

1. reproduces the isopleth construction numerically (construction error), and
2. repeats it with Gaussian placement errors of σ = 0.25 mm and 0.5 mm on every input mark, pivot point and
   output reading, at native print size (reading error).

Results are written to `results/verification_results.json` (median, 95th percentile and maximum absolute
relative errors, overall and for the central 60 % of the scales). Random seeds are fixed per chart, so the results reproduce Table 4 of the article exactly.

## Printing

Print each chart at no less than 1.2 × its native size (the `paper_width` × `paper_height` of the script,
in cm) so that the smallest tick labels are ≥ 6 pt; print the Bond chart at about 1.8 × (A4 landscape) and the
mill power chart at about 1.5 × (A3) native size. Reading errors scale approximately inversely with the print scale.

## Licence and citation

Please cite the article and this release (Zenodo DOI: to be added).
