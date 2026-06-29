# Example — Mathematical Proof

## Purpose

This example demonstrates how Project FAR represents a simple mathematical proof.

The objective is to illustrate the application of FARA and FAR to deductive reasoning.

---

# Investigation

## Question

Is the sum of two even integers always even?

---

## Objective

Determine whether the statement follows from the accepted definitions of even integers and ordinary arithmetic.

---

# Representations

The investigation begins with the following representations.

- Definition of an even integer.
- Let $begin:math:text$a$end:math:text$ and $begin:math:text$b$end:math:text$ be even integers.
- Rules of integer arithmetic.

---

# Representational Structure

The definition establishes the meaning of "even."

The assumptions introduce the objects under investigation.

The arithmetic rules govern valid transformations.

---

# Interpretation

An integer is interpreted as even if it is divisible by two.

Equivalently,

- $begin:math:text$a \= 2m$end:math:text$ for some integer $begin:math:text$m$end:math:text$
- $begin:math:text$b \= 2n$end:math:text$ for some integer $begin:math:text$n$end:math:text$

---

# Reasoning Calculus

The investigation employs ordinary deductive reasoning using the accepted rules of arithmetic.

---

# Initial Reasoning State

The investigation begins with the assumptions:

- $begin:math:text$a \= 2m$end:math:text$
- $begin:math:text$b \= 2n$end:math:text$

for integers $begin:math:text$m$end:math:text$ and $begin:math:text$n$end:math:text$.

---

# Transformations

## Transformation 1

Compute the sum.

$begin:math:display$
a\+b \= 2m \+ 2n
$end:math:display$

---

## Transformation 2

Factor the common term.

$begin:math:display$
a\+b \= 2\(m\+n\)
$end:math:display$

---

## Transformation 3

Since the sum of two integers is an integer,

$begin:math:display$
m\+n
$end:math:display$

is an integer.

Therefore,

$begin:math:display$
a\+b
$end:math:display$

is divisible by two.

---

# Candidates

The investigation admits two candidates.

- The sum is even.
- The sum is not necessarily even.

---

# Admissibility Structure (Ω)

| Candidate | Admissibility |
|-----------|---------------|
| The sum is even | Admissible |
| The sum is not necessarily even | Not Admissible |

---

# Resolution Rule

Select the admissible candidate supported by the deductive reasoning process.

---

# Resolution

The sum of two even integers is always even.

---

# Discussion

This example demonstrates that Project FAR naturally represents deductive reasoning.

Every inference is explicit.

Each transformation produces a new reasoning state.

The final resolution follows from the admissibility classification established by the reasoning calculus.
