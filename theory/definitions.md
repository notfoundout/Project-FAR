# Definitions

## Purpose

This document contains the canonical definitions of the formal terminology used throughout Project FAR.

Unless explicitly stated otherwise, every technical term appearing elsewhere in the project refers to the definitions given here.

---

# General Concepts

## Object

An **object** is any entity that can be explicitly distinguished.

---

## Property

A **property** is a characteristic that an object may possess.

---

## Relation

A **relation** is an explicitly defined association between two or more objects.

---

## Structure

A **structure** is an organized arrangement of objects together with the relations between them.

---

## Component

A **component** is an object that forms part of a larger structure.

---

## System

A **system** is a collection of interacting objects organized according to a structure.

---

## Model

A **model** is a representation of a system intended to capture selected properties of that system.

---

## Framework

A **framework** is an organized collection of concepts, definitions, and procedures developed to achieve a particular objective.

---

## Architecture

An **architecture** is a specification of the objects, relations, and organizing principles required to represent a class of systems.

---

## Domain

A **domain** is the collection of objects to which a claim, property, or framework is intended to apply.

---

## Universal

A property is **universal** over a specified domain if it applies to every member of that domain.

Universality is always relative to an explicitly stated domain.

---

## Universal Architecture

A **universal architecture** is an architecture capable of representing every member of a specified domain.

Universality does not imply uniqueness or minimality.

---

## Minimal

A structure is **minimal** if removing any required component reduces its intended expressive power.

---

## Primitive

A **primitive** is a concept that has not been derived from simpler concepts within the framework.

---

## Derived Concept

A **derived concept** is a concept defined in terms of one or more other concepts within the framework.

---

## Reduction

A **reduction** is the demonstration that one concept can be completely represented in terms of other concepts.

---

## Independence

Two concepts are **independent** if neither can be derived from the other within the framework.

---

## Equivalence

Two objects are **equivalent** if they satisfy the criteria specified by an explicitly stated equivalence relation.

---

## Expressive Power

The **expressive power** of a framework is the collection of objects, relations, or systems that it is capable of representing.

---

# Reasoning Concepts

## Investigation

An **investigation** specifies the object of analysis together with the criteria by which reasoning is organized.

Every reasoning process is relative to an investigation.

---

## Representation

A **representation** is an explicitly distinguishable object used to represent information within an investigation.

Representations are the fundamental objects manipulated during reasoning.

---

## Representational Structure

A **representational structure** is an organized collection of representations together with the relations between them.

---

## Interpretation

An **interpretation** assigns meaning to representations.

The same representation may possess different meanings under different interpretations.

---

## Reasoning

**Reasoning** is the process of producing, transforming, or evaluating explicit representations according to a reasoning calculus within the context of an investigation.

---

## Reasoning Calculus

A **reasoning calculus** is a collection of rules governing admissible reasoning transitions.

Project FAR remains independent of any particular reasoning calculus.

---

## State

A **state** is the complete specification of an object's relevant properties at a particular point of analysis.

---

## Transformation

A **transformation** is a rule or process that maps one state to another.

---

## Reasoning State

A **reasoning state** is the complete explicit representation of an investigation at a particular stage of reasoning.

A reasoning state is a specialized form of state.

---

## Transition Signature

A **transition signature** is the explicit description of the transformation between two reasoning states.

---

## Candidate

A **candidate** is an explicitly represented object admitted for consideration within an investigation.

A candidate need not ultimately be admissible or selected.

---

## Criterion

A **criterion** is an explicit condition used to determine classification, admissibility, or selection.

---

## Classification

A **classification** is the assignment of one or more objects to categories according to explicitly defined criteria.

---

## Admissibility

**Admissibility** is the property of satisfying the criteria established by a reasoning calculus within an investigation.

---

## Admissibility Structure (Ω)

The **admissibility structure**, denoted **Ω**, classifies the candidates admitted for consideration within an investigation according to the applicable reasoning calculus.

Ω records the admissibility status of each candidate.

---

## Resolution Rule

A **resolution rule** specifies how one or more admissible candidates are selected as the resolution of an investigation.

---

## Resolution

A **resolution** is the candidate, or collection of candidates, selected from an admissibility structure according to the applicable resolution rule.
