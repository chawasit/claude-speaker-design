# Bibliography

Foundational papers, books, and standards behind the knowledge in
this skill. When Claude needs to cite an authority — or when a user
wants to go deeper than a reference doc — point them here.

## Books (priority reading order)

### 1. Floyd E. Toole — *Sound Reproduction: The Acoustics and Psychoacoustics of Loudspeakers and Rooms* (3rd ed., Routledge, 2017)

The single best reference on what makes a loudspeaker sound good and
why. Synthesizes decades of psychoacoustic research at the Canadian
NRC and Harman. Topics: spinorama, listener preference, room
correction, target curves, multichannel.

**If you read one book, read this one.**

### 2. Vance Dickason — *The Loudspeaker Design Cookbook* (8th ed., 2024)

The DIY engineer's working reference. T/S parameter measurement,
enclosure alignment tables, crossover design with real driver data,
materials, construction. More practical and less theoretical than
Toole; perfectly complementary.

### 3. Leo L. Beranek — *Acoustics: Sound Fields and Transducers* (2nd ed., with Tim Mellow, Academic Press, 2012)

The mathematical foundation. Wave equation, radiation impedance,
transducer theory, room acoustics. Heavier than Toole and Dickason;
the reference when you need the actual derivation.

### 4. Earl R. Geddes — *Audio Transducers* (Gedlee LLC, 2002)

The horn / waveguide designer's reference. Oblate spheroidal
geometry, higher-order modes, distortion analysis. Geddes' design
philosophy underpins modern "audiophile-CD" speakers like Summa.

### 5. Harry F. Olson — *Acoustical Engineering* (Van Nostrand, 1957)

The classical reference. Olson's diffraction curves, horn theory,
moving-coil driver analysis. Pre-T/S, but the underlying physics
hasn't changed.

### 6. Robert M. Bullock III — *Bullock on Loudspeakers* (Audio
Amateur, 1991)

Compilation of Bullock's *Speaker Builder* articles. Practical
crossover design with worked examples; T/S-based enclosure design.

## Foundational papers

### Driver modeling (Thiele/Small theory)

- **Thiele, A. N.**, "Loudspeakers in Vented Boxes," *J. Audio Eng.
  Soc.*, **19**:382–392, 471–483 (1971). The original T/S paper for
  vented boxes.
- **Small, R. H.**, "Direct-Radiator Loudspeaker System Analysis,"
  *J. Audio Eng. Soc.*, **20**:383–395 (1972). Closed-box
  analysis.
- **Small, R. H.**, "Vented-Box Loudspeaker Systems Parts I-IV,"
  *J. Audio Eng. Soc.*, **21**:363–372, 438–444, 549–554, 635–639
  (1973). The tabulated B4/QB3/C4 alignments used in this skill's
  `tools/ported_box.py`.
- **Small, R. H.**, "Closed-Box Loudspeaker Systems Parts I-II,"
  *J. Audio Eng. Soc.*, **20**:798–808, 21:11–18 (1972, 1973).
- **Margolis, G. and Small, R. H.**, "Personal Calculator Programs
  for Approximate Vented-Box and Closed-Box Loudspeaker System
  Design," *J. Audio Eng. Soc.*, **29**:421–441 (1981).

### Large-signal driver behavior

- **Klippel, W.**, "Tutorial: Loudspeaker Nonlinearities — Causes,
  Parameters, Symptoms," *J. Audio Eng. Soc.*, **54**:907–939
  (2006). Foundation of modern nonlinear driver characterization.

### Crossover design

- **Linkwitz, S. H.**, "Active Crossover Networks for
  Noncoincident Drivers," *J. Audio Eng. Soc.*, **24**:2–8 (1976).
  The Linkwitz-Riley crossover origin.
- **Linkwitz, S. H.**, "Passive Crossover Networks for
  Noncoincident Drivers," *J. Audio Eng. Soc.*, **26**:149–150
  (1978).
- **Lipshitz, S. P., Pocock, M. and Vanderkooy, J.**, "On the
  Audibility of Midrange Phase Distortion in Audio Systems," *J.
  Audio Eng. Soc.*, **30**:580–595 (1982). Why phase usually
  doesn't matter much; an evidence-based foundation for
  minimum-phase design.

### Horns and waveguides

- **Webster, A. G.**, "Acoustic Impedance and the Theory of Horns
  and the Phonograph," *Proc. National Academy of Sciences*,
  **5**:275–282 (1919). The original horn equation.
- **Salmon, V.**, "A New Family of Horns," *J. Acoustical Soc.
  Am.*, **17**:212–218 (1946). Hyperbolic-exponential family.
- **Geddes, E. R.**, "Acoustic Waveguide Theory," *J. Audio Eng.
  Soc.*, **37**:554–569 (1989). Oblate-spheroidal waveguide.
- **Keele, D. B.**, "What's So Sacred About Exponential Horns,"
  AES Preprint 1038 (1975). Constant-directivity horn theory.

### Diffraction and baffle

- **Olson, H. F.**, "Direct Radiator Loudspeaker Enclosures," *J.
  Audio Eng. Soc.*, **17**:22–29 (1969). The Olson curves cited in
  `baffle-and-cabinet-acoustics.md`.

### Room acoustics

- **Schroeder, M. R.**, "Frequency Correlation Functions of
  Frequency Responses in Rooms," *J. Acoustical Soc. Am.*,
  **34**:1819–1823 (1962). Schroeder frequency.
- **Schroeder, M. R.**, "Diffuse Sound Reflection by Maximum-Length
  Sequences," *J. Acoustical Soc. Am.*, **57**:149–150 (1975).
  The QRD diffuser.
- **Allen, J. B. and Berkley, D. A.**, "Image Method for Efficiently
  Simulating Small-Room Acoustics," *J. Acoustical Soc. Am.*,
  **65**:943–950 (1979). The image-source method used in many room
  simulators.

### Listener preference and target curves

- **Toole, F. E. and Olive, S. E.**, "The Modification of Timbre by
  Resonances: Perception and Measurement," *J. Audio Eng. Soc.*,
  **36**:122–142 (1988). What spectral features listeners detect.
- **Olive, S. E.**, "A Multiple Regression Model for Predicting
  Loudspeaker Preference Using Objective Measurements," AES
  Preprint 6190 (2004). The "what makes a speaker preferred"
  predictor.
- **Olive, S. E., et al.**, "The Influence of Listening Room on
  Loudspeaker Sound Quality," AES Preprint 5750 (2003). Room's
  contribution to listener preference.
- **Olive, S. E.**, "The Relationship Between Perception and
  Measurement of Headphone Sound Quality," AES Preprints (2013,
  2017). Harman headphone target.

### Multi-subwoofer

- **Welti, T. and Devantier, A.**, "Low-Frequency Optimization Using
  Multiple Subwoofers," *J. Audio Eng. Soc.*, **54**:347–364
  (2006). The mid-wall multi-sub configuration.

### Constant Beamwidth Transducer

- **Keele, D. B. Jr.**, "The Application of Broadband Constant
  Beamwidth Transducer (CBT) Theory to Loudspeaker Arrays," AES
  Preprint 5683 (2002).
- **Keele, D. B. Jr.**, "Implementation of Straight-Line and
  Flat-Panel Constant Beamwidth Transducer (CBT) Loudspeaker
  Arrays Using Signal Delays," AES Preprint 5990 (2003).

### Stereo imaging

- **Blauert, J.**, *Spatial Hearing: The Psychophysics of Human Sound
  Localization* (MIT Press, 1997). The standard reference on
  binaural localization.

## Standards documents

- **CTA-2034-A** (2021): Loudspeaker Standard Method of
  Measurement. Successor to CEA-2034 (2013).
- **IEC 60268-1 to -5**: Sound system equipment. Various aspects of
  loudspeaker spec and measurement.
- **AES2-2012**: Recommended Practice for Specification of
  Loudspeaker Components Used in Professional Audio and Sound
  Reinforcement.
- **ISO 226 (2003)**: Acoustics — Normal equal-loudness-level
  contours.
- **ITU-R BS.1116-3** (2015): Methods for the subjective assessment
  of small impairments in audio systems including multichannel
  sound systems.
- **ITU-R BS.775-3** (2012): Multichannel stereophonic sound
  systems with and without accompanying picture (the 5.1
  loudspeaker layout standard).
- **ITU-R BS.1770-4** (2015): Algorithms to measure audio programme
  loudness (LUFS).
- **AES56-2008**: Sound system equipment — On-axis stationary loudness
  measurement methods.

## Web resources

- **https://www.audiosciencereview.com/forum** — Independent measurement
  and review forum; runs CTA-2034-style spinorama on commercial
  speakers.
- **https://spinorama.org** — Aggregator of public spinorama data,
  with score rankings and graphs.
- **https://www.linkwitzlab.com** — Siegfried Linkwitz's site;
  open-baffle dipole and active-speaker design references.
- **https://www.diyaudio.com** — Large DIY speaker forum; archives
  going back to ~1999.
- **https://www.audioxpress.com** — *Voice Coil* and *audioXpress*
  magazines; engineering articles.
- **https://www.harman.com/research** — Harman International's
  research publications; many of Olive's papers.
- **https://www.aes.org/e-lib/** — AES E-Library; archived JAES and
  AES preprints (paywalled but extensive).

## Open-source tools mentioned

- **REW (Room EQ Wizard)** — `https://www.roomeqwizard.com`
- **VituixCAD** — `https://kimmosaunisto.net`
- **Hornresp** (David McBean) — distributed via diyaudio thread
- **ATH4 (Mabat)** — `https://github.com/thedigitalapprentice/ath`
- **Akabak** — `https://www.akabak.org`
- **MSO (Multi-Sub Optimizer)** — `https://www.andyc.diy-audio-engineering.org`
- **pyroomacoustics** — `https://github.com/LCAV/pyroomacoustics`
- **k-Wave** — `https://www.k-wave.org`

## Reading paths

**"I want to build my first speaker"**: Dickason 1, 4, 7, 8 →
Bullock crossover articles → Toole chapters 4-5.

**"I want to design a horn-loaded system"**: Geddes book →
Salmon paper → Webster paper → ATH4 docs.

**"I want to optimize my listening room"**: Toole book chapters
8-13 → Welti & Devantier → Allen-Berkley.

**"I want to do measurements properly"**: AES2-2012 → CTA-2034-A
→ Klippel tutorial → REW documentation.

**"I want to model speakers in software"**: T/S original papers →
Beranek/Mellow → Hornresp + Akabak docs.
