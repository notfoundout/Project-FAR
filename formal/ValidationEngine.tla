----------------------------- MODULE ValidationEngine -----------------------------
EXTENDS Naturals, FiniteSets, Sequences

CONSTANTS Checks, Dependencies

Statuses == {"pending", "passed", "failed", "blocked"}
Terminal == {"passed", "failed", "blocked"}

VARIABLES status, executed
vars == <<status, executed>>

Init ==
  /\ status = [c \in Checks |-> "pending"]
  /\ executed = <<>>

Ready(c) ==
  /\ status[c] = "pending"
  /\ \A d \in Dependencies[c] : status[d] \in Terminal

RunPass(c) ==
  /\ Ready(c)
  /\ \A d \in Dependencies[c] : status[d] = "passed"
  /\ status' = [status EXCEPT ![c] = "passed"]
  /\ executed' = Append(executed, c)

RunFail(c) ==
  /\ Ready(c)
  /\ \A d \in Dependencies[c] : status[d] = "passed"
  /\ status' = [status EXCEPT ![c] = "failed"]
  /\ executed' = Append(executed, c)

Block(c) ==
  /\ Ready(c)
  /\ \E d \in Dependencies[c] : status[d] # "passed"
  /\ status' = [status EXCEPT ![c] = "blocked"]
  /\ UNCHANGED executed

Next == \E c \in Checks : RunPass(c) \/ RunFail(c) \/ Block(c)

TypeInvariant == \A c \in Checks : status[c] \in Statuses
DependencySafety ==
  \A c \in Checks : status[c] \in {"passed", "failed"} =>
    \A d \in Dependencies[c] : status[d] = "passed"
BlockedSoundness ==
  \A c \in Checks : status[c] = "blocked" =>
    \E d \in Dependencies[c] : status[d] # "passed"
NoFalseSuccess ==
  (\A c \in Checks : status[c] = "passed") <=>
  ~(\E c \in Checks : status[c] \in {"failed", "blocked", "pending"})

Spec == Init /\ [][Next]_vars
=============================================================================
