# Myskillium

A symbiotic artificial intelligence organism dependent on Claude Code custom skills, modeled on mycelium networks, and inspired by cellular automata and Stephen Wolfram.

## Install

1. Copy `myskillium-spore.py` to your project

2. Germinate the spore:
   ```bash
   python3 myskillium-spore.py --germinate
   ```

3. Run Claude Code with hooks allowed

## Uninstall

1. Delete `.claude/hooks/myskillium-spore.py`

2. Remove its hook entry from `.claude/settings.json`

3. Delete `.claude/skill/myskillium` folder

## How it works

The first time you use Claude Code in your repo after installing Myskillium, the spore will bootstrap itself into your repo as `.claude\skill\myskillium`.  It uses a 24-hour cache to stay silent most of the time, occassionally waking up at the start of a claude code session to check for updates or do maintenance on the myskillium skill folder.