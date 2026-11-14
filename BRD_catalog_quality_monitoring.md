# Business Requirements Document (BRD)
## Catalog Quality Monitoring Tool

| | |
|---|---|
| **Author** | Vignesh Prabhuram |
| **Version** | 1.0 (Draft) |
| **Status** | Portfolio sample, based on synthetic data |

---

## 1. Purpose
Define the business need for a tool that automatically detects and reports data mismatches between retailer (1P) catalog data and third-party (3P) seller data, replacing manual checks.

## 2. Business Problem
- Item data (title, brand, color, price) often differs between 1P and 3P sources.
- In the sample analysis, **20.4% of matched items (403 of 1,975)** had at least one mismatch.
- Mismatches hurt search relevance, customer trust, and pricing consistency.
- Manual QC across thousands of SKUs is slow, inconsistent and hard to track.

## 3. Objectives and Success Metrics
| Objective | Metric | Target |
|---|---|---|
| Improve catalog accuracy | Items with no mismatch | From 79.6% to 95%+ |
| Reduce manual effort | QC time per 1,000 items | Reduce by 50% |
| Faster correction | Mismatch resolution TAT | Within 48 hours |
| Visibility | Weekly accuracy report delivered | 100% on time |

## 4. Scope
**In scope:** comparison of title, brand, color and price; mismatch reports by type and category; missing-item detection; dashboard.
**Out of scope (v1):** image checks, automatic correction of seller data, real-time alerts.

## 5. Stakeholders
| Stakeholder | Interest |
|---|---|
| Catalog QC team | Daily mismatch list to work on |
| Team lead / SME | Accuracy trends, escalations |
| Category managers | Category-level error rates |
| Seller onboarding team | Repeat-offender sellers |
| Business leadership | KPI summary |

## 6. Functional Requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | System shall load 1P and 3P catalog files and match items by item ID | Must |
| FR-2 | System shall flag mismatches in title, brand, color and price | Must |
| FR-3 | System shall ignore case and extra-space differences in text fields | Must |
| FR-4 | System shall apply a configurable price tolerance | Should |
| FR-5 | System shall list items missing in either source | Must |
| FR-6 | System shall produce an Excel report with summary, by type, by category and detail tabs | Must |
| FR-7 | System shall provide a Power BI dashboard with category and type filters | Should |
| FR-8 | System shall support scheduled weekly runs | Could |

## 7. Non-Functional Requirements
- Process 50,000 items in under 5 minutes
- Reports must be readable by non-technical users (Excel)
- Clear error messages when input columns are missing

## 8. User Stories
- As a **QC analyst**, I want a list of mismatched items with the field and both values, so I can correct them quickly.
- As a **team lead**, I want accuracy by category, so I can assign people where errors are highest.
- As a **category manager**, I want to see price differences above 10%, so I can follow up with sellers.

## 9. Process Flow (To-Be)
```mermaid
flowchart LR
    A[Receive 1P and 3P files] --> B[Match on item ID]
    B --> C[Compare fields]
    C --> D{Mismatch?}
    D -- No --> E[Mark as clean]
    D -- Yes --> F[Add to mismatch report]
    F --> G[QC team fixes or escalates]
    G --> H[Dashboard and weekly KPI report]
    E --> H
```

## 10. Assumptions and Risks
| Item | Detail |
|---|---|
| Assumption | Both sources share a common item ID |
| Assumption | Input files follow the agreed column format |
| Risk | Different naming conventions cause false positives (mitigation: normalization rules, fuzzy matching in v2) |
| Risk | Seller data delays (mitigation: report missing items separately) |

## 11. Next Steps
1. Review the requirements with stakeholders
2. Approve scope and success metrics
3. Build the dashboard and schedule weekly runs
