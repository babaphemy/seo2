import enum


class ResourceEnum(enum.Enum):
    POLL = "Poll"
    FORM = "Form"
    QUESTIONNAIRE = "QUESTIONNAIRE"
    TEXT = "Text"
    VIDEO = "Video"
    AUDIO = "AUDIO"
    FILE = "File"
    LINK = "Link"


class AccessRoleEnum(enum.Enum):
    ADMIN = "Admin"
    USER = "User"
    GUEST = "Guest"
    PARENT = "Parent"
    TEACHER = "Teacher"
    ACCOUNT = "Account"
    REFEREE = "Referee"
    STUDENT = "Student"


class GradeLevel(enum.Enum):
    PRESCHOOL = "PRESCHOOL"
    DAYCARE = "DAYCARE"
    KG1 = "Kindgergaten 1"
    KG2 = "Kindergaten 2"
    KG3 = "Kindgergaten 3"
    PRIMARY1 = "Primary 1"
    PRIMARY2 = "Primary 2"
    PRIMARY3 = "Primary 3"
    PRIMARY4 = "Primary 4"
    PRIMARY5 = "Primary 5"
    PRIMARY6 = "Primary 6"
    JSS1 = "Junior Secondary School 1 (JSS1)"
    JSS2 = "Junior Secondary School 2 (JSS2)"
    JSS3 = "Junior Secondary School 1 (JSS3)"
    SSS1 = "Senior Secondary School 1 (SSS1)"
    SSS2 = "Senior Secondary School 2 (SSS2)"
    SSS3 = "Senior Secondary School 3 (SSS3)"
    POST_UTME = "Post UTME (Post JAMB)"
    PREDEGREE = "Pre-degree"
    OND1 = "Ordinary National Diploma 1 (OND)"
    OND2 = "Ordinary National Diploma 2 (OND2)"
    HND1 = "Higher National Diploma 1 (HND1)"
    HND2 = "Higher National Diploma 2 (HND2)"
    YEAR1 = "One Hunder Level (University)"
    YEAR2 = "Two Hunder Level (University)"
    YEAR3 = "Three Hunder Level (University)"
    YEAR4 = "Four Hunder Level (University)"
    YEAR5 = "Five Hunder Level (University/Postgraduate)"
    YEAR6 = "Six Hunder Level (University/Postgraduate)"
    YEAR7 = "Seven Hunder Level (University/Postgraduate)"
    YEAR8 = "Eight Hunder Level (University/Postgraduate)"


class Term(enum.Enum):
    FIRST = "First"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"


class StatusEnum(enum.Enum):
    NEW = "New"
    ENROLLED = "Enrolled"
    ADMITTED = "Admitted"
    DEBTOR = "Debtor"
    DELETED = "Deleted"
    SUSPENDED = "Suspended"
    EXPELLED = "Expelled"


class NigerianBank(enum.Enum):
    ACCESS_BANK = "Access Bank"
    CITIBANK = "Citibank"
    DIAMOND_BANK = "Diamond Bank"
    ECOBANK_NIGERIA = "Ecobank Nigeria"
    FIDELITY_BANK = "Fidelity Bank"
    FIRST_BANK_OF_NIGERIA = "First Bank of Nigeria"
    FIRST_CITY_MONUMENT_BANK = "First City Monument Bank"
    GUARANTY_TRUST_BANK = "Guaranty Trust Bank"
    HERITAGE_BANK_PLC = "Heritage Bank Plc"
    KEYSTONE_BANK_LIMITED = "Keystone Bank Limited"
    POLARIS_BANK = "Polaris Bank"
    PROVIDUS_BANK = "Providus Bank"
    STANBIC_IBTC_BANK = "Stanbic IBTC Bank"
    STANDARD_CHARTERED = "Standard Chartered"
    STERLING_BANK = "Sterling Bank"
    SUNTRUST_BANK_NIGERIA = "Suntrust Bank Nigeria"
    UNION_BANK_OF_NIGERIA = "Union Bank of Nigeria"
    UNITED_BANK_FOR_AFRICA = "United Bank for Africa"
    UNITY_BANK_PLC = "Unity Bank Plc"
    WEMA_BANK = "Wema Bank"
    ZENITH_BANK = "Zenith Bank"
