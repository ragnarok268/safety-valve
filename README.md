# Safety Valve (Public Skeleton)

Safety Valve is a deterministic, pre-token input gate for LLM systems.

It runs before a model is called.
If a prompt is unsafe, it blocks it early.
If a prompt is allowed, it passes through unchanged.

This repository is an intentionally under-built public skeleton.
It demonstrates the architecture and philosophy — not the full engine.

---

## What this does

- Runs on CPU only
- Deterministic (same input → same result)
- No classifiers
- No secondary LLMs
- No fine-tuning or model weights
- Adds a fast, predictable gate before inference

Basic flow:

User prompt → Safety Valve → ALLOW or BLOCK → LLM (if allowed)

---

## Why pre-token gating

Most safety systems operate after generation.
That wastes tokens, adds latency, and introduces non-determinism.

Safety Valve blocks unsafe prompts before the model runs at all.
Failure modes are simple and auditable.

---

## What’s in this repo

- A minimal, modular pipeline
- A toy jailbreak filter (keyword-based, intentionally naive)
- A CLI entrypoint
- A small demo script
- A smoke test

Everything runs locally.

---

## What this repo is NOT

This is not:

- A production safety product
- A complete filter set
- Tuned for high recall
- A compliance framework
- A replacement for policy teams

This is a public skeleton only.

---

## Private version (NDA)

The private version extends this architecture with:

- Multi-category deterministic rule graphs
- Higher recall on adversarial inputs
- Blinded evaluation harnesses (HarmBench-equivalent)
- Sub-5ms p95 latency on commodity hardware
- Integration docs for real inference pipelines

Those components are intentionally not public.

---

## Philosophy

Simple systems fail more predictably.
Determinism beats probabilistic safety in high-risk paths.
Pre-token gating saves compute and reduces liability.
