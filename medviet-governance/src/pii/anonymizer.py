# src/pii/anonymizer.py
import pandas as pd
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from faker import Faker
from .detector import build_vietnamese_analyzer, detect_pii

fake = Faker("vi_VN")

class MedVietAnonymizer:

    def __init__(self):
        self.analyzer = build_vietnamese_analyzer()
        self.anonymizer = AnonymizerEngine()

    def _fake_cccd(self) -> str:
        return str(fake.random_number(digits=12, fix_len=True))

    def _fake_phone(self) -> str:
        return "0" + str(fake.random_element(elements=[3, 5, 7, 8, 9])) + str(fake.random_number(digits=8, fix_len=True))

    def anonymize_text(self, text: str, strategy: str = "replace") -> str:
        """
        TODO: Anonymize text với strategy được chọn.

        Strategies:
        - "mask"    : Nguyen Van A → N****** V** A
        - "replace" : thay bằng fake data (dùng Faker)
        - "hash"    : SHA-256 one-way hash
        - "generalize": chỉ dùng cho tuổi/năm sinh
        """
        results = detect_pii(text, self.analyzer)
        if not results:
            return text

        # TODO: implement operators dict dựa trên strategy
        operators = {}

        if strategy == "replace":
            operators = {
                "PERSON": OperatorConfig("replace", 
                          {"new_value": fake.name()}),
                "VN_NAME": OperatorConfig("replace", 
                          {"new_value": fake.name()}),
                "EMAIL_ADDRESS": OperatorConfig("replace", 
                                 {"new_value": fake.email()}),   # TODO: fake email
                "VN_CCCD": OperatorConfig("replace", 
                           {"new_value": self._fake_cccd()}),          # TODO: fake CCCD
                "VN_PHONE": OperatorConfig("replace", 
                            {"new_value": self._fake_phone()}),         # TODO: fake phone
            }
        elif strategy == "mask":
            # TODO: implement masking
            operators = {
                "PERSON": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 999, "from_end": False}),
                "VN_NAME": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 999, "from_end": False}),
                "EMAIL_ADDRESS": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 999, "from_end": False}),
                "VN_CCCD": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 12, "from_end": False}),
                "VN_PHONE": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 10, "from_end": False})
            }
        elif strategy == "hash":
            # TODO: implement hashing dùng sha256
            operators = {
                "PERSON": OperatorConfig("hash", {}),
                "VN_NAME": OperatorConfig("hash", {}),
                "EMAIL_ADDRESS": OperatorConfig("hash", {}),
                "VN_CCCD": OperatorConfig("hash", {}),
                "VN_PHONE": OperatorConfig("hash", {})
            }

        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )
        return anonymized.text

    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        TODO: Anonymize toàn bộ DataFrame.
        - Cột text (ho_ten, dia_chi, email): dùng anonymize_text()
        - Cột cccd, so_dien_thoai: replace trực tiếp bằng fake data
        - Cột benh, ket_qua_xet_nghiem: GIỮ NGUYÊN (cần cho model training)
        - Cột patient_id: GIỮ NGUYÊN (pseudonym đã đủ an toàn)
        """
        df_anon = df.copy()

        # TODO: Xử lý từng cột PII
        # Gợi ý: dùng df.apply() hoặc list comprehension
        for col in ["ho_ten", "dia_chi", "email"]:
            df_anon[col] = df_anon[col].astype(str).apply(self.anonymize_text)
        df_anon["cccd"] = df_anon["cccd"].apply(lambda _: self._fake_cccd())
        df_anon["so_dien_thoai"] = df_anon["so_dien_thoai"].apply(lambda _: self._fake_phone())
        return df_anon

    def calculate_detection_rate(self, 
                                  original_df: pd.DataFrame,
                                  pii_columns: list) -> float:
        """
        TODO: Tính % PII được detect thành công.
        Mục tiêu: > 95%

        Logic: với mỗi ô trong pii_columns,
               kiểm tra xem detect_pii() có tìm thấy ít nhất 1 entity không.
        """
        total = 0
        detected = 0

        for col in pii_columns:
            for value in original_df[col].astype(str):
                total += 1
                value_str = value
                if col == "cccd" and value_str.isdigit():
                    value_str = value_str.zfill(12)
                elif col == "so_dien_thoai" and value_str.isdigit():
                    value_str = value_str.zfill(10)

                results = detect_pii(value_str, self.analyzer)
                if len(results) > 0:
                    detected += 1

        return detected / total if total > 0 else 0.0
