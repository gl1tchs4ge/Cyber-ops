# Corridor - TryHackMe

## Challenge Information

- Platform: TryHackMe
- Room: Corridor
- Category: Web / IDOR / Predictable Object References

## Objective

Investigate the application’s navigation system and identify hidden or unlinked endpoints by analyzing hexadecimal identifiers in the URL. The goal is to discover and access the hidden flag.

## Reconnaissance

Upon accessing the target:

    http://10.67.130.63/

The application displayed a corridor interface containing **13 doors**, each acting as a navigable endpoint.

Clicking on any door redirected the user to a URL structured as:

    http://10.67.130.63/<hex_value>

Example:

    http://10.67.130.63/c4ca4238a0b923820dcc509a6f75849b

## Enumeration

### Observation of Identifier Pattern

Each door corresponded to a **32-character hexadecimal string**, strongly suggesting MD5 hashing.

The first observed value:

    c4ca4238a0b923820dcc509a6f75849b

was identified as:

    MD5(1)

This indicated that door endpoints were likely generated using MD5 hashes of sequential integers.

## Analysis

### Hypothesis

- The application likely maps door numbers (1–13) to MD5 hashes of integers.
- Additional valid endpoints may exist beyond the visible UI if the system is predictable.
- If the system uses deterministic hashing, undisclosed values (such as 0 or values outside the displayed range) could produce valid but hidden routes.

## Exploitation Attempts

### Hash Generation and Fuzzing

A script was created to generate MD5 hashes for integers 1–100:

    for i in range(1, 101):
        md5(str(i)) -> stored in wordlist

The generated hashes were then used with `ffuf`:

    ffuf -w md5_hashes.txt -u http://10.67.130.63/FUZZ

### Result

- The fuzzing process only returned the same 13 visible door endpoints.
- No additional hidden endpoints were discovered within the tested range (1–100).

### Revised Hypothesis

Since sequential enumeration did not reveal new endpoints, the system may include special-case values not present in the visible range, such as:
- 0
- negative integers
- or non-obvious seed values used in hashing

## Discovery

Testing the value `0` produced a new insight.

Using CyberChef, the MD5 hash of `0` was computed:

    MD5(0) = cfcd208495d565ef66e7dff9f98764da

This hash was manually tested in the application:

    http://10.67.130.63/cfcd208495d565ef66e7dff9f98764da

## Exploitation Result

The endpoint successfully revealed the hidden flag:

    flag{2477ef02448ad9156661ac40a6b8862e}

## Flag

The flag was successfully obtained.

    flag{2477ef02448ad9156661ac40a6b8862e}

## Lessons Learned

- Predictable hashing schemes (e.g., MD5 of sequential integers) are a common source of IDOR vulnerabilities.
- Visible enumeration ranges do not guarantee full coverage of valid backend objects.
- Fuzzing should be combined with logical reasoning about edge cases (e.g., 0, negative values).
- When automation fails, testing boundary conditions manually can reveal overlooked attack surfaces.

## Key Takeaways

- MD5 hashes in URLs often encode simple integers.
- Always test edge cases when enumeration appears complete.
- IDOR vulnerabilities often rely on predictable object generation logic rather than direct exposure.
- Combining fuzzing with hypothesis-driven testing improves discovery efficiency.
