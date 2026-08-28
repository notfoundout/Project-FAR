import FARCoreV11Substrate

/-!
# FAR-CORE-013: canonical FARA Omega elimination

Omega is exactly the materialized representation of the calculus classification.  Operational
caching or audit value is not denied; no independent semantic information is introduced.
-/

namespace FARCoreV11.Omega

universe u v w z

/-- Canonical Omega materialization. -/
def omega {Investigation : Type u} {Classification : Type v} {OmegaRecord : Type w}
    (classifyKappa : Investigation -> Classification)
    (represent : Classification -> OmegaRecord) : Investigation -> OmegaRecord :=
  fun investigation => represent (classifyKappa investigation)

/-- FAR-CORE-013: unfolding Omega eliminates the materialized view. -/
theorem omega_elimination
    {Investigation : Type u} {Classification : Type v} {OmegaRecord : Type w}
    (classifyKappa : Investigation -> Classification)
    (represent : Classification -> OmegaRecord) (investigation : Investigation) :
    omega classifyKappa represent investigation = represent (classifyKappa investigation) := by
  rfl

/-- Resolving canonical Omega is exactly ordinary function composition. -/
theorem resolve_is_composition
    {Investigation : Type u} {Classification : Type v}
    {OmegaRecord : Type w} {Result : Type z}
    (classifyKappa : Investigation -> Classification)
    (represent : Classification -> OmegaRecord)
    (resolve : OmegaRecord -> Result) :
    (fun investigation => resolve (omega classifyKappa represent investigation)) =
      resolve ∘ represent ∘ classifyKappa := by
  rfl

/-- Negative control: an extra field is additional information, not canonical Omega. -/
theorem extra_information_is_not_canonical_omega
    {Investigation : Type u} {Classification : Type v}
    {OmegaRecord : Type w} {Extra : Type z}
    (classifyKappa : Investigation -> Classification)
    (represent : Classification -> OmegaRecord)
    (investigation : Investigation) {extra₀ extra₁ : Extra} (hdifferent : extra₀ ≠ extra₁) :
    (omega classifyKappa represent investigation, extra₀) ≠
      (omega classifyKappa represent investigation, extra₁) := by
  intro hequal
  exact hdifferent (congrArg Prod.snd hequal)

end FARCoreV11.Omega
