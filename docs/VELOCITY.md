# Engineer Velocity — A Realistic Speech

## The honest truth about how fast good engineers actually move

---

The gap between a mid-level engineer and a strong one isn't intelligence. It's not even experience. It's **the tolerance for incomplete information**.

Watch a strong engineer in a hackathon. They sit down, read the spec for 10 minutes, and then they start typing. Not planning. Not re-reading. Typing. They've decided that the fastest way to understand the problem is to build the wrong version of it first and fix it. They are not waiting until they understand everything. They are building their way to understanding.

The idle engineer? Still asking questions at hour two. Still making sure they have the perfect folder structure. Still reading docs for a library they haven't written a line of yet. Every minute they spend "figuring it out" before starting is a minute they've borrowed against shipping time — and the bill always comes due on demo day.

---

## What the clock actually looks like in a 48-hour build

Strong teams hit a working demo in **4 hours**. Not polished. Not complete. Working. Something you can run, click, or point at and say "this is the thing." Everything after that is refinement.

By hour 8, they know exactly what will and won't be in the final build. They've already cut scope twice. They're not cutting because they're lazy — they're cutting because they understand that a working narrow thing beats a broken wide thing every time on a demo stage.

By hour 24, they're rehearsing the demo. Not building new features. Rehearsing. Because the demo is the product. The judges never see your code. They see 3 minutes of you under pressure explaining what you built.

By hour 36, the code is frozen. What's left is the story.

That is not an exaggeration. That is the actual pace of teams that win.

---

## The specific version of this for you, right now

You have a complete spec. The data model is defined. The task list is written out to 106 items. The demo scenarios are scripted. The pitch lines exist. You even know what the opening line of the demo recording should be.

That's rare. Most hackathon teams spend 8 hours getting to where you already are.

So here's what velocity looks like for this project, measured in real time:

- **devices.json** — 15 minutes. 10 FBS switches, 4 DSRs, rack + zone fields. You already know the schema. Start typing.
- **cables.json** — 25 minutes. 30 cable entries, redundancy groups, one single-uplink FBS. It's a JSON array. You already know the shape.
- **impact.py core** — 45 minutes. Four functions: lookup, find group, count healthy, compute risk. No Flask, no HTML, no CLI yet. Just the math. Testable in a Python REPL.
- **cli.py** — 20 minutes. argparse, call analyze(), print colored output. That's it.

**You can have a working CLI demo in under 2 hours from right now.**

Not a polished one. A real one. One you can run and show someone. One that outputs RED when risk is HIGH. That is your first milestone. Everything else — Flask, HTML, dark theme, keyboard shortcuts — is decoration on top of something that works.

---

## The patterns that separate fast from slow

**Fast engineers do the ugly version first.**
They write hardcoded data to prove the logic before they build the data loader. They write `print()` before they build the formatted output. They get the thing working in any form, then make it right.

**Fast engineers don't build infrastructure they haven't needed yet.**
No venv setup before there's Python code. No requirements.txt before there's an import. No run.sh before there's an app to run. Every file you create before it's necessary is time you spent on something that isn't the core.

**Fast engineers commit working checkpoints.**
Every time something works — even slightly — they commit. `git add -A && git commit -m "cli returns risk for known cable"`. Not for cleanliness. Because it means they can always go back. It means they can experiment without fear. It means the work is saved before they break it.

**Fast engineers cut aggressively and unapologetically.**
The zone filter dropdown in the web UI? Cut. The verbose mode with intermediate computation steps? Cut. The favicon? Cut. The keyboard shortcuts? Cut. If it doesn't appear in the 3-minute demo, it doesn't exist. The app is: type a cable ID, see risk level, see MAINT snippet. That's the demo. Everything else is scope creep with good intentions.

**Fast engineers don't context-switch mid-task.**
When you're writing impact.py, you are writing impact.py. Not thinking about the Flask routes. Not thinking about the slide design. Not checking Slack. The task list has 106 items because it was written by someone thinking about the full project. On a given day, you should care about exactly the next 3.

---

## On tools and access

You won't always have access to every system you'd want. NetBox, Grafana, Jira, live topology data — sometimes you're blocked. The difference between a stuck engineer and a moving one is the decision you make when you hit that wall.

The stuck engineer waits for access. Waits for the right data. Waits until they can do it properly.

The moving engineer builds with what they have. Static JSON is not a compromise — it's a feature. It means your app works offline, in a demo room with bad wifi, on someone else's laptop, in front of judges who have no access to your internal systems. Static data is a demo superpower.

You have the schema. You know the data shape. Generate the data. Make it realistic enough to tell the story. EVI01-FBS01 through FBS10, DSR1 through DSR4, cables named like real cables, redundancy groups that match how the network actually works. A judge who's never touched a cable in a data center should be able to look at this JSON and believe it.

---

## The moment that matters

At some point in the next two weeks, you're going to be sitting in front of a screen with everything half-built, unsure what to do next, feeling like it's not good enough yet to show anyone.

That feeling is not a signal to keep designing. That is the exact moment to run the thing and let the broken output tell you what to fix next.

Build first. Fix on contact. Ship what works. Cut what doesn't.

The engineers who win don't do it by being smarter than you. They do it by spending more of their time with the thing running than with the thing being planned.

Open your editor. Start with devices.json. You already know what goes in it.

---

*This file exists to be read at the start of a session when momentum is low. It is not inspiration. It is a description of the pace that's required.*
