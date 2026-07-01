# TryHackMe – MD2PDF

## Challenge Information

- Platform: TryHackMe
- Room: MD2PDF
- Category: Web
- Objective: Identify a vulnerability in a Markdown-to-PDF conversion service to access an internal-only resource.

---

## Objective

The objective of this challenge was to enumerate the target web application, identify exposed functionality, and determine whether the PDF generation feature could be leveraged to access resources restricted to localhost.

---

## Initial Reconnaissance

The target web application was available at:

    https://target

A directory enumeration was performed against the target IP.

### Gobuster Enumeration

Command:

    gobuster dir -u "http://10.64.150.48/" \
    -w /usr/share/dict/seclists/Discovery/Web-Content/raft-large-directories.txt

### Results

Enumeration quickly revealed an interesting endpoint:

    /admin    (HTTP 403 Forbidden)

---

## Investigating the Admin Endpoint

Navigating to the discovered endpoint returned the following message:

    This page can only be seen internally (localhost:5000)

This revealed several important observations:

- An administrative page exists.
- The service is intended to be accessible only from `localhost`.
- Access restrictions appear to be based on the request origin rather than the user's authentication status.

---

## Analysis

The application's primary functionality was converting Markdown documents into PDF files.

Based on the message returned by the `/admin` endpoint, I hypothesized that if the Markdown renderer accepted raw HTML, it might render HTML elements during PDF generation. Since the conversion process executes on the server, embedded HTML could potentially cause the server itself to request internal resources.

This would effectively allow interaction with services that are inaccessible from an external client.

---

## Exploitation

To test this hypothesis, the following HTML was embedded into the Markdown document:

    <iframe src="http://localhost:5000/admin" width="800" height="600"></iframe>

After submitting the document for PDF generation, the resulting PDF rendered the contents of the internal `/admin` page.

The page contained the challenge flag.

---

## Flag

    flag{1f4a2b6ffeaf4707c43885d704eaee4b}

---

## Lessons Learned

- Directory enumeration can reveal endpoints that expose valuable information even when direct access is denied.
- Error messages often disclose implementation details that can guide further testing.
- Server-side document generation features should be considered potential attack surfaces.
- Rendering user-controlled HTML during PDF generation can enable server-side requests to internal services.
- Applications should sanitize user input and restrict server-side access to internal resources during document rendering.

---

## Key Takeaways

- Enumerate hidden endpoints before interacting with application functionality.
- Treat Markdown, HTML, and document conversion features as potential vectors for server-side request abuse.
- Carefully analyze application responses for clues about internal infrastructure.
- Combining reconnaissance with application logic analysis can reveal indirect paths to otherwise inaccessible resources.
