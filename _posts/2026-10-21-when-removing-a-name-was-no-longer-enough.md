---
title: "When Removing a Name Was No Longer Enough"
date: 2026-10-21 19:24:48 +0200
categories: [Privacy, Foundations]
tags: [differential-privacy, anonymization, healthcare, history]
description: >-
  An introduction to differential privacy: how record linkage, attribute
  disclosure, and reconstruction exposed the limits of classic anonymization.
author: mabben
toc: true
math: true
pin: true
image:
  path: /assets/img/posts/differential-privacy-introduction/privacy-header.png
  alt: Medical records and individual silhouettes give way to an aggregate cloud of statistical patterns.
---

*My journey into privacy-preserving data analysis, from medical-record anonymization to differential privacy.*

There is something deeply uncomfortable about the amount of information a hospital knows about a person. A medical record can contain years of diagnoses, medications, laboratory results, and details that a patient has never shared outside a consultation room.

That information also has enormous research value. Patterns across many patients can help researchers understand diseases, evaluate treatments, and ask better questions.

The tension is easy to state: **how do we learn from sensitive information without exposing the people who provided it?**

My final-year research at the École Nationale Supérieure d'Informatique (ESI) explored a variance-adaptive refinement of Private Multiplicative Weights, a mechanism for answering repeated statistical queries under differential privacy. Before getting into that work, I want to explain the problem that makes such mechanisms necessary.

The natural starting point is a deceptively simple idea: remove the patient's name.

## A record can identify someone without naming them

Imagine a hospital removing names, phone numbers, and patient identifiers before sharing a table with researchers. The remaining columns include dates of birth, postal codes, sex, and diagnoses.

The table looks anonymous. But an outside directory might contain names alongside the same demographic attributes. A distinctive combination can connect a row in one table to a person in the other. Attributes with this linking potential are called **quasi-identifiers**.

Latanya Sweeney demonstrated the problem using Massachusetts health-insurance data and a Cambridge voter-registration list. In her account, the combination of birth date, sex, and ZIP code singled out then-governor William Weld and linked him to his medical information. The medical release did not need a name column for that association to become possible.[^sweeney]

![An invented medical record and public directory share a birth date, postal code, and sex; if the combination is unique, a name can be linked to a diagnosis.](/assets/img/posts/differential-privacy-introduction/record-linkage.png)
_Figure 1. All values are invented. Linkage depends on the available information and how distinctive the shared attributes are._

Removing direct identifiers is still useful. The mistake is treating their absence as proof that nobody can be identified. The risk depends on what remains and what an observer can combine it with.

## Making records less precise

One response is to reduce detail. Replace an exact age with an age band, a postal code with a larger region, or an admission date with a month. This is **generalization**. Removing revealing values or records is **suppression**.

These transformations create a practical trade-off. Broad age bands can obscure age-related patterns. Suppressing rare diagnoses can remove the cases a researcher most wants to study.

Statistical disclosure control has a long history, including techniques such as rounding and perturbation. The difficult question has always been how much useful information a release can retain while providing a defensible level of protection.

### k-anonymity: hiding among similar records

Work by Pierangela Samarati and Latanya Sweeney in the late 1990s, followed by Sweeney's 2002 paper, gave an influential formal condition: **k-anonymity**. For selected quasi-identifiers, each released record must share its values with at least $$k-1$$ other records.[^sweeney]

For example, consider this invented release:

| Age band | Region | Diagnosis |
|---|---|---|
| 40–49 | North | Condition X |
| 40–49 | North | Condition X |
| 40–49 | North | Condition X |

With age band and region as the chosen quasi-identifiers, these rows form a group of three. That group meets the corresponding 3-anonymity condition.

But suppose an observer knows that a particular patient is represented in this group. Every row has the same diagnosis. The observer can infer the diagnosis without identifying the patient's exact row.

This is an example of **attribute disclosure**, often called a homogeneity attack in this setting. Uncertainty about which record belongs to someone does not necessarily create uncertainty about their sensitive information.[^ldiversity]

### ℓ-diversity and t-closeness: stronger conditions

In 2006, Ashwin Machanavajjhala and colleagues introduced **ℓ-diversity**, requiring suitably represented sensitive values within each group. It addresses the simple case in which all members share one diagnosis. Its protection depends on the particular definition of diversity; merely counting distinct values can miss important skew or similarities between diagnoses.[^ldiversity]

In 2007, Ninghui Li, Tiancheng Li, and Suresh Venkatasubramanian proposed **t-closeness**. It constrains the distance between a sensitive attribute's distribution within a group and its distribution across the released table.[^tcloseness]

These approaches made the problem more precise. They also left difficult engineering choices: which attributes to treat as identifying, what an observer might already know, and how several releases interact.

The dates matter here. These research directions overlapped: ℓ-diversity appeared in the same year as differential privacy, and t-closeness followed it.

## Aggregate answers can expose individuals too

Perhaps the hospital should keep the records private and release only statistics.

Consider a hypothetical query service that permits both of these exact questions:

| Query | Answer |
|---|---:|
| How many patients in this cohort have Condition X? | 23 |
| How many have Condition X, excluding Alice? | 22 |

If the observer can target Alice in that cohort, subtraction reveals her condition status. This is a **differencing attack**. Keeping individual rows hidden has not prevented a disclosure through the answers.

The broader risk goes beyond two queries. In 2003, Irit Dinur and Kobbi Nissim showed how sufficiently accurate answers to many subset-sum queries can enable reconstruction in their statistical-database model.[^reconstruction]

The result exposed a fundamental tension: releasing many highly accurate statistics about the same people can reveal far more than any single answer suggests.

## Randomness was part of the story long before DP

Differential privacy did not invent randomized protection. In 1965, Stanley Warner introduced **randomized response** for sensitive surveys. A respondent uses a private random procedure, so the interviewer cannot directly interpret an individual answer. With the procedure's probabilities known, researchers can still estimate a population proportion.[^warner]

That is an important precursor: uncertainty at the individual level can coexist with useful statistical information.

Here are a few landmarks in this overlapping history:

| Period | Development | Question it brings into focus |
|---|---|---|
| 1965 | Warner's randomized response | Can randomization protect respondents while preserving population estimates? |
| 1990s | Record-linkage demonstrations | Can outside information reconnect a person to a nameless record? |
| 1998–2002 | Samarati and Sweeney's work on k-anonymity | Can each record blend into a group on selected attributes? |
| 2003 | Dinur–Nissim reconstruction result | What can many accurate aggregate answers reveal together? |
| 2006 | Differential privacy; ℓ-diversity | How can we bound individual influence? How can we address attribute disclosure? |
| 2007 | t-closeness | How much does group membership change the sensitive-attribute distribution? |

## Differential privacy changes the question

In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith published *Calibrating Noise to Sensitivity in Private Data Analysis*, a foundational contribution to differential privacy.[^dwork2006]

The key comparison is between **neighboring datasets**. Here, take two hospital databases that are identical except that one contains a particular patient's contribution and the other does not.

A differentially private mechanism must produce sufficiently similar **output distributions** on those two databases. It limits how much additional evidence the release can provide because that person's data participated.

This gives us a way to reason about the analysis itself, rather than relying on whether a transformed table looks anonymous.

### The definition, without hiding the quantifiers

Let $$M$$ be a randomized analysis, $$D$$ and $$D'$$ neighboring datasets, and $$S$$ any measurable set of possible outputs. The mechanism satisfies **$$(\varepsilon,\delta)$$-differential privacy** if, for every such pair and every such event,

$$
\Pr[M(D)\in S]
\leq e^{\varepsilon}\Pr[M(D')\in S]+\delta.
$$

The probabilities come from the mechanism's randomness. When $$\delta=0$$, this is pure $$\varepsilon$$-differential privacy. Smaller $$\varepsilon$$ imposes a tighter constraint; $$\delta$$ is an additive relaxation that also needs careful selection.[^foundations]

The requirement covers all neighboring pairs and output events. Seeing one reassuring output is not evidence that an algorithm meets it. Neither parameter is simply the probability that a person will be re-identified.

The **privacy unit** is equally important. A patient can contribute many visits and laboratory results. Protecting the addition or removal of one row may protect much less than the addition or removal of that patient's entire contribution.[^nist]

## A small example: a count plus calibrated noise

Suppose each patient contributes at most once to a count. Adding or removing one patient can change that count by at most one: its **sensitivity** is 1.

The Laplace mechanism releases

$$
M(D)=f(D)+Z,
\qquad
Z\sim\operatorname{Laplace}\!\left(0,\frac{\Delta f}{\varepsilon}\right),
$$

where $$\Delta f$$ is the maximum change in the query across neighboring datasets. Calibrating the noise this way gives pure $$\varepsilon$$-DP for this scalar query.[^dwork2006]

For illustration, with sensitivity 1 and $$\varepsilon=0.5$$, the noise has scale 2. A true count of 23 can produce a value above or below 23. **Scale 2 is not a maximum error**: Laplace noise has unbounded tails.

![Two overlapping Laplace probability-density curves centered at counts 22 and 23, representing the same mechanism on neighboring datasets.](/assets/img/posts/differential-privacy-introduction/neighboring-distributions.png)
_Figure 2. One patient changes the true count by one. Both curves use Laplace noise with scale 2. For this mechanism, the likelihood ratio is bounded by $$e^{0.5}$$ in either direction. These parameters illustrate the mathematics; they are not a deployment recommendation._

The curves differ, but their relationship is controlled. That quantitative relationship is what supports the guarantee. Adding an arbitrary amount of noise without analyzing the computation does not establish DP.

The same absolute noise can have very different consequences for utility: a few units may matter little for a count in the thousands and a great deal for a count of four. Privacy protection and statistical usefulness both need evaluation.

## What DP gives us

**A guarantee that accounts for auxiliary information.** The definition does not depend on keeping an observer ignorant of external datasets. It bounds the effect of the protected contribution even when the observer has substantial background knowledge. It cannot erase information that is already known or prevent every inference from population patterns.

**A way to account for repeated releases.** Composition connects the guarantees of several analyses. Under basic sequential composition, mechanisms with parameters $$(\varepsilon_i,\delta_i)$$ have a combined guarantee of at most $$(\sum_i\varepsilon_i,\sum_i\delta_i)$$. Tighter accounting is possible in some settings, but repeated queries still require an overall analysis.

**Protection through post-processing.** Turning a DP output into a chart, summary, or decision, without another access to the private data, preserves its DP guarantee. Further private-data access needs its own accounting.[^foundations]

Together, these properties make privacy something we can reason about across a workflow. If an analyst repeatedly requests fresh, independently noisy versions of the same count, averaging can reduce the noise. A privacy budget is how a system accounts for those releases collectively.

## The guarantee still has boundaries

A proof depends on the mechanism that is actually implemented: contribution bounds, sensitivity, random sampling, query selection, and release accounting all matter. A large privacy parameter can also give weak protection despite formally satisfying the definition. NIST's guidance is a useful reference for evaluating those assumptions in real systems.[^nist]

DP governs disclosure through analysis outputs. A hospital still needs secure infrastructure, access control, encryption, and governance around its raw records. Population-level findings can also affect people who never participated in the data. Bounding individual influence does not settle every ethical question about an analysis.

These limits help explain what a DP guarantee means and where additional protections are needed.

## Why this became my starting point

The history changed how I think about privacy. A missing name, a group of similar rows, and a collection of aggregate answers each address only part of the problem. We also need to understand what a release reveals when combined with other information and future releases.

That is what drew me toward differential privacy and, eventually, Private Multiplicative Weights. Once researchers ask repeated, related questions, the challenge becomes how to learn useful patterns while accounting for the information each interaction reveals.

This first post is the starting point for that discussion. In later articles, I want to examine sensitivity, noise mechanisms, composition, and the ideas behind Private Multiplicative Weights more closely.

For now, the question that stays with me is simple:

**How much can we learn from a population without learning too much about any one person?**

## References and further reading

[^warner]: Stanley L. Warner (1965), [*Randomized Response: A Survey Technique for Eliminating Evasive Answer Bias*](https://pubmed.ncbi.nlm.nih.gov/12261830/).
[^sweeney]: Latanya Sweeney (2002), [*k-Anonymity: A Model for Protecting Privacy*](https://dataprivacylab.org/dataprivacy/projects/kanonymity/kanonymity.pdf). Includes the medical-record linkage example and acknowledges the earlier joint work with Samarati.
[^ldiversity]: Ashwin Machanavajjhala, Johannes Gehrke, Daniel Kifer, and Muthuramakrishnan Venkitasubramaniam (2006), [*ℓ-Diversity: Privacy Beyond k-Anonymity*](https://www.cs.cornell.edu/johannes/papers/2006/2006-icde-publishing.pdf).
[^tcloseness]: Ninghui Li, Tiancheng Li, and Suresh Venkatasubramanian (2007), [*t-Closeness: Privacy Beyond k-Anonymity and ℓ-Diversity*](https://www.cs.purdue.edu/homes/ninghui/papers/t_closeness_icde07.pdf).
[^reconstruction]: Irit Dinur and Kobbi Nissim (2003), [*Revealing Information while Preserving Privacy*](https://doi.org/10.1145/773153.773173).
[^dwork2006]: Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith (2006), [*Calibrating Noise to Sensitivity in Private Data Analysis*](https://www.microsoft.com/en-us/research/publication/calibrating-noise-to-sensitivity-in-private-data-analysis/).
[^foundations]: Cynthia Dwork and Aaron Roth (2014), [*The Algorithmic Foundations of Differential Privacy*](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf), especially Chapters 2–3.
[^nist]: Joseph Near, David Darais, Naomi Lefkovitz, and Gary Howarth (2025), [*Guidelines for Evaluating Differential Privacy Guarantees*, NIST SP 800-226](https://csrc.nist.gov/pubs/sp/800/226/final).
