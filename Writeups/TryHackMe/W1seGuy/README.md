# w1seguy

## Overview
TCP-based cryptography challenge running on port `1337`. The service implements a repeating-key XOR operation combined with a session-based authentication mechanism. The objective is to recover the XOR key and retrieve two flags during a single interactive session via `nc`.

---

## Reconnaissance
- Service type: TCP socket server (`socketserver.ThreadingTCPServer`)
- Access method:
  ```bash
  nc <target-ip> 1337
  ```
- Interaction model: single-session, stateful exchange

### Observed behavior
- Server generates a random 5-character alphanumeric key
- Applies XOR encryption to a static string (decoy flag)
- Sends hex-encoded ciphertext to client
- Prompts for encryption key input
- Validates input against generated key
- Returns final flag upon correct authentication

---

## Attack Surface Analysis

### XOR Encryption Logic
- Repeating-key XOR
- Key length: 5 characters
- Pattern: `key[i % 5]`
- Output: hex-encoded ciphertext

### Known-Plaintext Condition
Flag format:

```
THM{...}
```

This enables direct XOR key recovery:

```
key[i % 5] = ciphertext[i] \u2295 plaintext[i]
```

### Structural Weaknesses
- Small keyspace
- Repeating structure in XOR stream
- No randomness or salt
- Authentication separate from encryption logic

---

## Exploitation Process

### Step 1: Connect
```bash
nc <target-ip> 1337
```

### Step 2: Observe output
- Ciphertext is immediately provided in same session

### Step 3: Identify structure
- Repeating-key XOR confirmed
- Key length = 5

### Step 4: Known-plaintext alignment
Using prefix `THM{` to derive partial key bytes via XOR relationships.

### Step 5: Repetition constraint
- Key repeats every 5 bytes
- Positions overlap (0=5, 1=6, etc.)
- This reinforces partial recovery consistency

### Step 6: Key reconstruction
- Remaining bytes resolved via:
  - alphanumeric constraint space
  - consistency with decrypted output format
  - validation against expected structure

### Step 7: Authentication
- Recovered key submitted in same session
- Server validates via direct equality check
- Correct key returns final flag

---

## Key Findings
- XOR behaves as a repeating stream cipher
- Known plaintext enables partial key recovery
- Repetition introduces structural leakage
- Core weakness is authentication design
- Exploitation combines cryptanalysis + session logic

---

## Flags
- Flag 1:
```
THM{p1alntExtAtt4ckcAnr3alLyhUrty0urxOr}
```

- Flag 2:
```
THM{BrUt3_ForC1nG_XOR_cAn_B3_FuN_nO?}
```

---

## Lessons Learned
- Repeating-key XOR is vulnerable under known-plaintext attacks
- Small authentication keyspaces are a critical design flaw
- Periodic encryption structures leak recoverable patterns
- Real vulnerabilities often come from system design, not algorithms
- Structured reasoning is more important than brute force
