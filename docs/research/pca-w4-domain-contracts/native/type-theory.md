# Native contract: type theory

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

Does a raw term determine a typing judgment when the context is omitted? Contextual types pair an object with the context in which it is meaningful [pientka2020contextual], and standard presentations of dependent type theory make judgments explicitly context-indexed [angiuli2026principles].

## Finite fragment

Use a simply typed fragment with base types `Nat` and `Bool`, a variable `x`, and `succ : Nat -> Nat`. The two cases share the raw term `x`:

- `GNat = x:Nat`;
- `GBool = x:Bool`.

The declared behavior asks whether `succ x` checks at `Nat`. The answer is true under `GNat` and false under `GBool`. The raw term alone therefore does not determine the judgment.

The repaired carrier is `(context, raw term)`. The decoder performs the two lookup/application checks of this finite fragment.

## Scope boundary

This is a context-sensitivity witness in a simply typed subfragment, not a completeness or decidability result for dependent type theory. Definitional equality, universes, dependency, elaboration, and context equivalence are outside scope.
