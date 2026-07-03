# Neighbour - TryHackMe

## Challenge Information

- Platform: TryHackMe
- Room: Neighbour
- Category: Web / Insecure Direct Object Reference (IDOR)

## Objective

Obtain the flag by identifying and exploiting a vulnerability in the web application.

## Reconnaissance

After starting the target machine, the provided IP address presented a login page.

While inspecting the page, a hint suggested using **Ctrl+U** to view the page source.

### Observation

The HTML source contained the following developer comment:

    <!-- use guest:guest credentials until registration is fixed -->

This disclosed valid credentials for a guest account.

## Enumeration

Using the discovered credentials:

    Username: guest
    Password: guest

successfully authenticated to the application.

After logging in, the browser was redirected to:

    http://<TARGET_IP>/profile.php?user=guest

### Observation

The authenticated user's identity was controlled through the `user` query parameter in the URL.

## Analysis

The application appeared to trust the value of the `user` parameter without verifying that it matched the authenticated session.

This suggested a possible **Insecure Direct Object Reference (IDOR)** vulnerability, where modifying the identifier could provide access to another user's resources.

## Exploitation

To validate the hypothesis, the `user` parameter was modified from:

    guest

to:

    admin

Resulting URL:

    http://<TARGET_IP>/profile.php?user=admin

The application returned the administrator's profile instead of denying access.

The page displayed the flag directly.

## Flag

The flag was successfully obtained.

    flag{66be95c478473d91a5358f2440c7af1f}

## Lessons Learned

- Always inspect HTML source code for developer comments and hidden hints.
- Hardcoded credentials left in production code can expose unintended access.
- Query parameters that reference user identities should never be trusted without server-side authorization checks.
- Changing predictable object identifiers is a common technique for discovering IDOR vulnerabilities.

## Key Takeaways

- Review page source during reconnaissance.
- Test disclosed credentials when available.
- Examine URLs for user-controlled identifiers after authentication.
- Verify whether modifying object references grants unauthorized access.
- IDOR vulnerabilities arise from missing authorization checks rather than authentication failures.
