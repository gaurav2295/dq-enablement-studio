---
id: prn-adr-027
type: principle
kind: decision
title: ADR D-27 — review_sql's retry-exception fallback re-judges/records/stamps, mirroring the empty-corrected_sql fallback (A2)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-27
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

review_sql's retry-exception fallback re-judges/records/stamps, mirroring the empty-corrected_sql fallback (A2).

## Rationale

core/harness/wrap.py's review_sql outer except (fired when the RETRY attempt itself raises) used to simply return the first attempt's payload unstamped and unrecorded — that verdict never reached harness_verdicts and the result carried no validator_findings/validator_retried. This was pinned (as the then-accepted behavior) by tests/test_harness_wrap.py's TestReviewSqlRetryExceptionFailSoft::test_retry_attempt_raises_falls_back_to_first_attempts_result, which T5b (commit 2d7ddd5, 2026-07-27) renamed and rewrote to test_retry_attempt_raises_re_judges_records_and_stamps_first_attempt, asserting the FIXED behavior instead. The old behavior was inconsistent with the sibling "retry-succeeds-but-empty-corrected_sql" fallback, which correctly re-judges first_candidate via local_pipeline.run, records once via self._pipeline.recorder, and stamps the native findings. Adversarial gate-approved amendment A2 (design doc header, 2026-07-27).

## Consequence

A2 landed with T5b (commit 2d7ddd5, 2026-07-27): the retry-exception path now mirrors the empty-corrected_sql fallback exactly — re-judges first_candidate, records the verdict once, and stamps validator_findings + validator_retried (=False, since the recorded verdict is the first attempt's, retry_count==0). Every review_sql outcome — clean, retried, empty-retry, or retry-errored — now produces exactly one recorded verdict and a stamped result, closing the last silent-drop hole. Flipped proposed -> active on 2026-07-27, citing tests/test_harness_wrap.py::TestReviewSqlRetryExceptionFailSoft::test_retry_attempt_raises_re_judges_records_and_stamps_first_attempt (the updated test asserting the fixed behavior).

> [!note] Provenance
> Architecture decision **D-27** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
