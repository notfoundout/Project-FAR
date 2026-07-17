# CRE-004 Frozen Decision Tree

For each case, process answers in this order.

1. If `source_difference = no`, classify the response as `invalid_case_response`.
2. If `source_difference = cannot_determine`, classify it as `unknown`.
3. If `source_difference = yes` and `translated_distinction = no`, classify it as `fail`.
4. If `source_difference = yes` and `translated_distinction = cannot_determine`, classify it as `unknown`.
5. If both are `yes`, require at least one mechanism label.
6. If the only mechanism label is `cannot_determine`, classify it as `unknown`.
7. Otherwise classify it as `pass`.
8. If `other` is selected and its registered-function follow-up identifies one of the five functions, set `hidden_reintroduction = true`.
9. Otherwise set `hidden_reintroduction = false`, unless the follow-up is `cannot_determine`, in which case set it to `unknown`.
10. Confidence never changes any classification.

No evaluator judgment may override this tree after response capture.