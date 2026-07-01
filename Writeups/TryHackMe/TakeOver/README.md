# TryHackMe – TakeOver

## Challenge Information
- Platform: TryHackMe
- Room: TakeOver
- Category: Web / Reconnaissance / Subdomain Enumeration
- Objective: Discover hidden subdomains and identify misconfigurations leading to sensitive information disclosure

---

## Objective

The goal of this challenge was to perform reconnaissance against the target domain, identify hidden virtual hosts and subdomains, and investigate exposed services to retrieve the flag.

The focus of this engagement was on:
- DNS and subdomain enumeration
- Virtual host discovery
- TLS certificate inspection
- HTTP service validation
- Identifying misconfigurations

---

## Initial Reconnaissance

The target domain under investigation was:

    futurevera.thm

Initial enumeration attempts focused on discovering subdomains using standard wordlists and tooling.

### Gobuster DNS Enumeration

An initial attempt was made using Gobuster for DNS brute force:

    gobuster dns --domain "futurevera.thm" \
    -w "/usr/share/dict/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt" \
    --no-error

This approach returned no meaningful results, indicating either:
- Non-standard subdomain naming
- Wildcard DNS configuration
- Or hidden services not exposed via DNS records

---

## Methodology Adjustment – FFUF VHOST Fuzzing

After unsuccessful DNS enumeration, the approach was shifted to virtual host fuzzing using FFUF.

### Initial VHOST Enumeration Attempt

    ffuf -w "/usr/share/dict/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt" \
    -u "https://futurevera.thm/" \
    -H "Host: FUZZ.futurevera.thm" \
    -fc 0,1512

This attempt produced no valid results.

---

### Improved Enumeration Strategy

The methodology was refined by:
- Switching to direct IP targeting
- Expanding wordlist coverage
- Filtering wildcard responses

Final enumeration command:

    ffuf -w "/usr/share/dict/seclists/Discovery/DNS/subdomains-top1million-5000.txt" \
    -u "https://10.67.164.243/" \
    -H "Host: FUZZ.futurevera.thm" \
    -fs 4605

### Results

Two valid virtual hosts were identified:

- support.futurevera.thm
- blog.futurevera.thm

These results confirmed:
- Name-based virtual hosting
- Multiple applications hosted on a single backend IP
- Filtering was required to remove default responses

---

## TLS Inspection & Certificate Analysis

Each discovered virtual host was further analyzed using TLS inspection.

### support.futurevera.thm

- Self-signed certificate
- Subject CN mismatch with SAN validation failure
- Expired certificate
- Indicates misconfigured SSL setup

### blog.futurevera.thm

- Self-signed certificate
- CN matches hostname correctly
- Expired certificate
- Proper SNI-based certificate routing observed

---

## Certificate Enumeration – Hidden Subdomain Discovery

During inspection of the TLS certificate for:

    support.futurevera.thm

A Subject Alternative Name entry revealed an additional hidden subdomain:

    secrethelpdesk934752.support.futurevera.thm

This hostname was not discovered during DNS or VHOST brute force enumeration, indicating:
- Certificate metadata leakage
- Hidden internal service exposure
- Nested subdomain structure under the support domain

---

## Host Resolution Setup

To facilitate direct access, the following entries were added to `/etc/hosts`:

- futurevera.thm
- blog.futurevera.thm
- support.futurevera.thm
- secrethelpdesk934752.support.futurevera.thm

This ensured consistent routing to the target IP and bypassed DNS ambiguity.

---

## Exploitation – Secret Helpdesk Endpoint

The newly discovered subdomain was accessed for further investigation.

### HTTPS Request

    curl https://secrethelpdesk934752.support.futurevera.thm/

Result:
- TLS handshake succeeded
- Certificate mismatch error occurred
- Server returned a fallback certificate for `futurevera.thm`
- HTTPS endpoint was not properly configured for this host

This indicated that HTTP was the intended access method.

---

### HTTP Request

    curl http://secrethelpdesk934752.support.futurevera.thm/

### Response

    HTTP/1.1 302 Found
    Server: Apache/2.4.41 (Ubuntu)
    Location: http://flag{beea0d6edfcee06a59b83fb50ae81b2f}.s3-website-us-west-3.amazonaws.com/

The server responded with a redirect containing the flag location.

---

## Flag

    flag{beea0d6edfcee06a59b83fb50ae81b2f}

---

## Lessons Learned

- DNS enumeration alone is insufficient in modern CTF environments
- Virtual host fuzzing can reveal hidden services not present in DNS records
- TLS certificate inspection can expose hidden subdomains via SAN fields
- Misconfigured HTTPS services may fallback to incorrect certificates
- HTTP endpoints may expose sensitive redirects even when HTTPS fails
- Combining multiple reconnaissance techniques is critical for full attack surface discovery

---

## Key Takeaways

- Always pivot between enumeration methods when results are empty
- Inspect TLS certificates thoroughly during reconnaissance
- Use IP-based VHOST fuzzing when DNS enumeration fails
- Validate discovered subdomains with multiple protocols (HTTP/HTTPS)
- Small misconfigurations can lead directly to sensitive data exposure
