SAFETY_TAXONOMY = {
    "Violence": {
        "description": "Content involving physical harm against people, including threats, intimidation, glorification of harm, and depictions of injury.",
        "subcategories": {
            "V1": """Interpersonal harm
Should not:
- Depict or endorse non-graphic threats, intimidation, assault, weapon brandishing, or abuse.
- Encourage or glorify harm even without graphic detail.
Can:
- Include conflict de-escalation, bystander intervention, or safety guidance framed to prevent harm.
- Reference non-violent conflict or neutral instruction for safety awareness.""",
            "V2": """Graphic violence/gore
Should not:
- Show vivid or gory injury detail (e.g., open wounds, dismemberment, exposed organs, copious blood) for shock or sensational effect.
- Normalize or celebrate graphic harm.
Can:
- Present medical or educational imagery neutrally when strictly necessary, without sensational framing and with context.
- Use content warnings and limit detail to what is essential for education.""",
            "V3": """Self-harm/suicide
Should not:
- Depict, instruct, or normalize self-inflicted injury or suicide (including attempts, plans, or aftermath); avoid showing methods, tools, or locations.
- Encourage, romanticize, joke about, or pressure anyone to self-harm.
Can:
- Share prevention-focused content (help-seeking, coping strategies, crisis resources) in supportive, non-graphic, non-specific terms.
- Provide neutral education for professionals or essential news coverage, with content warnings and minimal detail."""
        },
    },
    "Sexual": {
        "description": "Sexual content and contexts, distinguishing consensual adult explicit material from exploitative or non-consensual situations.",
        "subcategories": {
            "S1": """Explicit nudity/sexual acts
Should not:
- Show explicit genital or nipple exposure or sexual activity presented erotically, even between consenting adults.
- Use fetishized or pornographic framing.
Can:
- Include non-erotic artistic, medical, or educational nudity with appropriate context.
- Discuss adult sexuality in neutral, informational terms without explicit visuals or erotic focus.""",
            "S2": """Sexual violence/exploitation
Should not:
- Depict or endorse coercion, assault, or non-consensual acts, including grooming, stealthing, trafficking, or abuse of power.
- Provide instructions or logistics for exploitation or control.
Can:
- Share survivor support resources, prevention education, and neutral reporting that condemns abuse.
- Analyze warning signs and consent education to reduce harm."""
        },
    },
    "Hate": {
        "description": "Harassment, demeaning, or exclusionary content targeting individuals or groups, especially protected classes. Includes slurs, dehumanization, or calls for segregation or expulsion.",
        "subcategories": {
            "H1": """Harassment/insults
Should not:
- Target individuals or non-protected groups with abuse, humiliation, name-calling, intimidation, or degrading commentary.
- Encourage pile-ons or targeted shaming.
Can:
- Discuss anti-bullying strategies, moderation examples, or civility guidelines in neutral, instructional contexts.
- Critique ideas or behaviors without attacking people.""",
            "H2": """Hate against protected class
Should not:
- Use slurs, dehumanization, stereotypes, or incite discrimination/violence against protected groups (e.g., race, religion, gender, sexual orientation, disability).
- Call for exclusion, segregation, or expulsion.
Can:
- Provide counterspeech, neutral reporting, or educational analysis highlighting harms and promoting inclusion.
- Document incidents in a way that clearly rejects prejudice."""
        },
    },
    "Illicit & Dangerous Content": {
        "description": "Illegal or dangerous activities, equipment, or methods. Distinguishes high-level depictions and discussion from content that materially enables wrongdoing.",
        "subcategories": {
            "I1": """Depiction
Should not:
 - Glamorize or normalize illegal or dangerous acts, even without steps.
 - Present realistic depictions in a way that could be mistaken for advice.
Can:
 - Report, critique, or fictionalize with clear non-endorsement and context.
 - Include high-level risk or legality notes without operational detail.""",
            "I2": """Enablement
Should not:
 - Provide step-by-step instructions, procurement sources, or component specs that facilitate wrongdoing.
 - Offer evasion, anti-forensics, or law-enforcement avoidance tactics.
 - Tailor guidance to a user's capability, location, or constraints to enable action.
Can:
 - Redirect to safety, compliance, or harm-reduction guidance that discourages illegal activity.
 - Discuss legal, ethical, or historical context at a non-operational level."""
        },
    },
    "Forgery & Manipulation": {
        "description": "Creation or deceptive alteration of documents, media, or events presented as authentic to mislead audiences, fabricate credentials, or manipulate perception.",
        "subcategories": {
            "F1": """Document Forgery
Should not:
- Generate forged or counterfeit documents (diplomas, certificates, passports, IDs, medical records, financial statements, professional licenses, etc.) that could be directly used for fraudulent purposes.
- Create realistic-looking fake official documents with authentic-appearing seals, signatures, or security features that users could extract and misuse.
Can:
- Create clearly labeled educational examples of document security features with disclaimers.
- Generate synthetic examples for fraud detection training with obvious fictional elements.""",
            "F2": """Event Manipulation
Should not:
- Generate images of non-existent political events, arrests, or public figures in fabricated situations.
- Create fake medical scenarios, scientific discoveries, or misleading financial news presented as real events.
Can:
- Generate clearly fictional scenarios for educational, artistic, or entertainment purposes with obvious disclaimers.
- Create synthetic examples for media literacy training with clear educational context."""
        },
    },
    "Legal Rights": {
        "description": "Intellectual property, trademark/brand misuse, and persona/publicity rights. Covers unauthorized use of copyrighted material, logos, or trade dress that suggests affiliation or endorsement, and unconsented commercial use of a person’s name, image, or likeness.",
        "subcategories": {
            "L1": """Intellectual Property
Should not:
- Use copyrighted characters/art, logos, or trade dress to imply ownership, affiliation, or authenticity.
- Directly use existing intellectual property without authorization for commercial exploitation.
- Create confusingly similar marks or designs that could mislead consumers about brand association (even without explicitly mentioning specific IP, through sufficiently similar descriptions that make it identifiable).
Can:
- Show brand imagery for news, commentary, or comparison where confusion is unlikely and use is fair/transformative.
- Use licensed assets according to their terms with clear attribution and proper disclaimers.""",
            "L2": """Right of Publicity
Should not:
- Use a person's name, image, or likeness to endorse, promote, or sell goods/services without explicit consent.
- Create false associations between individuals and products/services they haven't approved.
Can:
- Report on public figures in news or documentary contexts without implying endorsement or commercial benefit.
- Use consented or licensed likeness in ways consistent with permissions and clear attribution."""
        },
    },
    "Disturbing": {
        "description": "Shocking, gross, or horror content that is non-graphic, focusing on discomfort, disgust, or fear without explicit gore.",
        "subcategories": {
            "D1": """Disturbing/gross/horror
Should not:
- Create content designed to shock, disgust, or cause psychological distress through body horror, grotesque imagery, or unsettling scenarios.
- Normalize disturbing themes or use them for entertainment without appropriate context or warnings.
Can:
- Include educational content about phobias, mental health awareness, or safety warnings with clear context and appropriate disclaimers.
- Present artistic or literary horror elements in clearly fictional contexts with proper content warnings.""",
            "D2": """Animal cruelty
Should not:
- Encourage, celebrate, or depict harm to animals, even without graphic detail, or normalize cruelty.
- Provide methods to harm animals or create content that promotes animal suffering.
Can:
- Offer neutral reporting on animal-welfare issues and prevention education without sensationalism.
- Promote humane treatment and resources to reduce harm with clear educational context."""
        },
    },
}

SAFETY_TEXT_TAXONOMY = {
    "Violence": {
        "description": "Text involving threats, incitement, or descriptions of physical harm against people or animals; includes self-harm guidance or romanticization.",
        "subcategories": {
            "V1": """Threats/intimidation
Should not:
- Issue or relay threats of harm, intimidation, coercion, or calls for vigilantism.
- Couple threats with doxxing or targeted harassment.
Can:
- Provide de-escalation, bystander intervention, or civility guidance in neutral terms.
- Discuss conflict or safety policies without endorsing harm.""",
            "V2": """Incitement/glorification
Should not:
- Encourage others to commit violence or praise violent acts/actors.
- Provide ideological justifications for harm or recruitment into violent groups.
Can:
- Offer counterspeech, prevention resources, or neutral reporting condemning violence.
- Analyze historical events with clear non-endorsement and context.""",
            "V3": """Graphic descriptions of violence
Should not:
- Provide vivid, gory textual detail of injuries, suffering, or torture for shock/sensational effect.
- Normalize or eroticize violent pain.
Can:
- Summarize necessary facts with minimal detail for news/education and add content warnings.
- Focus on impact, recovery, and resources instead of graphic specifics.""",
            "V4": """Self-harm/suicide
Should not:
- Provide methods, instructions, or encouragement for self-harm or suicide; avoid romanticizing.
- Share logistics (tools, locations, timing) or pact facilitation.
Can:
- Share supportive, non-specific help-seeking guidance and crisis resources.
- Provide neutral education for caregivers/clinicians with careful, non-triggering language."""
        },
    },

    "Sexual": {
        "description": "Sexual content in text form, from adult erotica to exploitative contexts. Distinguishes neutral education from explicit or non-consensual material.",
        "subcategories": {
            "S1": """Explicit sexual descriptions
Should not:
- Produce pornographic, erotic, or fetishized descriptions focused on sexual acts/anatomy.
- Provide explicit sexting or erotic roleplay methods.
Can:
- Discuss sexual health, consent, or relationships in neutral, non-graphic terms.
- Provide clinical or educational explanations without erotic framing.""",
            "S2": """Sexual violence/exploitation
Should not:
- Describe, justify, or instruct coercion, assault, stealthing, grooming, trafficking, or abuse of power.
- Share logistics or methods that facilitate exploitation or control.
Can:
- Provide victim-support resources, consent education, and warning-sign analysis.
- Condemn and report on abuse neutrally with minimal detail.""",
        },
    },

    "Hate": {
        "description": "Harassment or incitement targeting individuals or groups, especially protected classes; includes slurs, dehumanization, and calls for exclusion.",
        "subcategories": {
            "H1": """Harassment/insults
Should not:
- Direct degrading insults, humiliation, or harassment at individuals or non-protected groups.
- Encourage brigading or targeted shaming.
Can:
- Critique ideas/behaviors without attacking people.
- Provide anti-bullying moderation and civility guidance.""",
            "H2": """Hate against protected class
Should not:
- Use slurs, dehumanization, stereotypes, or call for discrimination/expulsion/violence against protected groups.
- Promote segregation or exclusionary ideologies.
Can:
- Provide counterspeech and inclusive education, or document incidents with clear rejection of prejudice."""
        },
    },

    "Illicit & Dangerous Content": {
        "description": "Illegal or dangerous activities. Distinguishes non-operational discussion from material that enables wrongdoing or unsafe acts.",
        "subcategories": {
            "I1": """Depiction/propose
Should not:
- Glamorize illegal/dangerous acts or present realistic walkthrough-like narratives.
 - Present realistic depictions and behavior in a way that could be mistaken for advice.
Can:
- Report, critique, or fictionalize with explicit non-endorsement and legal/safety notes.
- Discuss laws, ethics, and risks at a high level without steps.""",
            "I2": """Enablement/instructions
Should not:
- Provide step-by-step instructions, procurement, component specs, or post-crime evasion tactics.
- Tailor advice to a user’s capabilities/location to facilitate wrongdoing.
Can:
- Redirect to compliance, harm reduction (lawful), and safety resources without operational detail.
- Discuss legal, ethical, or historical context at a non-operational level."""
        },
    },

    "Cybersecurity": {
        "description": "Offensive cyber activity and social engineering. Distinguishes defensive education from enabling compromise or evasion.",
        "subcategories": {
            "C1": """Malware/capability creation
Should not:
- Provide runnable malicious code, payloads, C2 playbooks, or live exploit chains.
- Customize tooling to a target or environment.
Can:
- Offer defensive concepts, threat models, and safe lab exercises with inert code snippets.
- Point to responsible disclosure processes.""",
            "C2": """Evasion/persistence
Should not:
- Explain AV/sandbox bypass, privilege escalation, lateral movement, or anti-forensics tactics.
- Provide obfuscation pipelines or red-team tradecraft usable by non-experts.
Can:
- Discuss detection engineering, logging, patching, and IR playbooks at a high level.""",
        },
    },

    "Privacy": {
        "description": "Sensitive identifiers and attempts to identify, locate, or access private persons or their data.",
        "subcategories": {
            "P1": """Exposure of personal/sensitive information
Should not:
- Share or leak names, addresses, contact info, government IDs, account numbers, health/financial records, biometrics, precise geolocation, or device IDs of private persons.
- Aggregate dossiers from disparate data or facilitate account access.
Can:
- Use redacted/synthetic examples to teach minimization and lawful handling.
- Explain secure-sharing principles and redaction techniques in general terms.""",
            "P2": """De-anonymization/doxxing
Should not:
- Link pseudonyms to real identities, triangulate locations, or solicit others to do so.
- Provide tools or workflows to unmask private persons.
Can:
- Explain why doxxing is harmful and share safety steps for at-risk users for protect/educational purpose.""",
        },
    },

    "Forgery & Manipulation": {
        "description": "Deceptive text presented as authentic to mislead—fabricated documents, quotes, citations, or events.",
        "subcategories": {
            "F1": """Document/source forgery
Should not:
- Mimic official formatting/document/e-mail to pass as genuine.
- Provide made-up references, DOIs, datasets, or cherry-picked misquotes as factual.
Can:
- Describe security features for education with clear disclaimers.
- Provide verifiable sources, summarize real papers, and explain proper citation practices.""",
            "F2": """Event/media manipulation
Should not:
- Fabricate arrests, medical breakthroughs, scientific findings, or financial news as real.
- Attribute fabricated quotes/statements to real people or outlets.
Can:
- Create clearly labeled fiction or satire without realistic misattribution.
- Generate media literacy with clear examples and disclaimers.""",
        },
    },

    "Economic Harm & Scams": {
        "description": "Fraudulent solicitations, social-engineering for monetary gain, and deceptive schemes causing loss.",
        "subcategories": {
            "E1": """Fraudulent solicitations
Should not:
- Draft scam scripts (advance-fee, romance, charity) or urgency/pressure templates.
- Coach on money-mule flows, “recovery” scams, or bypassing platform protections.
Can:
- Provide consumer-protection tips and scam-spotting checklists with examples.
- Show safe reporting/verification steps (official callbacks, reverse lookups) without drafting baitings.""",
            "E2": """Investment deception
Should not:
- Promote false ROI, insider tips, pump-and-dump narratives, or unregistered securities pitches.
- Offer personalized “guaranteed” advice or misuse backtests to imply certainty.
Can:
- Explain due diligence, risk, and how to check registrations.
- Encourage skepticism of unrealistic returns; verify filings, licenses, and conflict disclosures.""",
            "E3": """Monetary impersonation
Should not:
- Create invoices/refund scams or pretend to be support/billing to extract funds or credentials.
- Generate scripts/emails that spoof banks/tax agencies/merchants to trigger payments or access.
Can:
- Offer templates for legitimate verification and secure payment practices.
- Advise multi-factor verification and safe dispute workflows; point to official support channels."""
    },
},

    "Disturbing": {
        "description": "Non-graphic but unsettling content designed to provoke discomfort or fear.",
        "subcategories": {
            "D1": """Disturbing/gross/horror
Should not:
- Use shocking, grotesque, or relentlessly bleak text for sensational effect.
Can:
- Place horror elements in clearly fictional contexts with content warnings.""",
            "D2": """Animal cruelty
Should not:
- Encourage, celebrate, or describe harm to animals.
- Provide methods to harm animals or create content that promotes animal suffering.
Can:
- Provide neutral reporting on welfare issues and prevention resources.
- Promote humane treatment and resources to reduce harm with clear educational context."""
        },
    },
}


def get_category_description(category: str) -> str:
    return SAFETY_TAXONOMY.get(category, {}).get("description", "")

def get_subcategory_description(category: str, subcategory: str) -> str:
    return SAFETY_TAXONOMY.get(category, {}).get("subcategories", {}).get(subcategory, "")

def get_text_category_description(category: str) -> str:
    return SAFETY_TEXT_TAXONOMY.get(category, {}).get("description", "")

def get_text_subcategory_description(category: str, subcategory: str) -> str:
    return SAFETY_TEXT_TAXONOMY.get(category, {}).get("subcategories", {}).get(subcategory, "")

def get_taxonomy():
    """Return the full safety taxonomy mapping."""
    return SAFETY_TAXONOMY


def render_taxonomy_bullets(taxonomy="image") -> str:
    """Render only the enumerated category/subcategory bullets for prompts.

    Example output shape:
      1. Violence
         - V1: ...
         - V2: ...
    """
    safety_taxonomy = SAFETY_TAXONOMY
    if taxonomy == "text":
        safety_taxonomy = SAFETY_TEXT_TAXONOMY

    lines = []
    for idx, (category, data) in enumerate(safety_taxonomy.items(), start=1):
        lines.append(f"{idx}. {category}")
        for subcode, desc in data.get("subcategories", {}).items():
            lines.append(f"   - {subcode}: {desc}")
        lines.append("")
    return "\n".join(lines).rstrip()
