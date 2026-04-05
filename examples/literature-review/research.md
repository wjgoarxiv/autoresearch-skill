# Research: Morning vs Evening Exercise Effectiveness

## Goal
Conduct a systematic literature review to determine whether morning or evening exercise is more effective across multiple health and fitness outcomes. Build a comprehensive taxonomy covering 8 outcome categories with sufficient evidence depth (>=2 papers each).

## Success Metric
- **Metric:** Taxonomy coverage (8 categories, each needs >=2 papers)
- **Target:** 8/8 categories covered (100%)
- **Direction:** maximize

## Constraints
- **Max iterations:** 6
- **Evaluator:** _(none — agent judges manually via taxonomy coverage count)_
- **Keep policy:** score_improvement
- **Min delta:** 1
- Publication types: RCTs, meta-analyses, systematic reviews, prospective cohort studies
- Language: English only
- Sources: PubMed, Google Scholar, Semantic Scholar
- Minimum 2 papers per taxonomy category to count as "covered"

## Current Approach
Starting from 3 known meta-analyses as seed references:
1. Bruggisser et al. (2023) "Best Time of Day for Strength and Endurance Training" -- Sports Medicine Open
2. Sevilla-Lorente et al. (2023) "Effects of Time-of-Day on Blood Pressure" -- JSAMS
3. Chtourou & Souissi (2012) "Effect of Training at a Specific Time of Day" -- JSCR

Initial taxonomy coverage:
- **Muscle Performance:** Bruggisser 2023, Chtourou 2012 (2 papers -- COVERED)
- **Cardiovascular Health:** Sevilla-Lorente 2023 (1 paper -- needs more)
- **Weight/Fat Loss:** 0 papers -- gap
- **Hormonal Response:** 0 papers -- gap
- **Sleep Quality:** 0 papers -- gap
- **Metabolic Health:** 0 papers -- gap
- **Circadian Rhythm:** 0 papers -- gap
- **Adherence & Consistency:** 0 papers -- gap

**Final taxonomy coverage (Iteration 4):**
- **Weight/Fat Loss:** 3 papers -- COVERED
- **Muscle Performance:** 2 papers -- COVERED
- **Cardiovascular Health:** 2 papers -- COVERED
- **Hormonal Response:** 3 papers -- COVERED
- **Sleep Quality:** 2 papers -- COVERED
- **Metabolic Health:** 2 papers -- COVERED
- **Circadian Rhythm:** 2 papers -- COVERED
- **Adherence & Consistency:** 3 papers -- COVERED
- **Total:** 19 unique papers, 8/8 categories met

## Search Space
- **Allowed changes:** Search queries, source databases, taxonomy category refinement, inclusion/exclusion criteria
- **Forbidden changes:** Minimum 2-paper threshold per category, 8-category taxonomy structure, language requirement (English)

## Taxonomy Categories
1. **Weight/Fat Loss** -- Body composition, fat oxidation, weight reduction outcomes
2. **Muscle Performance** -- Strength, hypertrophy, power, maximal exercise capacity
3. **Cardiovascular Health** -- Blood pressure, heart rate, vascular function
4. **Hormonal Response** -- Cortisol, testosterone, growth hormone, insulin
5. **Sleep Quality** -- Sleep onset, duration, architecture, disturbance
6. **Metabolic Health** -- Insulin sensitivity, glucose tolerance, metabolic syndrome markers
7. **Circadian Rhythm** -- Chronotype interactions, peripheral clock entrainment, phase shifts
8. **Adherence & Consistency** -- Habit formation, long-term compliance, dropout rates

## Context & References
- Exercise timing research has accelerated since 2019 with wearable-derived data
- Key confound: most studies do not control for chronotype
- "Temporal congruence effect" -- training at a consistent time matters more than which time
- Sex-specific differences emerging as major finding (Arciero 2022, Scientific Reports 2025)

---

## Paper Catalog

### 1. Weight/Fat Loss
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Arciero et al. | 2022 | Morning Exercise Reduces Abdominal Fat and Blood Pressure in Women; Evening Exercise Increases Muscular Performance in Women and Lowers Blood Pressure in Men | Morning exercise reduced abdominal fat (-2.6 kg vs -0.9 kg) in women; sex-specific effects |
| 2 | Brooker et al. | 2023 | The efficacy of morning versus evening exercise for weight loss: A randomized controlled trial | No significant difference; morning -2.7 kg vs evening -3.1 kg; consistency matters more than timing |
| 3 | Lan et al. | 2025 | Morning vs. evening: the role of exercise timing in enhancing fat oxidation in young men | Morning fasting exercise showed superior acute fat oxidation; evening exercise enhanced next-morning fat oxidation |

### 2. Muscle Performance
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Bruggisser et al. | 2023 | Best Time of Day for Strength and Endurance Training | Meta-analysis: evening training marginally better for strength/power outcomes |
| 2 | Chtourou & Souissi | 2012 | Effect of Training at a Specific Time of Day | Review: peak muscle performance in evening aligns with core body temperature peak |

### 3. Cardiovascular Health
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Sevilla-Lorente et al. | 2023 | Time of the day of exercise impact on cardiovascular disease risk factors in adults: a systematic review and meta-analysis | Meta-analysis: no significant difference between morning vs evening for BP or glucose |
| 2 | Brito et al. | 2019 | Morning versus Evening Aerobic Training Effects on Blood Pressure in Treated Hypertension | Evening training reduced 24h and asleep diastolic BP; decreased vascular resistance |

### 4. Hormonal Response
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Hayes et al. | 2010 | Interactions of cortisol, testosterone, and resistance training: influence of circadian rhythms | Evening has more favorable T/C ratio; morning cortisol may counteract testosterone benefits |
| 2 | Bird & Tarpenning | 2004 | Influence of circadian time structure on acute hormonal responses to heavy-resistance exercise | Evening exercise produced lower cortisol and better T/C ratio for muscle building |
| 3 | Kuusmaa et al. | 2016 | Effects of morning versus evening combined strength and endurance training on physical performance, muscle hypertrophy, and serum hormone concentrations | Diurnal rhythms in T and C remained unaltered by training time; evening groups gained more muscle after 12 weeks |

### 5. Sleep Quality
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Kim et al. | 2023 | Effects of exercise timing and intensity on physiological circadian rhythm and sleep quality: a systematic review | Evening exercise did not impair sleep quality but altered circadian rhythm; morning reduced cortisol |
| 2 | Yue et al. | 2022 | Different Intensities of Evening Exercise on Sleep in Healthy Adults: A Systematic Review and Network Meta-Analysis | Acute evening exercise before bedtime does not disrupt sleep; moderate intensity may improve sleep efficiency |

### 6. Metabolic Health
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Morales-Palomo et al. | 2023 | Efficacy of morning versus afternoon aerobic exercise training on reducing metabolic syndrome components: A randomized controlled trial | Morning exercise reduced MetS Z-score by 52% vs 19% afternoon; better insulin sensitivity |
| 2 | Moholdt et al. | 2021 | The effect of morning vs evening exercise training on glycaemic control and serum metabolites in overweight/obese men: a randomised trial | Evening exercise improved glycaemic control and reversed HFD-induced metabolic changes; morning did not |

### 7. Circadian Rhythm
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Thomas et al. | 2020 | Circadian rhythm phase shifts caused by timed exercise vary with chronotype | Morning exercise induced 0.62h phase advance; effects depend on chronotype |
| 2 | Shen et al. | 2023 | Effects of exercise on circadian rhythms in humans | Exercise upregulates BMAL1/PER2 in skeletal muscle; non-photic zeitgeber for clock entrainment |

### 8. Adherence & Consistency
| # | Authors | Year | Title | Key Finding |
|---|---------|------|-------|-------------|
| 1 | Schumacher et al. | 2023 | Consistent exercise timing as a strategy to increase physical activity: A feasibility study | Prescribed morning/evening timing produced more MVPA than self-choice; 69.9% timing adherence |
| 2 | Back et al. | 2022 | Evening chronotype predicts dropout of physical exercise: a prospective analysis | Evening chronotypes had 2.22x higher dropout risk; 68.2% vs 35.4% dropout rate |
| 3 | Brooker et al. | 2022 | How do previously inactive individuals restructure their time to fit in morning or evening exercise | No difference in time restructuring between morning/evening; both displaced screen time |

---

## History
<!-- Auto-maintained by the agent. Do not edit manually. -->
| # | Search Strategy | Papers Found | Coverage | Result | Timestamp |
|---|----------------|-------------|----------|--------|-----------|
| 0 | Seed: 3 known meta-analyses (Bruggisser 2023, Sevilla-Lorente 2023, Chtourou 2012) | 3 | 1/8 (12.5%) | baseline | 2026-04-05 |
| 1 | Weight/Fat Loss + Cardiovascular: "morning vs evening exercise fat loss body composition" + "exercise timing blood pressure cardiovascular" | 4 new (Arciero 2022, Brooker 2023, Lan 2025, Brito 2019) | 3/8 (37.5%) | +2 categories | 2026-04-05 |
| 2 | Hormonal + Sleep: "cortisol testosterone resistance exercise morning evening diurnal" + "evening exercise sleep quality systematic review" | 5 new (Hayes 2010, Bird 2004, Kuusmaa 2016, Kim 2023, Yue 2022) | 5/8 (62.5%) | +2 categories | 2026-04-05 |
| 3 | Metabolic + Circadian: "morning vs evening exercise insulin glucose metabolic syndrome" + "exercise timing chronotype circadian phase shift" | 4 new (Morales-Palomo 2023, Moholdt 2021, Thomas 2020, Shen 2023) | 7/8 (87.5%) | +2 categories | 2026-04-05 |
| 4 | Adherence: "exercise timing adherence morning dropout compliance" + "evening chronotype exercise dropout" | 3 new (Schumacher 2023, Back 2022, Brooker 2022) | 8/8 (100%) | TARGET MET | 2026-04-05 |
