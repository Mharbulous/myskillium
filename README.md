# Myskillium

Myskillium is a meta-skill within the Claude Code ecosystem that finds and improves skills using processes modelled after mycelium.  Through a process called conidiation it creates spores (conidium) that can be copied to other repos where they grow independently into hyphae (threads) and eventualy connect to create decentralized network of symbiotic cloned skills.

This experiment in non-deterministic evolutionary programming is dedicated to John Horton Conway, Edward Lorenz, Stephen Wolfram, and Andrej Karpathy.

1. Install

   ```bash
   python conidium.py --germinate
   ```

3. Uninstall

   ```bash
   python conidium.py --apoptose
   ```

## Uninstall

1. Delete .claude/skills/myskillium/scripts/conidium.py
2. Remove its hook entry from .claude/settings.json
3. Delete .claude/skills/myskillium folder

## How it works

The first time you use Claude Code in your repo after installing Myskillium, the spore will bootstrap itself into your repo as .claude/skills/myskillium.

It stays silent most of the time, only waking to notify you when upstream updates are available.
