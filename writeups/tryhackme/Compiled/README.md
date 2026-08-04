# Compiled (TryHackMe)

## Overview

This challenge involved a compiled Linux binary that prompts for a password. The goal was to reverse engineer the binary behavior and determine the correct input to trigger the success condition and retrieve the flag.

The primary technique used was static string analysis combined with dynamic tracing using `ltrace`.

---

## Reconnaissance

- Downloaded a compiled Linux executable (`Compiled`)
- Confirmed binary type using file inspection (implicitly ELF 64-bit based on libc references)
- Initial enumeration performed using:

    strings Compiled

### Key observations from `strings`:

- Presence of standard libc functions:
  - `strcmp`
  - `printf`
  - `__isoc99_scanf`
  - `fwrite`
- Suspicious string fragments:

    DoYouEven%sCTF
    Password:
    Correct!
    Try again!

These suggested:
- A password comparison via `strcmp`
- A formatted or partially constructed expected input

---

## Attack Surface Analysis

- Binary likely reads user input via `scanf`
- Input is validated using `strcmp`
- Obfuscation likely occurs through:
  - String concatenation or segmentation
  - Internal function or symbol leakage (`_init`, `__dso_handle`)

### Hypotheses:
- Password is constructed dynamically or requires prefix/suffix manipulation
- `ltrace` can reveal runtime string comparisons
- False leads exist in symbol table strings exposed via `strings`

---

## Exploitation Process

### Step 1: Dynamic tracing

Executed:

    ltrace ./Compiled

Observed:

    fwrite("Password: ", ...)
    __isoc99_scanf(...)
    strcmp("", "__dso_handle")
    strcmp("", "_init")
    printf("Try again!")

#### Observation
- Initial comparisons were incorrect or empty string mismatches
- `_init` appeared as a comparison target, suggesting symbol leakage

---

### Step 2: First attempt using symbol-based guess

Input tested:

    DoYouEven_initCTF

Result:

    strcmp("_initCTF", "__dso_handle")
    strcmp("_initCTF", "_init")
    Try again!

#### Finding
- Input was being partially truncated or parsed
- Only `_initCTF` portion was effectively used in comparison

---

### Step 3: Refined input based on truncation behavior

Input tested:

    DoYouEven_init

`ltrace` output:

    strcmp("_init", "__dso_handle")
    strcmp("_init", "_init")
    printf("Correct!")

#### Result
- First comparison failed
- Second comparison succeeded (`strcmp == 0`)
- Program accepted input and printed success message

---

## Key Findings

- The binary uses `strcmp` for validation
- Input parsing likely splits or ignores prefix portions
- Effective comparison target is `_init`
- Correct input is constructed by embedding the expected internal string into the required format

---

## Flag

    DoYouEven_init

---

## Lessons Learned

- `strings` alone can mislead due to symbol table noise in compiled binaries
- `ltrace` is highly effective for runtime function-level observation (`strcmp`, `scanf`)
- Binary may not use full input string; partial parsing or format constraints can exist
- Internal ELF symbols (like `_init`) can leak logic clues but may also act as red herrings
- Always validate whether input is fully consumed or truncated during `scanf` processing
