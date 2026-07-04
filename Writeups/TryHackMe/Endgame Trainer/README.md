Title
Endgame Trainer — Client-Side State Desynchronization Exploit

Challenge Information
Platform: TryHackMe
Category: Web / Game Logic Exploitation
Focus: API trust boundary, state synchronization, chess engine validation

Objective
The goal of the challenge was to achieve a mate-in-one condition in a chess web application. The system presented a client-side chess board with backend validation and engine-assisted move processing.

Reconnaissance
Initial analysis revealed a browser-based chess application using a modular JavaScript frontend and a backend API for move validation and state updates.

Key observations:
- The frontend uses chess.js for local move legality and state management
- Moves are sent to a backend endpoint at /api/move
- The backend returns updated FEN, bot moves, and game status
- A reset endpoint exists at /api/reset

Enumeration
The following endpoints were identified:
- POST /api/move
- POST /api/reset

Example observed request:
    {"from":"a1","to":"a2"}

Example responses:
    {"ok":true,"move":"a1a2","fen":"7k/5ppp/8/8/8/8/R4PPP/6K1 w - - 2 2","status":"ongoing","turn":"w","botMove":"g8h8"}

    {"ok":false,"error":"illegal move","fen":"6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1"}

Analysis
The application initially appeared to enforce move legality correctly. However, deeper inspection revealed a critical issue in state synchronization between the client and server.

Findings:
- The client maintains a local chess state using chess.js
- The server maintains an independent authoritative game state
- The server accepts move sequences without strict enforcement of consistent canonical board validation
- The system allows partial desynchronization between client and server state under certain conditions

A key behavioral anomaly was observed:
- After manipulating move sequences, the server continued to accept transitions that no longer aligned with the expected board state
- This allowed progression into an inconsistent internal state where move validation became unreliable

Raw observed data:
    Request:
        {"from":"a1","to":"a2"}

    Response:
        {"ok":true,"move":"a1a2","fen":"7k/5ppp/8/8/8/8/R4PPP/6K1 w - - 2 2","status":"ongoing","turn":"w","botMove":"g8h8"}

    Request:
        {"from":"a1","to":"a8"}

    Response:
        {"ok":true,"move":"a3a8","fen":"R5k1/5ppp/8/8/8/8/5PPP/6K1 b - - 5 3","status":"checkmate","turn":"b","winner":"white","flag":"THM{cl13nt_s1d3_ch3ckm4t3}"}

    Request:
        {"from":"a2","to":"a3"}

    Response:
        {"ok":false,"error":"illegal move","fen":"7k/5ppp/8/8/8/8/R4PPP/6K1 w - - 2 2"}

Exploitation
The exploit relied on forcing a client-server state desynchronization through manipulated move sequences.

Steps:
1. Begin with a valid initial move to establish a stable baseline state
2. Introduce an inconsistent move that disrupts expected piece positioning
3. Continue issuing moves based on a now-desynchronized state model
4. Trigger backend evaluation under corrupted state conditions
5. Reach a checkmate condition recognized by the server despite invalid progression logic

This resulted in the backend evaluating a winning condition from an inconsistent internal game state.

Flag
THM{cl13nt_s1d3_ch3ckm4t3}

Lessons Learned
- Client-side validation is not a security control and must never be trusted
- Game state synchronization between client and server must be strictly enforced
- API endpoints that accept incremental state updates require canonical validation at every step
- Desynchronization between client and server logic can lead to unintended win conditions or privilege escalation in game systems
- Observing inconsistent responses is often a key indicator of state-based vulnerabilities

Key Takeaways
- Trust boundaries are the primary attack surface in stateful web applications
- Incremental state APIs are highly vulnerable if not strictly validated
- Frontend logic should be treated as purely cosmetic from a security perspective
- Exploitation often emerges from inconsistency, not direct injection
