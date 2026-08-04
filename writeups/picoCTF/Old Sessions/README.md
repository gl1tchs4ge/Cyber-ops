# Old Sessions

## Challenge Information

- **Platform:** picoCTF 2026
- **Category:** Web Exploitation
- **Difficulty:** Easy
- **Challenge Name:** Old Sessions
- **Author:** David Gaviria

## Objective

Identify and exploit insecure session management in the web application to obtain the flag.

## Reconnaissance

The challenge provided a social media platform with a login page.

Target:

    http://dolphin-cove.picoctf.net:64732/login

The challenge description indicated that the application had improper session expiration controls, allowing sessions to remain active indefinitely.

Initial hypothesis:

    The vulnerability likely involved persistent authentication sessions that could be reused without credentials.

## Enumeration

### Login Page

The `/login` endpoint contained a standard HTML login form.

Observed:

    Method: POST

    Parameters:
        username
        password

No hidden fields, JavaScript logic, or client-side authentication mechanisms were identified.

### Registration Page

The `/register` endpoint contained a registration form.

Observed:

    Method: POST

    Parameters:
        username
        password
        conf_password

No additional security mechanisms were visible in the HTML source.

## Analysis

A test account was created:

    Username:
        H4ck4n3r

After authentication, the application displayed the user's profile page.

Observed functionality:

- User greeting
- Logout option
- Comments section

A comment from another user contained a useful discovery:

    Hey I found a strange page at /sessions

This suggested that the application exposed session-related information.

## Session Enumeration

Navigating to:

    /sessions

revealed active session information.

Observed sessions:

    session:-xUhvYfnuThRed5YFwED_-B5Zngi0kgLHJIpU9k_dsA
    {
        '_permanent': True,
        'key': 'admin'
    }

    session:64CFegTgdPAKmwNjugavndCcDGlKCzBSPtysS1-I3nw
    {
        '_permanent': True,
        'key': 'H4ck4n3r'
    }

The application exposed both the current user's session and the administrator's session.

## Exploitation

The session information suggested that authentication relied on session cookies.

The first attempt was to replace the current browser session value with the administrator session identifier.

The administrator session identifier:

    xUhvYfnuThRed5YFwED_-B5Zngi0kgLHJIpU9k_dsA

This attempt did not immediately work.

Further investigation was performed using browser developer tools.

The session cookie stored in the browser was modified directly through the Storage section:

    Developer Tools → Storage → Cookies

The existing session cookie value was replaced with the exposed administrator session value.

After refreshing the application, the session was accepted and access to the administrator account was obtained.

## Flag

The flag was successfully obtained:

    picoCTF{s3t_s3ss10n_3xp1rat10n5_51c526ab}

## Lessons Learned

This challenge demonstrated the risks of improperly configured session management.

The application trusted persistent sessions without enforcing appropriate expiration controls. Exposed or leaked session identifiers could therefore allow account takeover without requiring valid credentials.

## Key Takeaways

- Session identifiers are equivalent to authentication credentials while valid.
- Long-lived sessions increase the impact of session leakage.
- Session expiration and invalidation mechanisms are critical security controls.
- Sensitive session information should never be exposed through application endpoints.
- Authentication security depends not only on passwords but also on secure session lifecycle management.
