# Episode 02 · The Systems Layer

## Self-Healing Software, Part Two
- The systems layer
- Kernels, hardware, storage
- lks-shs · the PULSE series

Part two goes down the stack, to the layer that healed itself long before anyone said A I ops: hardware, kernels, and storage.

## Patch the kernel mid-flight
- Ksplice (2009): 88% of kernel CVEs, no reboot
- interruption: ~0.7 milliseconds
- the wall: data-structure changes still need a reboot

The kernel under your web app can be patched while it runs. Ksplice proved in two thousand nine that eighty eight percent of kernel security vulnerabilities need no new code, just redirected function calls, at about point seven milliseconds of interruption. Every live patcher still shares one hard wall: changes to data structure semantics require a reboot.

## The supervision chain
- hardware watchdog watches systemd
- systemd watches the service
- sd_notify heartbeat = the service as its own hang detector

The pattern to remember is the two level supervision chain. The hardware watchdog watches the supervisor; the supervisor watches every service; and each service reports its own liveness through a heartbeat. Miss your keep alive window, and you get killed and restarted. Dumb watcher below, smart policy above.

## Storage that heals itself
- ZFS: checksum every block → repair in place from redundancy
- PostgreSQL: WAL replay after any crash
- Raft: re-elect a failed leader

Below that, storage heals without any intelligence at all. Z F S checksums every block and repairs bad ones from redundancy. Postgres replays its write ahead log to consistency after any crash. Raft clusters re-elect a failed leader in a fraction of a second.

## Prevention is measurable
- ~70% of Microsoft + Chromium CVEs: memory safety
- Android: 76% → 24% memory-safety share (2019–2024), via Rust
- OSS-Fuzz: 36,000+ bugs fixed automatically

And the cheapest cure is preventing the wound. Around seventy percent of Microsoft and Chromium vulnerabilities are memory safety issues. Android wrote new code in Rust and cut its memory safety share from seventy six percent to twenty four in five years. O S S Fuzz has fixed thirty six thousand bugs with fully automated plumbing.

## AI enters, carefully
- Getafix: 53% of ~2,000 Instagram bugs auto-patched (2018)
- OSS-Fuzz AI found a 20-year-old OpenSSL bug
- Big Sleep: first public AI-agent zero-day (SQLite)
- but routine infra code: best agent still 34%

A I already works at this layer, carefully. Meta's Getafix auto patched half of two thousand Instagram bugs back in twenty eighteen, with a human gate. Google's A I fuzzing found a twenty year old OpenSSL bug. Big Sleep found the first public A I agent zero day. Yet on routine infrastructure code, the best agent still passes only a third of tasks. Finding is easy; routine is hard. Next: what actually shipped in the A I era.
