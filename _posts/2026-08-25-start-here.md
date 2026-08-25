---
title: "Start Here: Building a Reproducible Security Research Practice"
date: 2026-08-25 21:00:00 +0200
categories: [Journal, Research]
tags: [security-research, reproducibility, responsible-disclosure]
description: >-
  What this research blog will publish, the standards behind each technical
  claim, and the boundaries that keep security work useful and responsible.
author: mabben
pin: true
toc: true
---

Security research is easy to dramatize and difficult to document well. A polished screenshot can show that something happened; it rarely explains the assumptions, environment, failed attempts, or evidence needed to decide whether the result matters.

This site exists to close that gap in my own work.

I am **Mohamed Aniss Benstaali**, writing under the handle **Uchiha Mabben**. I use this blog as a public research notebook for cybersecurity, privacy engineering, defensive analysis, and reproducible experimentation.

## What I will publish

The articles here will generally fall into three groups.

### Original investigations

These are question-driven studies: a protocol behavior, an application weakness, a privacy property, a detection hypothesis, or another claim that deserves controlled testing. Each investigation should make its scope and evidence explicit.

### Defensive engineering

Finding a weakness is only half the job. Defensive posts will focus on observability, useful telemetry, detection logic, hardening decisions, and the limits of each mitigation.

### Research notes

Not every useful result needs to become a long paper. Shorter notes will capture lab methods, debugging lessons, tool behavior, and carefully bounded observations that may support later research.

## The standard for a technical claim

A strong article should let a skeptical reader answer five questions:

| Question | What the article should provide |
|---|---|
| What is being claimed? | A precise research question or finding |
| Under which conditions? | Scope, versions, configuration, and threat model |
| What is the evidence? | Logs, traces, measurements, derivations, or artifacts |
| Can it be repeated? | Minimal reproduction steps and expected observations |
| What should defenders do? | Impact, detection opportunities, mitigations, and limitations |

This does not mean every post will be perfect or exhaustive. It means uncertainty should be visible. A negative result, an unstable reproduction, or a limitation is part of the research—not something to hide after the fact.

> Evidence is more valuable when the reader can distinguish observation, interpretation, and speculation.
{: .prompt-tip }

## Research boundaries

The work published here uses controlled laboratories, public datasets, deliberately vulnerable targets, or systems for which testing is explicitly authorized. Sensitive artifacts are sanitized before publication.

For vulnerabilities that could affect real users, publication should follow a coordinated disclosure process. A technical write-up should not create unnecessary risk simply to arrive first.

> Nothing on this site grants permission to test a system you do not own or administer.
{: .prompt-danger }

## Current direction

My final-year project studied a variance-adaptive refinement of **Private Multiplicative Weights**, motivated by repeated statistical analysis over sensitive healthcare data. That work established a useful foundation: define the model, separate guarantees from heuristics, state the event on which a bound holds, and keep the complete artifact available for review.

I am carrying the same discipline into broader security research. The immediate focus is on:

- reproducible application and systems-security labs;
- privacy engineering for sensitive-data workflows;
- detection-oriented interpretations of technical findings;
- small tools whose assumptions and failure modes are documented.

You can follow the growing body of work through the [Research]({% link _tabs/research.md %}) and [Projects]({% link _tabs/projects.md %}) pages.

## Corrections are part of the work

Research improves through review. When a material error is found, I will correct the article and make the change visible rather than quietly preserving a stronger but unsupported claim.

That is the tone I want for this site: technical, skeptical, useful, and open to revision.
