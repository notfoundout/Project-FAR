from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from typing import Literal

from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator

from .app import PAGE, app
from .formats import ACCEPT_ATTRIBUTE

logger = logging.getLogger("far.validation")

Role = Literal[
    "founder_or_executive",
    "ai_engineering",
    "security",
    "governance_risk_compliance",
    "enterprise_procurement",
    "consultant_or_advisor",
    "researcher",
    "other",
]
Organization = Literal[
    "ai_startup",
    "enterprise",
    "consultancy",
    "government_or_nonprofit",
    "academic",
    "independent",
    "other",
]
Wedge = Literal[
    "release_assurance",
    "incident_reconstruction",
    "procurement_evidence",
    "instrumentation_sufficiency",
]
ReleaseAction = Literal[
    "block_release",
    "require_human_review",
    "allow_release",
    "not_sure",
]
BudgetAnswer = Literal[
    "yes",
    "no",
    "not_sure",
    "i_am_the_budget_owner",
]


class ValidationFeedback(BaseModel):
    role: Role
    organization_type: Organization
    strongest_use_case: Wedge
    clarity_score: int = Field(ge=1, le=5)
    trust_score: int = Field(ge=1, le=5)
    release_action: ReleaseAction
    would_share_authorized_artifacts: bool
    budget_owner_identified: BudgetAnswer
    design_partner_interest: bool
    contact_email: str | None = Field(default=None, max_length=254)
    source: str = Field(default="direct", min_length=1, max_length=64)
    session_id: str = Field(min_length=8, max_length=80)
    consent_to_store: bool

    @field_validator("contact_email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Enter a valid email address or leave it blank.")
        return value.lower()

    @field_validator("source", "session_id")
    @classmethod
    def validate_tracking_token(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9._:-]+", value):
            raise ValueError("Tracking values may contain letters, numbers, dots, underscores, colons, and hyphens only.")
        return value


@app.get("/api/validation-config")
def validation_config() -> dict[str, object]:
    return {
        "study": "far-commercial-wedge-validation-v1",
        "commercial_wedges": [
            "release_assurance",
            "incident_reconstruction",
            "procurement_evidence",
            "instrumentation_sufficiency",
        ],
        "privacy": {
            "uploaded_package_contents_collected": False,
            "uploaded_filenames_collected": False,
            "ip_address_intentionally_collected": False,
            "user_agent_intentionally_collected": False,
            "free_text_collected": False,
        },
    }


@app.post("/api/feedback")
def submit_feedback(feedback: ValidationFeedback) -> dict[str, str]:
    if not feedback.consent_to_store:
        raise HTTPException(400, "Consent is required to submit validation feedback.")

    event = {
        "schema": "far-validation-feedback/1.0",
        "study": "far-commercial-wedge-validation-v1",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        **feedback.model_dump(exclude={"consent_to_store"}),
    }
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
    receipt = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    logger.info("far_validation_feedback %s", canonical)
    return {"status": "recorded", "receipt": receipt}


FEEDBACK_SECTION = r'''
<section class="section" id="validation-feedback">
  <div class="sectionHead">
    <div class="sectionLabel">Controlled validation</div>
    <div>
      <h2>Would this change a real release decision?</h2>
      <p class="sectionLead">This structured study tests which FAR use case has the strongest operational value. It does not collect uploaded package contents, filenames, open-ended comments, IP addresses, or browser fingerprints intentionally.</p>
    </div>
  </div>
  <form id="feedbackForm" class="feedbackGrid">
    <label>Primary role<select name="role" required>
      <option value="">Select</option><option value="founder_or_executive">Founder or executive</option><option value="ai_engineering">AI engineering</option><option value="security">Security</option><option value="governance_risk_compliance">Governance, risk, or compliance</option><option value="enterprise_procurement">Enterprise procurement</option><option value="consultant_or_advisor">Consultant or advisor</option><option value="researcher">Researcher</option><option value="other">Other</option>
    </select></label>
    <label>Organization type<select name="organization_type" required>
      <option value="">Select</option><option value="ai_startup">AI startup</option><option value="enterprise">Enterprise</option><option value="consultancy">Consultancy</option><option value="government_or_nonprofit">Government or nonprofit</option><option value="academic">Academic</option><option value="independent">Independent</option><option value="other">Other</option>
    </select></label>
    <label>Strongest use case<select name="strongest_use_case" required>
      <option value="">Select</option><option value="release_assurance">Release assurance</option><option value="incident_reconstruction">Incident reconstruction</option><option value="procurement_evidence">Procurement evidence</option><option value="instrumentation_sufficiency">Instrumentation sufficiency</option>
    </select></label>
    <label>What should happen to this release?<select name="release_action" required>
      <option value="">Select</option><option value="block_release">Block release</option><option value="require_human_review">Require human review</option><option value="allow_release">Allow release</option><option value="not_sure">Not sure</option>
    </select></label>
    <label>Clarity score<select name="clarity_score" required><option value="">1–5</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></label>
    <label>Trust score<select name="trust_score" required><option value="">1–5</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></label>
    <label>Would you provide authorized artifacts?<select name="would_share_authorized_artifacts" required><option value="">Select</option><option value="true">Yes</option><option value="false">No</option></select></label>
    <label>Is a budget owner identifiable?<select name="budget_owner_identified" required><option value="">Select</option><option value="i_am_the_budget_owner">I am the budget owner</option><option value="yes">Yes</option><option value="no">No</option><option value="not_sure">Not sure</option></select></label>
    <label>Design-partner interest<select name="design_partner_interest" required><option value="">Select</option><option value="true">Yes</option><option value="false">No</option></select></label>
    <label>Contact email <span>(optional)</span><input type="email" name="contact_email" autocomplete="email" maxlength="254"></label>
    <label class="consent"><input type="checkbox" name="consent_to_store" required> Store these structured answers for Project FAR product validation.</label>
    <div class="feedbackAction"><button class="primary" type="submit">Submit validation record</button><p id="feedbackStatus"></p></div>
  </form>
</section>
<style>
.feedbackGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;background:var(--panel);border:1px solid var(--line2);border-radius:22px;padding:22px}.feedbackGrid label{display:grid;gap:8px;color:#c6ceda;font-size:12px}.feedbackGrid label span{color:var(--muted)}.feedbackGrid select,.feedbackGrid input[type=email]{width:100%;border:1px solid var(--line2);background:#090d14;color:var(--ink);border-radius:10px;padding:13px}.feedbackGrid .consent{grid-column:1/-1;display:flex;align-items:flex-start;gap:10px;line-height:1.45}.feedbackGrid .consent input{margin-top:3px}.feedbackAction{grid-column:1/-1;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.feedbackAction p{margin:0;color:var(--muted);font-size:13px}@media(max-width:700px){.feedbackGrid{grid-template-columns:1fr;padding:17px}.feedbackGrid .consent,.feedbackAction{grid-column:auto}}
</style>
'''

FEEDBACK_SCRIPT = r'''
<script>
const feedbackForm=document.getElementById('feedbackForm');
const querySource=new URLSearchParams(location.search).get('source')||'direct';
const source=/^[A-Za-z0-9._:-]{1,64}$/.test(querySource)?querySource:'direct';
let sessionId=sessionStorage.getItem('far_validation_session');
if(!sessionId){sessionId=(crypto.randomUUID?crypto.randomUUID():'session-'+Date.now()+'-'+Math.random().toString(16).slice(2));sessionStorage.setItem('far_validation_session',sessionId);}
feedbackForm.addEventListener('submit',async event=>{
  event.preventDefault();
  const status=document.getElementById('feedbackStatus');
  status.textContent='Recording…';
  const form=new FormData(feedbackForm);
  const payload={
    role:form.get('role'),organization_type:form.get('organization_type'),strongest_use_case:form.get('strongest_use_case'),
    clarity_score:Number(form.get('clarity_score')),trust_score:Number(form.get('trust_score')),release_action:form.get('release_action'),
    would_share_authorized_artifacts:form.get('would_share_authorized_artifacts')==='true',budget_owner_identified:form.get('budget_owner_identified'),
    design_partner_interest:form.get('design_partner_interest')==='true',contact_email:form.get('contact_email')||null,
    source,session_id:sessionId,consent_to_store:form.get('consent_to_store')==='on'
  };
  try{
    const response=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const data=await response.json();
    if(!response.ok)throw new Error(data.detail||'Submission failed');
    status.textContent='Recorded · receipt '+data.receipt.slice(0,12);
    feedbackForm.querySelector('button').disabled=true;
  }catch(error){status.textContent=error.message;}
});
</script>
'''


# Replace the original root route so the validation build can inject the study
# without coupling feedback storage to uploaded package handling.
app.router.routes = [
    route
    for route in app.router.routes
    if not (getattr(route, "path", None) == "/" and "GET" in getattr(route, "methods", set()))
]


@app.get("/", response_class=HTMLResponse)
def validation_index() -> str:
    page = PAGE.replace("__ACCEPT__", ACCEPT_ATTRIBUTE)
    page = page.replace("<footer>", FEEDBACK_SECTION + "<footer>")
    return page.replace("</body>", FEEDBACK_SCRIPT + "</body>")
