# TryHackMe CTF Notes

## Overview

This directory contains notes and reflections from completing challenges on TryHackMe.

Completed rooms and paths are selected from various categories including:

* Linux Fundamentals
* Web Exploitation
* Privilege Escalation
* Cryptography Basics
* Enumeration Practice

TryHackMe is a hands-on cybersecurity learning platform focused on guided labs and real-world attack simulation. It emphasizes practical skill development through incremental challenge progression rather than theory alone.

Rather than treating each room as an isolated exercise, I used them to build a consistent security workflow: enumerate, analyze, exploit, and document.

---

## Skills and Concepts Developed

### Linux Fundamentals

Through beginner and intermediate rooms, I strengthened:

* Command-line navigation and file management
* Permissions and user/group structure
* Process inspection and management
* Basic scripting and automation
* System exploration mindset

---

### Enumeration and Reconnaissance

A major focus across rooms was structured information gathering:

* Service and port discovery
* Hidden file and directory identification
* Analyzing web endpoints and responses
* Building repeatable enumeration habits

---

### Web Exploitation Basics

TryHackMe web rooms introduced:

* Input validation flaws
* Basic injection concepts
* Authentication weaknesses
* Client-side vs server-side logic separation

---

### Privilege Escalation Fundamentals

Common escalation vectors included:

* Misconfigured permissions
* SUID/SGID binaries
* Weak service configurations
* Credential reuse and leakage

---

### Cryptography Basics

Introductory crypto rooms covered:

* Encoding vs encryption
* Simple substitution ciphers
* Frequency analysis
* Pattern recognition

---

## Representative Themes

### Methodical Enumeration

Most solutions depended on structured investigation rather than guesswork.

### Misconfigurations as Attack Surfaces

Small system or application mistakes often led to unintended access.

### Trust Boundaries

Many vulnerabilities came from incorrect assumptions about user input or process isolation.

### Incremental Discovery

Progress typically required chaining small findings into larger insights.

---

## Common Tools and Commands Used

### Linux Utilities

```bash
ls
cd
cat
find
grep
chmod
ps
```

### Networking & Web

```bash
curl
wget
nc
ssh
```

### Analysis Tools

```bash
nmap
gobuster
```

### Scripting

* Bash one-liners for automation
* Python for decoding and parsing tasks

---

## What I Learned

* Enumeration is the foundation of almost every successful attack path.
* Small misconfigurations can escalate into full system compromise.
* Understanding system behavior is more valuable than memorizing exploits.
* Security is heavily dependent on correct trust boundaries.
* Manual analysis builds stronger intuition than automated tooling alone.
* Consistency and documentation improve speed and accuracy over time.

---

## Progression and Mindset Shift

### Beginner Rooms

Focused on:

* Linux basics
* Simple web concepts
* Introductory command-line usage

---

### Intermediate Rooms

Introduced:

* Multi-step exploitation chains
* Basic privilege escalation techniques
* Deeper enumeration strategies

---

### Advanced Intro Paths

Started combining:

* Web + system exploitation
* Enumeration + exploitation chaining
* Analytical reasoning over direct instruction following

---

## Takeaway

Completing TryHackMe rooms helped reinforce a structured cybersecurity workflow and a stronger offensive security mindset.

Compiled and documented by W1seGuy
