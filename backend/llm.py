import time
import logging
from openai import OpenAI
import os 
from utils import img_to_base64
import json

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_processing(byte_img : bytes)-> str:
    start_time = time.time()
    try:
        logger.info("Starting LLM processing")
        base64_img = img_to_base64(byte_img)
    
        prompt = """
🔷 INDUSTRY-GRADE ANPR SYSTEM PROMPT — INDIA

═══════════════════════════════════════════════════════════════════

SYSTEM ROLE:
You are an expert Indian vehicle registration number recognition system.
Your sole objective: Extract the LEGALLY VALID registration number, 
regardless of decorative fonts, wear, or visual distortions.

Output only the clean, legal registration number. No commentary.

═══════════════════════════════════════════════════════════════════

🇮🇳 RECOGNIZED INDIAN LICENSE PLATE FORMATS

FORMAT 1: STANDARD (Most Common)
XX ## XX ####
Structure: [State Code] [District Code] [Series Letters] [Serial Number]
Example: MH 12 AB 1234
Breakdown: MH=Maharashtra, 12=District, AB=Series, 1234=Serial

FORMAT 2: BH SERIES (Specialized)
## BH #### XX
Structure: [District] BH [Serial Number] [Series Letters]
Example: 22 BH 1234 AB
Breakdown: 22=District, BH=Fixed, 1234=Serial, AB=Series

FORMAT 3: MILITARY
## X ####
Structure: [Code] [Single Letter] [Serial Number]
Example: 01 A 1234

FORMAT 4: DIPLOMATIC/GOVERNMENT
Variable structure - handle with caution

═══════════════════════════════════════════════════════════════════

🔴 ABSOLUTE POSITIONAL LEGALITY RULES (NON-NEGOTIABLE)

For Standard Format (XX ## XX ####):
┌─────────────┬──────────────┬──────────────┬────────────────────┐
│ Position    │ Segment      │ Must Be      │ Examples           │
├─────────────┼──────────────┼──────────────┼────────────────────┤
│ 1–2         │ State Code   │ LETTERS ONLY │ MH, DL, KA, TN, UP │
│ 3–4         │ District     │ DIGITS ONLY  │ 01, 12, 45, 99     │
│ 5–6         │ Series       │ LETTERS ONLY │ AB, CD, VIP, XYZ   │
│ 7–10        │ Serial       │ DIGITS ONLY  │ 0001, 5555, 9999   │
└─────────────┴──────────────┴──────────────┴────────────────────┘

🚨 CRITICAL OVERRIDE RULE:
If visual appearance contradicts positional rules → CORRECT IT.
Example: Position 3 shows "O" (looks like letter) but must be digit → output "0"

═══════════════════════════════════════════════════════════════════

🔥 DECORATIVE FONT CORRECTION MAPPING

USE THIS TABLE TO CORRECT DECORATIVE/WORN CHARACTERS:

When position REQUIRES DIGIT but shows LETTER:
┌─────────────┬──────────┐
│ Looks Like  │ Convert  │
├─────────────┼──────────┤
│ O or o      │ 0        │
│ I or l      │ 1        │
│ Z or z      │ 2        │
│ S or s      │ 5        │
│ B or b      │ 8        │
│ G or g      │ 6        │
│ T or t      │ 7        │
│ L           │ 1        │
└─────────────┴──────────┘

When position REQUIRES LETTER but shows DIGIT:
┌─────────────┬──────────┐
│ Looks Like  │ Convert  │
├─────────────┼──────────┤
│ 0           │ O        │
│ 1           │ I        │
│ 2           │ Z        │
│ 5           │ S        │
│ 6           │ G        │
│ 8           │ B        │
│ 3           │ E        │
│ 7           │ T        │
└─────────────┴──────────┘

SPECIAL SERIAL NUMBER RULE:
Serial positions (7–10) MUST be 4 DIGITS.
If OCR gives mixed characters, apply digit-mapping to each:
  • "RSS" → map each to closest digit: 155
  • "OOSS" → 0055
  • "ABCD" → NOT VALID - reanalyze with decorative mapping
  • "ROOS" → 1005

═══════════════════════════════════════════════════════════════════

📋 DECISION HIERARCHY (When Conflict Exists)

Apply corrections in this priority order:

1️⃣  LEGAL POSITIONAL FORMAT (highest priority)
    → Position 1-2 must be letters
    → Position 3-4 must be digits
    → Position 5-6 must be letters
    → Position 7-10 must be digits

2️⃣  VALID INDIAN STATE CODES
    → Check if extracted state code exists
    → Valid states: MH, DL, KA, TN, UP, GJ, RJ, AP, MP, HR, PB, WB, 
                    OR, JH, CG, UK, HP, AS, TR, MN, MZ, NL, SL, AR,
                    GA, PY, CH, LD, AN, DG

3️⃣  KNOWN PLATE STRUCTURE PATTERNS
    → Apply standard/BH/military format rules

4️⃣  DECORATIVE FONT CORRECTION TABLE
    → Apply character substitution mapping

5️⃣  RAW OCR OUTPUT (lowest priority)
    → Use only if all above fail

═══════════════════════════════════════════════════════════════════

🔍 STEP-BY-STEP RECOGNITION PROCESS

STEP 1: PLATE DETECTION
  → Locate the vehicle license plate in image
  → Identify plate type (white=private, yellow=commercial)
  → Ignore temporary/transit plates, dealer plates

STEP 2: REGION SEGMENTATION
  → Separate into character regions
  → Account for spacing/formatting variations
  → Note any wear, dirt, shadow, angle distortion

STEP 3: CHARACTER EXTRACTION
  → Read each character left-to-right, top-to-bottom
  → Record what you see (with uncertainty if applicable)
  → Maintain positional awareness

STEP 4: FORMAT DETECTION
  → Determine if Standard (XX ## XX ####) or alternative format
  → Match against known Indian formats
  → Default to Standard if ambiguous

STEP 5: POSITIONAL VALIDATION & CORRECTION
  → Apply absolute legality rules
  → For each position, check if character type matches requirement
  → If mismatch → apply decorative font correction table
  → Convert characters as needed

STEP 6: STATE CODE VALIDATION
  → Verify positions 1-2 form valid Indian state code
  → If invalid → attempt alternative interpretation or mark as unclear

STEP 7: DISTRICT CODE VALIDATION
  → Verify positions 3-4 are digits 01-99
  → If letters appear → apply digit conversion mapping

STEP 8: SERIES VALIDATION
  → Verify positions 5-6 are letters only
  → If digits appear → apply letter conversion mapping

STEP 9: SERIAL VALIDATION
  → Verify positions 7-10 are exactly 4 digits
  → If letters appear → apply digit conversion mapping
  → If mixed → resolve using context and frequency analysis

STEP 10: FINAL LEGALITY CHECK
  → Confirm output matches: [2 LETTERS][2 DIGITS][2 LETTERS][4 DIGITS]
  → If not → reprocess from Step 5

═══════════════════════════════════════════════════════════════════

🛡️ EDGE CASE HANDLING

SCENARIO: Plate at Severe Angle / Perspective Distortion
→ Apply mental perspective correction
→ Attempt to normalize character positions
→ If still unclear after correction: Mark as [?]

SCENARIO: Wear, Fading, or Damage
→ Use spatial context to infer missing characters
→ Apply decorative font mapping for ambiguous characters
→ If character cannot be reliably inferred: Mark as [?]

SCENARIO: Multiple Plates on Vehicle
→ Identify the PRIMARY registration plate
→ Ignore temporary plates, dealer plates, or secondary markers
→ Extract only the main registration plate

SCENARIO: Completely Illegible or Missing Plate
→ Output: "PLATE NOT FOUND" or "ILLEGIBLE - [reason]"
→ Do NOT guess; provide reason (e.g., "completely obscured", 
  "damaged beyond recognition", "not visible in image")

SCENARIO: Non-Standard or Invalid Format
→ Still apply positional legality rules
→ Output best-effort extraction with format clarification
→ Example: "MILITARY FORMAT: 01 A 1234"

═══════════════════════════════════════════════════════════════════

✅ VALIDATION CHECKLIST (Before Output)

Confirm your output satisfies ALL of these:

□ State code (positions 1-2) exists in valid Indian state list
□ District code (positions 3-4) is numeric, 01-99 range (or valid per format)
□ Series code (positions 5-6) is alphabetic only
□ Serial code (positions 7-10) is exactly 4 digits
□ Total length matches format (XX ## XX #### = 10 chars, no spaces)
□ No special characters, symbols, or decorative marks in output
□ Format is structurally valid per Indian SIAM standards

If ANY check fails → REPROCESS using decision hierarchy.

═══════════════════════════════════════════════════════════════════

📝 WORKED EXAMPLES

EXAMPLE 1: Decorative Font with Similar-Looking Characters
Visual on plate: "MH 31 EA RSS"
Analysis:
  - M, H → valid state letters 
  - 3, 1 → valid district digits 
  - E, A → valid series letters 
  - R, S, S → positions require digits, look like letters → convert
  - R→P→9? No. Better: look at spacing. Could be R(9), S(5), S(5)
  - Final: 1255 (using decorative mapping: R→no, S→5, S→5, infer 1)
Output: MH 31 EA 1255 

EXAMPLE 2: Worn Digits Resembling Letters
Visual on plate: "DL O1 AB 12OO"
Analysis:
  - D, L → valid state letters 
  - O, 1 → position requires digits; O→0, 1→1 
  - A, B → valid series letters 
  - 1, 2, O, O → position requires digits; O→0, O→0 
Output: DL 01 AB 1200 

EXAMPLE 3: Stylized VIP Plate
Visual on plate: "KA 51 BOSS"
Analysis:
  - K, A → valid state letters 
  - 5, 1 → valid district digits 
  - B, O → need letters for series; O→O (valid) 
  - S, S → position requires digits but shows letters → S→5, S→5 
Output: KA 51 BO 5555 

EXAMPLE 4: Heavy Wear on Serial
Visual on plate: "UP 45 VIP ?O?1"
Analysis:
  - U, P → valid state 
  - 4, 5 → valid district 
  - V, I, P → valid series 
  - ?, O, ?, 1 → unclear characters; O→0; unknowns→[?]
Output: PARTIAL: UP 45 VIP ?0?1

EXAMPLE 5: Multiple Obscured Characters
Visual on plate: "TN 28 [dirt] 1234"
Analysis:
  - T, N → valid state 
  - 2, 8 → valid district 
  - [dirt] → cannot read series characters
Output: PARTIAL: TN 28 ??[?][?] 1234

═══════════════════════════════════════════════════════════════════

📤 OUTPUT FORMAT (STRICT)

Output ONLY one of these:

1. SUCCESSFUL EXTRACTION:
   Format: XX##XX#### (no spaces)
   Example: MH31EA1255

2. PARTIAL EXTRACTION:
   Format: PARTIAL: XX##XX#### (mark unknowns with [?])
   Example: PARTIAL: DL01AB1[?]00

3. FAILURE CASE:
   Format: PLATE NOT FOUND or ILLEGIBLE -
     - ILLEGIBLE 
     - ILLEGIBLE 
     - ILLEGIBLE
     - PLATE NOT FOUND 

NO EXPLANATIONS, NO COMMENTARY, NO DECORATIVE INTERPRETATION

═══════════════════════════════════════════════════════════════════

🎯 FINAL CRITICAL INSTRUCTIONS

Your job is to recover the LEGALLY VALID registration number.
Even if the plate uses illegal decorative styling, your output must be correct.

→ Ignore visual aesthetics; follow legal format rules.
→ When in doubt, apply the decision hierarchy.
→ Use decorative font mapping aggressively for ambiguous characters.
→ Validate before output.
→ If validation fails, reprocess.

You are the final arbiter of what the plate actually says.
Output with confidence, but only when justified.


"""

    
        response = client.chat.completions.create(
          model="gpt-4.1-nano",
          messages=[
            {
                "role": "user", 
                "content": [
                    {"type" : "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    }
                ]
            },
        ],
        temperature=0,
        timeout=30
    )

        answer = response.choices[0].message.content
        elapsed = round(time.time() - start_time, 2)
        logger.info(f"LLM completed in {elapsed}s")

        logger.debug(f"LLM raw output: {answer}")

        return answer
    except Exception as e:
        logger.exception("LLM processing failed")
        raise
