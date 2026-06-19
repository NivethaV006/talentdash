from level_rules import LEVEL_RULES
from llm_fallback import llm_classify
# Future Gemini fallback



def map_level(role, experience):

    role = role.lower().strip()

    # Exact mappings
    if role in LEVEL_RULES:

        # Software Engineer
        if role == "software engineer":

            if experience < 2:
                level = "SDE-I"

            elif experience < 5:
                level = "SDE-II"

            else:
                level = "SDE-III"

            return {
                "level": level,
                "confidence": 0.90,
                "method": "RULE"
            }

        # Data Analyst
        if role == "data analyst":

            if experience < 2:
                level = "L3"

            elif experience < 5:
                level = "L4"

            else:
                level = "L5"

            return {
                "level": level,
                "confidence": 0.90,
                "method": "RULE"
            }

        return {
            "level": LEVEL_RULES[role],
            "confidence": 0.90,
            "method": "RULE"
        }

    # LLM fallback
    return llm_classify(
        role,
        experience
    )