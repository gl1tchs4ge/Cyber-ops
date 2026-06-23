# Narnia Wargame

## Overview

Narnia is a beginner-friendly Linux x86 exploitation wargame designed to introduce the fundamentals of binary exploitation and low-level program analysis.

Originally hosted on intruded.net and later revived by the OverTheWire community, Narnia provides a structured set of 10 levels, each focusing on a specific vulnerability class or exploitation concept.

The difficulty is relatively low compared to more advanced wargames, but it still requires patience, careful analysis, and a willingness to understand assembly and program behavior.

Each level provides both a compiled binary and its source code, allowing direct study of how vulnerabilities are introduced and how they can be exploited.

---

## What This Wargame Teaches

Narnia is focused on building foundational exploitation skills, including:

### Binary Exploitation Fundamentals
- Stack-based buffer overflows
- Format string vulnerabilities
- Unsafe memory handling in C
- Basic privilege escalation techniques

### Reverse Engineering Basics
- Reading and understanding C source code
- Mapping source code to compiled behavior
- Understanding control flow in binaries

### Assembly & Low-Level Understanding
- Introduction to x86 assembly
- Function calls and stack frames
- Register usage and memory layout

### Dynamic Analysis
- Using debuggers to inspect program execution
- Understanding crashes and memory corruption
- Step-by-step execution tracing

---

## Tools You Will Use

### Debugging & Reverse Engineering
- gdb (GNU Debugger)
- gef or pwndbg (gdb enhancements)
- radare2
- Ghidra (static analysis)

### Development & Exploitation
- gcc (compiling test binaries)
- python3 (scripting exploits)
- pwntools (exploit development framework)
- as (assembler)

### System Utilities
- SSH client (OpenSSH)
- Standard Linux utilities (`ls`, `cat`, `strings`, `file` `ltrace` `strace`)
- `/etc/motd` (system messages sometimes contain hints)

---

## Access Information

The wargame is hosted at: https://overthewire.org/wargames/narnia/

