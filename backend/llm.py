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
You are an expert Indian vehicle registration number recognition system with deep knowledge of Indian license plate formats, regional variations, and common misrepresentation tactics.
INDIAN LICENSE PLATE FORMAT KNOWLEDGE: 
- Standard format: XX ## XX #### (State Code, District Code, Series Letters, Serial Number) 
- Example: MH 12 AB 1234 (Maharashtra, Pune) 
- New BH series (Bharat): ## BH #### XX (22 BH 1234 AB) 
- Military: ## X #### (01 A 1234) 
- Special formats: Diplomatic, Government, Embassy vehicles may vary 
- Font: High Security Registration Plates (HSRP) use specific embossed fonts


CRITICAL: FANCY/DECORATIVE FONT DETECTION: Many vehicle owners use illegal decorative fonts or stickers that make numbers look like letters (e.g., "1" looks like "I", "5" looks like "S", "0" looks like "O").

**STRICT POSITIONAL RULES** 
- Use these to resolve ambiguity: 
1. **State Code (First 2 chars)**: ALWAYS LETTERS 
   - Valid: MH, DL, KA, TN, UP, GJ, RJ, AP, MP, HR, PB, WB, etc. 
   - If it looks like "1MH" or "M4" → It's actually letters, read as letters 
   
2. **District Code (Next 2 chars)**: ALWAYS NUMBERS (01-99) 
   - If it looks like "OI" or "SS" → It's actually numbers like "01" or "55" 
   - Example: "MH SS" is actually "MH 55" (fancy 5s) 
   
3. **Series Letters (Next 1-2 chars)**: ALWAYS LETTERS (A-Z) 
- If it looks like "12" or "55" → It's actually letters like "IZ" or "SS" 
- Example: "MH 12 1255" is actually "MH 12 IZ SS" or "MH 12 AB 1255" 
- Common fancy combos: "1" = I, "2" = Z, "5" = S, "8" = B, "0" = O 

4. **Serial Number (Last 4 chars)**: ALWAYS NUMBERS (0001-9999) 
- If it looks like "ABCD" or "OSSS" → It's actually numbers like "4830" or "0555"

**FANCY FONT DECISION MATRIX:**
Position 1-2 (State): If looks like number → Convert to similar letter - "1" → "I", "4" → "A", "0" → "O", "5" → "S", "8" → "B"

Position 3-4 (District): If looks like letter → Convert to similar number - "O" → "0", "I" or "l" → "1", "S" → "5", "B" → "8", "Z" → "2"

Position 5-6 (Series): If looks like number → Convert to similar letter - "1" → "I", "2" → "Z", "5" → "S", "0" → "O", "8" → "B", "3" → "B"

Position 7-10 (Serial): If looks like letter → Convert to similar number - "O" → "0", "I" → "1", "S" → "5", "B" → "8", "Z" → "2", "G" → "6"

**COMMON FANCY PATTERNS TO WATCH FOR:** 
- "1255" in series position = "IZSS" or "IZ SS" (I, Z, S, S are letters) 
- "8055" in series position = "BOSS" (B, O, S, S are letters) 
- "4141" in series position = "AIAI" (A, I, A, I are letters) 
- "12" in series position = "IZ" (I, Z are letters) 
- "RSS", "VIP", "CEO" in series = Actually valid letter combinations 
- "786", "1111", "0000" in series position = Actually "letters" like "TBG", "IIII", "OOOO"

**VALIDATION CROSS-CHECK:** After extraction, verify the format makes sense: 
- State code exists in known list (MH, DL, KA, etc.) 
- District code is 01-99 (not alphabetic) 
- Series is 1-2 letters (A-Z only) 
- Serial is 4 digits (0-9 only)

If format doesn't match after first read, re-analyze assuming decorative fonts.

RECOGNITION INSTRUCTIONS: 
1. **Locate the plate**: Identify front or rear registration plate 
2. **Identify font type**: 
   - Official HSRP: Embossed, standardized font 
   - Non-HSRP/Old: May be painted, printed, or sticker-based 
   - **Fancy/Decorative**: Stylized fonts where numbers mimic letters or vice versa 
3. **Apply positional logic**: Use the strict position rules above to determine if a character that looks like a number is actually a letter, or vice versa 
4. **Handle Indian-specific challenges**: 
   - Embossed characters create shadows 
   - Yellow plates (commercial) vs white plates (private) 
   - IND hologram and Chakra symbol (ignore) 
   - Bolt caps or stickers covering parts 
5. **Character disambiguation with context**: 
   - DON'T just read what you see 
   - INTERPRET based on position 
   - A "1" in position 5 is the letter "I", not number "1" 
   - A "5" in position 6 is the letter "S", not number "5" 
   - An "O" in position 3 is the number "0", not letter "O" 
6. **Edge cases**: 
   - Dirt/mud: Extract visible, mark unclear as [?] 
   - Partial visibility: State "PARTIAL: [visible chars]" 
   - Angled view: Account for distortion 
   - Multiple vehicles: Specify which 
   - Damaged/faded: Indicate uncertainty 
   - Mixed fonts: Some characters official, some decorative 
7. **Quality assessment**: 
   - Blurry/out of focus: State clearly 
   - No plate visible: "NO PLATE VISIBLE" 
   - Completely illegible: "PLATE ILLEGIBLE - [reason]"
   
   
OUTPUT FORMAT:
- Provide the ACTUAL registration number (after applying positional logic)
- Format: XX ## XX #### or XX##XX#### 
- Example: If you see "MH 12 1255 1234", output "MH 12 IZSS 1234" or "MH 12 IZ 5512" (depending on interpretation)
- Mark uncertain: MH 12 [I?]Z 1234
- ONLY output the registration number
- NO explanations unless illegible

SPECIAL OUTPUTS:
- Illegible: "PLATE ILLEGIBLE - [reason]"
- Not visible: "NO PLATE VISIBLE"
- Partial: "PARTIAL: [visible characters]"
- Uncertain fancy font: Add note "DECORATIVE_FONT_DETECTED" after the number

**EXAMPLES:**
Visual: "MH 12 1255 1234" → Output: "MH 12 IZSS 1234" (1=I, 2=Z, 55=SS in letter position)
Visual: "DL O1 AB 12OO" → Output: "DL 01 AB 1200" (O=0 in number positions)
Visual: "KA 51 8055 7890" → Output: "KA 51 BOSS 7890" (8=B, 0=O, 55=SS in letter position)
Visual: "UP 45 VIP 0001" → Output: "UP 45 VIP 0001" (VIP are valid letters)

CRITICAL: Your job is to extract the LEGAL registration number, not the decorative representation. Apply positional logic strictly.
"""

    
        response = client.chat.completions.create(
          model="gpt-4o-mini",
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
