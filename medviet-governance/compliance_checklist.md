# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam (region VN-HN)
- [x] Backup cũng phải ở trong lãnh thổ VN (backup hằng ngày sang VN-HCM)
- [x] Log việc transfer data ra ngoài nếu có (egress log + alert)

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training (form điện tử + chữ ký số)
- [x] Có mechanism để user rút consent (Right to Erasure) qua cổng CSKH
- [x] Lưu consent record với timestamp (audit trail, immutable log)

## C. Breach Notification (72h)
- [x] Có incident response plan (IRP v1.0, RACI rõ ràng)
- [x] Alert tự động khi phát hiện breach (SIEM + Prometheus + PagerDuty)
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h (mẫu báo cáo + checklist)

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | CloudTrail + API access logs | ⬜ Todo | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ⬜ Todo | Security Team |

## F. TODO: Điền vào phần còn thiếu
Với mỗi row còn "⬜ Todo", mô tả technical solution cụ thể bạn sẽ implement.

- Audit logging: bật API access logs ở gateway, lưu vào object storage bất biến (WORM), ingest vào SIEM (ELK/Splunk), giữ log tối thiểu 12 tháng, có dashboard và cảnh báo truy cập bất thường.
- Breach detection: dùng Prometheus + Alertmanager theo dõi spike 403/401, anomaly detection trên truy cập dữ liệu nhạy cảm, tích hợp SIEM để phát hiện IOC và gửi cảnh báo trong 5 phút.
