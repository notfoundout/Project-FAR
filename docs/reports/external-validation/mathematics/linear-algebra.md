# External Validation: Linear Algebra

## Target System

Linear algebra studies vectors, vector spaces, linear maps, matrices, bases, dimensions, and invariant relations.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | vector, scalar, matrix, basis, equation, transformation |
| Representational structure | coordinate tuple, matrix arrangement, span relation, linear dependence relation |
| Interpretation | specified field, vector space, basis, and linear map |
| Investigation | prove linearity, dependence, dimension, invertibility, or equivalence |
| Reasoning calculus | field axioms, vector-space axioms, definitions, and algebraic rules |
| Operation | addition, scalar multiplication, row operation, basis change, substitution |

## Valid Case

Claim: The zero vector in a vector space is unique.

Suppose 0 and z are both additive identities. Then 0 + z = z because 0 is an identity, and 0 + z = 0 because z is an identity. Therefore z = 0.

FAR can represent the two candidate identities, the shared expression, the equality chain, and the final determination.

Result: PASS.

## Invalid Case

Claim: Two matrices with the same determinant are equal.

The determinant is not a complete representation of a matrix. Distinct matrices may share the same determinant. FAR can distinguish preservation of one derived value from structural equivalence of the full matrices.

Result: PASS.

## Malformed or Scope-Violating Case

A row operation divides by a symbolic quantity without establishing that the quantity is nonzero.

The operation is conditionally admissible, not universally admissible. FAR can record the hidden condition and classify the step as unsupported when the condition is absent.

Result: PASS.

## Limitations

FAR does not supply vector-space axioms, determinant theory, field properties, or computational algorithms. Those remain part of the target mathematical calculus.

## Final Outcome

CONDITIONAL PASS

Condition: the field, vector space, basis conventions, and admissible algebraic operations must be explicit.
