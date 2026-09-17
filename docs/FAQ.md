> [!IMPORTANT]
> **This guide predates the 2026-08-20 rebuild.** The academy HTML it references now lives in
> `archive/academy-v1/`; the live experience is `dist/enablement-master.html` (see README.md
> and SETUP.md). Timing guidance and pedagogy below still apply — Sessions 1-3 exist as
> learning paths in the app. A full rewrite is on the open-items list.

# Frequently Asked Questions

## For Learners

### General Questions

**Q: How long does it take to complete all three sessions?**
A: Approximately 3-4 hours of active learning, plus 1-2 hours of practice. You can do it in one day or spread it over a week.

**Q: Do I need to complete Session 1 before Session 2?**
A: Recommended. Session 2 assumes you understand OptSel/RptSel, error flags, and the DQ lifecycle from Session 1. If you already know these concepts, you can skip ahead.

**Q: Do I need both Session 2 and Session 3?**
A: Session 2 (SQL) teaches the standards. Session 3 (Studio) teaches how to use the tool. Both are valuable together. You can take Session 3 without Session 2 if you just want to use the UI, but Session 2 helps you understand what the tool generates.

**Q: Can I take this on my mobile phone?**
A: Yes! The pages are responsive and work on mobile. However, reading SQL examples and taking quizzes is easier on a larger screen.

**Q: Is there a certificate or badge when I finish?**
A: Not automatically. Ask your facilitator about internal recognition or certificates for completing all sessions.

---

### Session 1 Questions

**Q: What's the difference between OptSel and RptSel?**
A: **OptSel** = "Options" view, returns ALL rows (both clean and error) with a 1/0 error flag. **RptSel** = "Report" view, wrapper that filters OptSel to show only errors (the 1s). OptSel lets you measure the whole universe; RptSel is what business users see to remediate.

**Q: Why does data quality matter if our systems work?**
A: Systems process whatever data you give them. Bad data = bad results, bad decisions, customer issues, rework. A single bad record in master data can break downstream analytics, forecasting, and compliance. The cost of bad data is often hidden until it's too late.

**Q: What's the difference between a deletion flag (LVORM) and a status field (PSTAT)?**
A: **Deletion flags** (LVORM, LOEKZ) = "Is this record deleted?" Answer: yes or no. You exclude these from rules (WHERE clause). **Status fields** (PSTAT, MMSTA) = "What's the status?" Answer: active, inactive, draft, etc. These can drive your error condition (CASE). Example: A rule might only check active materials, so status goes in WHERE (scope). But a rule checking "is status valid?" puts PSTAT in CASE (error condition).

---

### Session 2 Questions

**Q: Why do I need to learn SQL if the Studio generates it?**
A: The Studio generates SQL, but YOU define the rule. You need to understand what makes SQL correct, what Session 2 standards mean, and how to evaluate Claude's suggestions. Also, some rules are too complex for the UI — you need to understand the SQL to review and modify them.

**Q: What's zSourceSystemID and why is it everywhere?**
A: It's the column that identifies which SAP system a row belongs to (Z01=Production, Z02=Quality, etc.). It appears in four mandatory places to prevent **silent data leakage** — where data from two different systems accidentally mixes in a join and you get wrong results. It's THE most important concept in Session 2.

**Q: Why are comments so strict? Can't I just write the SQL and let it speak for itself?**
A: Because rules are auditable — someone unfamiliar with your data needs to understand why a record is flagged as an error. The comment explains the **business logic**, not the SQL syntax. Someone should be able to read the comments and understand the rule without knowing anything about SQL.

**Q: Why does field order matter?**
A: It's a standard. Every rule looks the same: Technical (zSourceSystemID, zConcatenatedKey, zIsErrorFlag) first, then Basic (identification), then Org, Value, Activity. This consistency makes rules easier to read and compare across hundreds of rules.

**Q: Why can't I use deletion flags in the CASE statement?**
A: Because CASE is for error conditions (what makes a record bad). Deletion flags are scope (which records to even check). If you put LVORM in CASE, you're treating a deleted record as an "error to remediate" — but you don't remediate a deleted record; you exclude it from checking entirely. WHERE is for scope; CASE is for logic.

---

### Session 3 Questions

**Q: How do I get access to the DQ Studio?**
A: Contact your DQ enablement lead or your manager. Studio access is provisioned per organization. Your facilitator can show you how to get set up.

**Q: What's the difference between local derivation and AI enhancement?**
A: **Local derivation** = Studio generates SQL based on your input (deterministic, always the same for same input). **AI Enhancement** = You optionally send the derived rule to Claude, who can improve it, optimize it, or suggest alternatives. Local is always available; AI is optional.

**Q: Will Claude's version always be better than the local derivation?**
A: Not always. Local derivation is production-ready. Claude can optimize, catch edge cases, or simplify. But sometimes your local rule is already good. You review Claude's suggestion and decide: accept, modify, or stick with what you have.

**Q: What are sibling rules?**
A: When you derive a rule for multiple systems (Z01, Z02, Z03), the Studio creates siblings — one rule per system with identical logic, different zSourceSystemID filters. Siblings ensure system isolation and make it easy to compare results across systems.

**Q: Do I need to run AI enhancement on every sibling?**
A: No. AI enhancement happens once (on the primary rule). The Studio then mechanically creates siblings by substituting the system ID. Same logic, all siblings — efficient and consistent.

**Q: How long does bulk execution take?**
A: Depends on how many rules and how much data. Simple rules on 100K rows: ~5 minutes. Complex rules on 10M rows: ~30 minutes. Hundreds of rules in parallel: ~15–30 minutes typically. Your DQ team can advise based on your systems.

**Q: What do I do with the results from bulk execution?**
A: You get error counts per rule. High error counts might mean: (1) your rule is too strict, (2) your data has real issues, or (3) your rule logic is wrong. Investigate high-error rules. Then either fix the rule or fix the data. Use error trends to track progress over time.

---

## For Instructors

### Facilitation Questions

**Q: How do I know if learners actually understood the content?**
A: Give them a practical task: "Design a rule for [your business]. What table? What's the error condition? What scope?" Review their answer using the Session 2 checklist. Can they explain OptSel vs RptSel? Ask them.

**Q: Some learners are SQL experts and others are non-technical. How do I pace this?**
A: Session 1 is for everyone (concepts, no SQL). Session 2 assumes basic SQL knowledge. For non-SQL-fluent learners: Emphasize that they don't write SQL (Studio does). Focus on logic and standards. For SQL experts: Challenge them to review real rules and spot compliance issues.

**Q: One learner says they already know data quality — can they skip ahead?**
A: Probably not much skipping needed. The material progresses: concepts (S1) → standards (S2) → tool usage (S3). Even experts may not know your org's standards or the Studio. Suggest they take the pre-assessment; if they score 12+, they can start Session 2. But don't let them skip Session 2 — the standards are non-negotiable.

**Q: How do I make the SQL less scary for non-technical people?**
A: Separate logic from syntax. "The logic is: if UoM is null OR invalid, flag it." That's the business rule. "The SQL is how we express that." Show the SQL, but focus on the comment that explains the business logic. Reassure them: "The Studio writes the SQL. Your job is defining the rule and reviewing it."

**Q: What if learners get stuck on zSourceSystemID?**
A: This is expected. Use a concrete scenario: "Two systems load their own copies of T006 (valid UoMs). If we join MARA from system 1 to T006 without filtering by system ID, we might match a material from system 1 against UoM codes from system 2. The rule gives wrong results, but looks like it works. zSourceSystemID filtering prevents that." Repeat this multiple times.

---

### Content Customization

**Q: Should I customize the HTML files for my organization?**
A: Yes, highly recommended. At minimum:
- Replace "Z01, Z02, Z03" with your actual system IDs
- Use tables from your own systems (materials, vendors, customers, not generic examples)
- Update the intro to mention your company's DQ strategy
- Add your logo in the header

This makes the content feel real to learners and more relevant.

**Q: Can I add or remove content?**
A: Yes. The content is open-source HTML. You can:
- Edit text directly (open .html in any text editor)
- Add new sections (copy an existing section and modify)
- Remove sections (comment out or delete the HTML)
- Add new questions to the pre-assessment

Test in a browser after edits to ensure it still looks good.

**Q: Should I host this on our intranet or the public web?**
A: Intranet is safer (controlled access). Public web is easier for remote/global teams. For proprietary content, keep it internal. The SETUP.md guide covers both options.

---

### Assessment Questions

**Q: What should I do if a learner scores low on the pre-assessment?**
A: Don't shame them. Low scores tell you they need to review Session 1 concepts (OptSel/RptSel, deletion flags, scope) before Session 2. Recommend 20–30 minutes of focused review on "Key Concepts" and "What a Good Rule Looks Like" sections. Offer to discuss one-on-one if they prefer.

**Q: Should I use the pre-assessment even if sessions are instructor-led?**
A: Yes. Give it at the start of your workshop (or before). It primes the brain on key topics and helps you see who needs extra attention. You can use it formatively (learning tool) not summatively (grading).

**Q: Can I add more questions to the pre-assessment?**
A: Yes. Open `assessments/sql-pre-assessment.html`, find the last question block, and duplicate it. Change the question number, question text, and answer options. Update the JavaScript answer key (near the bottom of the file) to include the new question.

---

### Troubleshooting

**Q: A learner says the content is too long.**
A: It can be read in 3–4 hours or spread over weeks. Emphasize: Sessions are modular. They can do Session 1 now, Session 2 next week. The knowledge checks are optional (helps learning but aren't mandatory).

**Q: Someone asks: "When will I actually use this?"**
A: Be specific to your org. "By Q4, we're rolling out the DQ Studio for master data rules. This training teaches how. You'll use it to derive rules for [specific tables] and review AI-suggested improvements."

**Q: A learner finds a mistake or outdated reference in the content.**
A: Thank them. Note it. Update the HTML file (if minor) or document it for the next version. Content should evolve based on learner feedback.

---

## Technical Questions

**Q: Does this require special software to deploy?**
A: No. It's plain HTML/CSS/JavaScript. Any web server or file share can host it. Or just open the .html files locally in a browser.

**Q: Are quizzes scored? Do I see results?**
A: Quizzes are scored in the learner's browser (no central database). Results are not sent anywhere — they're local to that session. You could collect results via survey if you want to track cohort performance.

**Q: Can I integrate this with our LMS (Moodle, Blackboard, etc.)?**
A: Yes. Add the HTML files as content resources in your LMS. Or embed them as iframes in LMS pages. See SETUP.md for LMS-specific instructions.

**Q: What if the HTML files won't load?**
A: Check: 
- Is the file in the right directory? 
- Is your web server set to serve .html files as HTML (not as text)? 
- Do you see errors in browser console (F12 → Console tab)? 
- Try a different browser to rule out browser-specific issues.

---

## Content Deep Dives

**Q: Why is OptSel/RptSel the foundational concept?**
A: Because everything in DQ rules builds on it. OptSel is how you measure ("we have 1M materials, 15K bad"). RptSel is how you act ("here are the 15K errors to fix"). Session 2 standards (field order, comments, etc.) are all about making OptSel correct and auditable. Session 3 (bulk, AI) all produces OptSel/RptSel pairs. Understand this, and everything else clicks.

**Q: Why does Session 2 forbid hardcoding zSourceSystemID as a literal?**
A: Because you might copy that rule to another system and forget to change the literal. Then it only checks system Z01 even if you meant Z02. Column references are safe — the rule automatically uses the right system wherever it runs.

**Q: Why does the comment standard forbid mentioning AI or automation?**
A: Because rules are auditable documents. If someone reads "this SQL was generated by Claude," they might assume it wasn't reviewed or is less trustworthy. The comment should read as a normal engineering note regardless of how the SQL was written. All rules (hand-written, derived, AI-enhanced) must meet the same standard.

---

## Learner Success Stories

**Q: I completed Session 1 but don't understand OptSel/RptSel yet. What should I do?**
A: That's normal. This is the hardest concept. Re-read that section. Draw a picture: OptSel box (all rows, 1s and 0s), RptSel box inside it (only 1s). Use a concrete example from your work. Ask your facilitator to explain with your actual table. Then re-read the content. It will click.

**Q: I finished all sessions and still don't feel ready to derive rules.**
A: Completely normal. Practice is next. Derive your first rule with your facilitator present. You'll surprise yourself — it's easier than you expect. The Studio UI guides you; you just define the logic.

**Q: I took the pre-assessment and scored 8/15. Should I give up?**
A: No! This tells you to review Session 1 before Session 2. Spend 30 min reviewing "Key Concepts" and "What a Good Rule Looks Like." Then retake the pre-assessment. Most people improve significantly.

---

**Last updated:** August 2026  
**Have a question not listed here?** Suggest it — this FAQ evolves based on learner needs.
