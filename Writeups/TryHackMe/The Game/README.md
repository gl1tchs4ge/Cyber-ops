# The Game

## Overview
The Game is a beginner-level TryHackMe challenge focused on static analysis of a Windows executable. The objective is to extract hidden information from a binary without executing it.

The challenge is designed to introduce fundamental binary inspection techniques, particularly how readable strings embedded in executables can reveal sensitive data. It reinforces the importance of secure compilation practices and awareness of plaintext leakage in binaries.

## Reconnaissance
- Downloaded and extracted the provided challenge archive
- Identified a Windows executable: `Tetris.exe`
- Performed initial static analysis using `strings`

Tools used:
- strings
- grep

Observations:
- The binary contains many readable ASCII strings
- No immediate flag found using generic keyword search
- Indicates the flag is likely embedded but not trivially indexed by naive search terms

## Attack Surface Analysis
- No execution or dynamic analysis required
- Likely plaintext storage of sensitive data within binary
- Expected flag format suggests TryHackMe convention: THM{...}

Hypothesis:
- The flag exists in the string table of the binary
- Requires filtered extraction using format-aware search patterns

## Exploitation Process
- Extracted all readable strings from the binary:
  strings Tetris.exe

- Attempted naive keyword search:
  strings Tetris.exe | grep "flag"
  Result: no relevant output

- Refined search using expected flag pattern:
  strings Tetris.exe | grep "^THM"

- Successfully extracted flag:
  THM{I_CAN_READ_IT_ALL}

## Key Findings
- Strings extraction is an effective first-step binary reconnaissance technique
- Generic keyword searches often fail against structured or unexpected formats
- Knowledge of flag format significantly improves efficiency
- Simple CLI utilities can outperform complex tooling in early-stage analysis

## Flag
THM{I_CAN_READ_IT_ALL}

## Lessons Learned
- Always begin binary analysis with lightweight static inspection
- Pattern-aware searching is more effective than generic keyword scanning
- Many beginner CTF binaries intentionally store flags in plaintext
- Basic Unix tools remain highly effective for initial exploitation workflows

## Suggested Improvements
- Use `strings -n 4` to reduce noise from short strings
- Try case-insensitive search: grep -i thm
- Scan for multiple known formats early (THM{, flag{, etc.)
- Consider deeper inspection tools (rabin2, binwalk) for advanced challenges
