# src/pii/detector.py
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    TODO: Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\b\d{12}\b",          # TODO: điền regex cho 12 chữ số
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        supported_language="vi",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"]
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        supported_language="vi",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"\b0(?:3|5|7|8|9)\d{8}\b",      # TODO: điền regex
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"]
    )

    # --- TASK 2.2.2b ---
    # Tạo name recognizer: họ tên VN (2-4 từ, chỉ chữ cái Unicode)
    name_pattern = Pattern(
        name="vn_name",
        regex=r"(?u)(?:[^\W\d_]+(?:[-'][^\W\d_]+)*\.?)(?:\s+[^\W\d_]+(?:[-'][^\W\d_]+)*\.?){1,3}",
        score=0.7
    )
    name_recognizer = PatternRecognizer(
        supported_entity="VN_NAME",
        supported_language="vi",
        patterns=[name_pattern],
        context=["họ tên", "bệnh nhân", "bn", "tên"]
    )

    # --- TASK 2.2.2c ---
    # Tạo email recognizer
    email_pattern = Pattern(
        name="email_pattern",
        regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        score=0.85
    )
    email_recognizer = PatternRecognizer(
        supported_entity="EMAIL_ADDRESS",
        supported_language="vi",
        patterns=[email_pattern],
        context=["email", "e-mail", "mail"]
    )

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": "xx_ent_wiki_sm"}]   # TODO: điền model name
    })
    nlp_engine = provider.create_engine()

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["vi"])
    analyzer.registry.add_recognizer(cccd_recognizer)   # TODO
    analyzer.registry.add_recognizer(phone_recognizer)   # TODO
    analyzer.registry.add_recognizer(name_recognizer)
    analyzer.registry.add_recognizer(email_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    TODO: Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: EMAIL_ADDRESS, VN_CCCD, VN_PHONE, VN_NAME
    """
    results = analyzer.analyze(
        text=text,       # TODO
        language="vi",   # TODO
        entities=["EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE", "VN_NAME"]    # TODO
    )
    return results
