# Added to actor.schema.yaml properties:

  classification:
    type: string
    enum: ["internal_auditor", "external_auditor", "researcher", "founder", "system"]
    description: "Auditor classification. Determines promotion authority per PL-001 Interim Governance Rule."
  
  auditor_agreement_signed:
    type: boolean
    description: "Has this actor signed the Loom auditor agreement?"
  
  auditor_agreement_date:
    type: string
    format: date
    description: "When the agreement was signed"
  
  capacity_limit:
    type: integer
    minimum: 0
    description: "Maximum concurrent audit assignments (0 = inactive)"
  
  current_assignments:
    type: integer
    minimum: 0
    description: "Current active audit assignments"
  
  rotation_group:
    type: string
    description: "Rotation group identifier for load balancing"
  
  independence_distance:
    type: string
    enum: ["none", "organizational", "financial", "professional", "personal"]
    description: "Closest relationship to founder/project that could compromise independence"
  
  independence_disclosure:
    type: string
    description: "Detailed description of any relationship requiring disclosure"
  
  can_promote_to_accepted:
    type: boolean
    description: "Can this actor participate in 'accepted' promotions? (internal auditors only under bootstrap rule)"
  
  can_promote_to_canonical:
    type: boolean
    description: "Can this actor participate in 'canonical' promotions? (external auditors only)"
  
  active:
    type: boolean
    description: "Is this auditor currently active in the pool?"

# Added to required array:
# - classification
# - auditor_agreement_signed
# - active