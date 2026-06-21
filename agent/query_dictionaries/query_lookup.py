from agent.schema_structures.Schema import ClaimCategory

def get_system_query(category: ClaimCategory) -> str:
    match category:
        case ClaimCategory.CONSULTATION:
            return "Consultation"
        case ClaimCategory.DIAGNOSTIC:
            return "Diagnostic"
        case ClaimCategory.PHARMACY:
            return "Pharmacy"
        case ClaimCategory.DENTAL:
            return "DENTAL"
        case ClaimCategory.VISION:
            return "VISION"
        case ClaimCategory.ALTERNATIVE_MEDICINE:
            return "ALTERNATIVE_MEDICINE"
        
def get_human_query(category, ) -> str:
    match category:
        case ClaimCategory.CONSULTATION:
            return "Consultation"
        case ClaimCategory.DIAGNOSTIC:
            return "Diagnostic"
        case ClaimCategory.PHARMACY:
            return "Pharmacy"
        case ClaimCategory.DENTAL:
            return "DENTAL"
        case ClaimCategory.VISION:
            return "VISION"
        case ClaimCategory.ALTERNATIVE_MEDICINE:
            return "ALTERNATIVE_MEDICINE"