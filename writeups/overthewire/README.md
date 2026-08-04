# OverTheWire Wargames

## Overview

This directory contains notes and reflections from completing several challenges on the OverTheWire platform.

Completed wargames:

* Bandit
* Krypton
* Leviathan
* Natas

OverTheWire is a collection of security-focused wargames designed to teach practical skills through hands-on problem solving. Each game focuses on a different area of cybersecurity, gradually introducing more complex concepts and encouraging a methodology-driven approach.

Rather than treating the challenges as isolated puzzles, I used them to strengthen my understanding of Linux systems, web applications, cryptography, and offensive security thinking.

---

## Skills and Concepts Developed

### Linux Fundamentals

Through Bandit and Leviathan, I strengthened:

* File system navigation
* Permissions and ownership concepts
* Standard input/output redirection
* Working efficiently from the command line
* Understanding how programs interact with the operating system

### Enumeration and Information Gathering

Many levels required careful observation and systematic enumeration rather than guessing. This reinforced:

* Searching for useful information
* Identifying hidden or unusual files
* Recognizing attack surfaces
* Building a repeatable methodology

### Cryptography Fundamentals

Krypton introduced concepts such as:

* Classical ciphers
* Frequency analysis
* Encoding versus encryption
* Pattern recognition and analytical problem solving

### Binary and Program Analysis

Leviathan provided exposure to:

* SUID programs
* Runtime behavior analysis
* Trust boundaries inside applications
* Basic privilege escalation concepts

### Web Security Concepts

Natas focused on:

* HTTP fundamentals
* Authentication mechanisms
* Client-side versus server-side trust
* Input validation weaknesses
* Common web application mistakes

---

## Representative Themes

### Linux Permission Misconfigurations

Several challenges demonstrated how improper permissions and SUID binaries can unintentionally expose privileged functionality.

### Information Disclosure

Many solutions depended on discovering information that had been unintentionally exposed through files, application behavior, or system configuration.

### Weak Trust Boundaries

Across both Leviathan and Natas, challenges highlighted the risks of trusting user-controlled input.

### Observation Over Automation

Success often came from understanding how a system behaved rather than relying on automated tools.

### Incremental Enumeration

Small pieces of information frequently led to larger discoveries, reinforcing the importance of a structured approach.

---

## Common Tools and Commands Used

### Linux Utilities

```bash
ls
cd
cat
find
grep
file
strings
sort
uniq
xxd
```

### Network and Web Tools

```bash
ssh
curl
nc
```

### Analysis Tools

```bash
ltrace
strace
```

### Scripting

* Bash one-liners
* Python for small transformations and decoding tasks

---

## What I Learned

* Enumeration is usually more important than exploitation.
* Small configuration mistakes can create significant security weaknesses.
* Understanding system behavior is more valuable than memorizing solutions.
* Trust boundaries are a recurring source of vulnerabilities.
* Manual investigation develops stronger intuition than relying exclusively on automation.
* Most challenges reward patience, observation, and methodical thinking.

---

## Difficulty Progression and Mindset Shift

### Beginner Stage — Bandit

Bandit established a foundation in:

* Linux usage
* Terminal workflows
* Basic problem solving

The focus was learning how to interact with systems effectively.

### Intermediate Transition — Krypton and Leviathan

These games shifted the emphasis toward:

* Analytical thinking
* Understanding program behavior
* Recognizing weaknesses in implementations

This stage introduced a more offensive mindset.

### Expanding Into Web Security — Natas

Natas required thinking about:

* Application logic
* User input handling
* Authentication mechanisms
* Trust relationships between client and server

At this point, challenges became less about commands and more about understanding how systems are designed.

---

## Takeaway

Completing these OverTheWire wargames marked an important transition from learning individual tools to developing a security mindset.

The experience emphasized methodology, curiosity, and understanding over memorization, providing a solid foundation for more advanced topics in offensive security and security research.

