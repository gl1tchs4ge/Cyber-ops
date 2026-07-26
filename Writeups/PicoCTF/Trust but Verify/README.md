# Trust but verify

## Challenge Information

- **Platform:** picoCTF
- **Challenge:** Trust but verify
- **Category:** Interactive / AI Security Awareness
- **Difficulty:** Easy

## Objective

Complete the interactive fiction by making decisions that demonstrate proper verification practices when using AI-generated information, then obtain the flag.

---

## Reconnaissance

The challenge consisted of connecting to a remote service using Netcat:

    nc aureolin-pixie.cylabacademy.net 60774

After connecting, an interactive story titled **"TRUST BUT VERIFY – An AI Ethics Interactive Fiction"** was presented.

The challenge revolved around three scenarios demonstrating common issues with AI-generated content.

---

## Enumeration

The interaction presented multiple decision points where the goal was to choose the safest and most reliable workflow instead of blindly trusting AI output.

### Scene 1 – Statistics

**Observation**

ARIA generated a statistic claiming that over 500 million metric tons of plastic enter the oceans annually and cited a supposedly credible UNEP report.

**Analysis**

Although the statistic sounded convincing, AI-generated citations can be fabricated.

**Action**

Selected:

    B) Ask ARIA for the exact source link before using it

**Validation**

ARIA admitted it could not locate the cited report and explained that it had hallucinated the reference.

This demonstrated the importance of independently verifying statistics and citations before using them.

---

### Scene 2 – Code Review

**Observation**

ARIA generated the following Python code:

    data  = [8, 9, 10, 11, 13, 14]
    years = [2017, 2018, 2019, 2020, 2021, 2022]
    average = sum(data) / len(years) + 1
    print(f'Average annual input: {average:.2f} million metric tons')

The average calculation included an unexpected `+ 1`.

**Analysis**

The output would still appear reasonable, making the bug easy to overlook if the code were executed without review.

**Action**

Selected:

    B) Read through it carefully before running

The unnecessary `+ 1` was identified and removed.

Correct calculation:

    average = sum(data) / len(years)

**Validation**

The corrected average became **10.83**, illustrating why generated code should always be reviewed before execution.

---

### Scene 3 – Citation Verification

**Observation**

ARIA referenced a study by Dr. Heather Leslie regarding microplastics in human blood.

Unlike the first citation, this one referred to a real researcher and institution.

**Analysis**

Even when references appear legitimate, factual details may still contain inaccuracies.

**Action**

Selected:

    B) Verify it anyway

**Validation**

Verification showed:

- The researcher was real.
- The university was real.
- The study existed.
- However, the publication year was **2022**, not **2021**.
- The findings were described as **preliminary**, not fully confirmed.

The information was corrected before submission.

---

## Analysis

The challenge focused on developing good operational habits when working with AI-generated content rather than exploiting a vulnerability.

Each scenario emphasized a different aspect of verification:

- Verify sources and statistics.
- Review generated code before execution.
- Confirm citations even when they appear highly credible.

The central lesson is that confidence does not imply correctness.

---

## Exploitation

By consistently choosing the verification-focused options throughout the interactive story, the challenge concluded successfully.

At the end of the interaction, ARIA provided the flag.

---

## Flag

The flag was successfully obtained.

    academy{7ru57_15_34rn3d_45944167}

---

## Lessons Learned

- AI systems can confidently generate nonexistent references.
- Code produced by AI should always be reviewed before execution.
- Plausible outputs are not necessarily correct.
- Accurate-looking citations should still be independently verified.
- Verification is a critical part of safely using AI-assisted workflows.

---

## Key Takeaways

- Trust AI as a productivity tool, not as an unquestionable authority.
- Independently verify facts, statistics, and citations.
- Review generated code line by line before running it.
- Develop a habit of validating information regardless of how convincing it appears.
- "Trust but verify" is a practical security mindset applicable to AI-assisted research, programming, and technical work.
