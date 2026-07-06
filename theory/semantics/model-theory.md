# Model Theory

## Purpose

This document develops the general theory of models employed throughout Project FAR.

It establishes:

- models;
- interpretations;
- satisfaction;
- semantic validity; and
- model comparison.

Subsystem-specific notions of models shall extend these definitions rather than redefine them.

## Canonical Specification

The current formal model specification is maintained at:

`../model-theory/FAR-model-theory.md`

## Current Model Form

A FAR model has the form:

```text
A = <I, Rep, S, Int, C>
```

A FAR representation of a reasoning process has the extended form:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

## Status

Initial model-theory foundation established.

Future work should add mappings between models, submodels, conservative extensions, compression results, and preservation results.
