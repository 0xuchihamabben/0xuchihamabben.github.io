---
title: "PMW–Bernstein: Privacy Engineering for Adaptive Data Analysis"
date: 2026-08-24 18:00:00 +0200
categories: [Research, Privacy]
tags: [differential-privacy, privacy-engineering, pmw, healthcare]
description: >-
  The research question, mechanism, and update guarantees behind my
  variance-adaptive refinement of Private Multiplicative Weights.
author: mabben
toc: true
math: true
---

Privacy engineering becomes difficult when analysis is interactive. A researcher asks one question, studies the result, and chooses the next question based on what was learned. The sequence itself can reveal information even when every individual answer looks harmless in isolation.

My final-year project studies this problem through **Private Multiplicative Weights (PMW)**. The project asks whether a step size adapted to the current query error and hypothesis variance can improve the progress made on difficult rounds.

The complete paper and source artifact are available in the [PMW–Bernstein repository](https://github.com/0xuchihamabben/pmw-bernstein).

## The interactive setting

Let $$p$$ represent the empirical distribution of a private dataset. At round $$t$$, PMW maintains a public hypothesis distribution $$h_t$$ and receives a normalized linear query $$q_t : \mathcal X \rightarrow [0,1]$$.

The hypothesis and private-data answers are

$$
\mu_t = \mathbb E_{h_t}[q_t], \qquad a_t = \mathbb E_p[q_t].
$$

Their absolute discrepancy and the query variance under the current hypothesis are

$$
e_t = |\mu_t-a_t|, \qquad v_t = \mathrm{Var}_{h_t}(q_t).
$$

PMW answers from the public hypothesis when it is sufficiently accurate. On a difficult round, it obtains a private numerical answer and updates the hypothesis.

That separation matters operationally: inexpensive public answers should handle easy rounds, while the limited privacy budget is reserved for corrections.

## The variance-adaptive step

The numerical mechanism produces an estimate $$\widehat e_t$$ of the current error. The proposed update uses

$$
\eta_t = \log\!\left(1+\frac{\widehat e_t}{v_t}\right).
$$

The expression adapts to two local properties:

- a larger estimated discrepancy asks for a stronger correction;
- a larger variance makes an aggressive exponential reweighting more costly.

The project does not claim that adaptivity alone creates a privacy improvement. The privacy mechanisms and their composition remain explicit and separate from the potential argument. The adaptive step instead targets utility: how much progress the public hypothesis makes each time private information is spent on an update.

## Mechanism architecture

Each round has four relevant stages:

1. Compute the public hypothesis prediction and variance.
2. Use a differentially private Sparse Vector screen to classify the round.
3. Publish the hypothesis answer on an easy round.
4. On a difficult round, publish a Gaussian-perturbed numerical answer and update the hypothesis.

The mechanism also includes a hard cutoff on difficult rounds. This is not an implementation footnote. The cutoff connects the promised privacy budget to the transcript that the mechanism is actually allowed to publish.

> Privacy accounting, stopping behavior, and the public transcript must describe the same mechanism.
{: .prompt-info }

## Measuring progress

The analysis uses the Kullback–Leibler divergence

$$
\Phi_t = \mathrm{KL}(p\|h_t)
$$

as a potential function. For the idealized true error, the step

$$
\eta_t^\star = \log\!\left(1+\frac{e_t}{v_t}\right)
$$

is the unique maximizer of the derived variance-sensitive lower bound.

The private mechanism cannot use $$e_t$$ directly, so it substitutes $$\widehat e_t$$. When the estimate has the correct direction and satisfies the relative-accuracy condition

$$
\widehat e_t \in \left[\frac{e_t}{2},\frac{3e_t}{2}\right],
$$

the one-step potential decrease obeys

$$
\Phi_t-\Phi_{t+1} \geq \frac{3}{8}\frac{e_t^2}{v_t+e_t}.
$$

Summing over update rounds $$U$$ gives the weighted-energy bound

$$
\sum_{t\in U}\frac{e_t^2}{v_t+e_t}
\leq \frac{8}{3}\mathrm{KL}(p\|r),
$$

where $$r=h_1$$ is the public full-support prior.

## Two update regimes

Without an additional relationship between variance and error, the analysis recovers an update count with the familiar quadratic dependence on the target accuracy $$\alpha$$:

$$
|U| \leq \frac{40}{3}\frac{\mathrm{KL}(p\|r)}{\alpha^2}.
$$

Under the local Bernstein-type relation

$$
v_t \leq B e_t,
$$

the count improves to

$$
|U| \leq \frac{16}{3}(B+1)\frac{\mathrm{KL}(p\|r)}{\alpha}.
$$

The fast regime is therefore conditional, not universal. Its value is that it identifies a precise local structure under which the mechanism can make stronger progress.

## Why healthcare motivates the question

Healthcare analysis often involves repeated aggregate questions about cohorts, diagnoses, outcomes, treatments, or rare events. These questions are naturally adaptive: one result determines the next subgroup or hypothesis worth investigating.

Indicator queries provide a useful example. If $$q_t=\mathbf 1_A$$ for an event $$A$$, then

$$
v_t=\mu_t(1-\mu_t)\leq\mu_t.
$$

When an event is underrepresented by the current public hypothesis relative to the private empirical distribution, this structure can connect rare-event analysis to the local Bernstein condition.

The theoretical model does not replace deployment work. A real system still needs careful query governance, contribution bounds, privacy-budget ownership, monitoring, and an interpretation of what happens when the cutoff is reached.

## What the artifact provides

The repository contains:

- the complete paper;
- the formal mechanism and privacy statement;
- the one-step and global potential analysis;
- the noise calibration and non-exhaustion conditions;
- a concise project README for readers entering from GitHub.

[Open the PMW–Bernstein project](https://github.com/0xuchihamabben/pmw-bernstein){: .btn .btn-outline-primary }

The broader lesson extends beyond this mechanism: a privacy claim becomes more credible when the algorithm, accounting, stopping rule, accuracy event, and published artifact agree on the exact system being analyzed.
