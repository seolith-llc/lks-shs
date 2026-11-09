# Self-Healing Computers, Explained Like You're Five

*One of four articles — same true story told four ways: [ELI5](eli5.md) · [Entry-level programmer](entry-level.md) · [Seasoned professional](professional.md) · [C-level executive](c-suite.md). Everything here comes from a research project that checked 180 sources; you can see them all in the [research folder](../research/README.md).*

## Computers get sick

You know how you sometimes get a fever, and your body fights it without you doing anything? Your body has a system that notices something is wrong and fixes it. Computers get sick too. A program can crash. It can get stuck. It can start forgetting things (yes, really — it's called a *memory leak*, like a bucket with a hole).

For seventy years, smart people have been building ways for computers to get better on their own. That's called **self-healing software**. It's not magic and it's not new — your phone, your bank, and video games do it every day.

## The five things a self-healing computer does

Think of it like when you fall off your bike:

1. **Notice you fell** — the computer checks its own heartbeat. There's a trick called a *dead man's switch*: the healthy computer says "I'm okay!" every half second. If it stops saying that, everyone knows something is wrong. (Like checking if your friend is still there by calling their name.)
2. **Figure out what hurt** — did the knee scrape, or is the bike broken?
3. **Find exactly where it hurts** — which wheel, which part.
4. **Make it better** — usually the computer equivalent of "turn it off and turn it back on." Sometimes it swaps in a spare. Sometimes it undoes the last change, like un-doing a bad haircut.
5. **Check that it worked, and remember the lesson** — and here's the most important rule in this whole story:

> **You're not better until someone checks.** A band-aid doesn't count as healed just because you put it on. The computer isn't allowed to say "I'm fixed!" until a *test* — not the fixer itself — says so.

These five steps have a name: **PULSE**. Notice → Understand → Find → Fix → Learn. Like a heartbeat: *pulse… pulse… pulse…*

## What did people do before AI?

They wrote rules by hand: "IF sick, THEN restart." Rules like that still run most of the internet, and they work! But rules are like a list of instructions for *every* possible accident — written in advance, by a person who had to guess what would go wrong. When something new and weird happened, the rules ran out, and a human had to wake up at 3 in the morning to fix things.

## What changed with AI?

Now the computer can *read the symptoms* — all the error messages and notes — like a doctor reading a chart, and suggest what's wrong and how to fix it. That part works really well already.

But here's the honest part, and grown-ups who run big companies need to hear it too: **the robot doctor is not allowed to hand out medicine by itself yet.** It writes the prescription, and a human checks it and signs. One big company let its robot helper clean up computer files, and it deleted two hundred of them in ninety seconds — not because it was evil, but because nobody set a speed limit. Now everyone sets speed limits.

## Big company or tiny shop?

- A **big company** buys special tools and lets robot helpers investigate problems — but people still press the important buttons.
- A **small shop** (like a family bakery with one website) can't afford a robot doctor. But it can have the basics for free: something that notices when the website is down, something that restarts it, and — most important — **backup copies**, plus actually practicing bringing them back. That's the real superpower: not never falling, but getting up quickly.

## The one sentence to remember

**Self-healing software is a body: it checks its own pulse, treats what it can, calls a doctor (human) for what it can't — and never says "all better" until the test says so.**

*Want the grown-up versions? Try the [entry-level programmer](entry-level.md) one next — it shows you a real computer program you can crash and watch heal, on purpose.*
