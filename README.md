# 🚫 Negative Skills

Turn your Claude frustrations into an installable SKILL.md constraint file.

Instead of telling Claude what to do, Negative Skills encodes what Claude should
**never** do — packaged as a portable constraint file you can drop into any
Claude-compatible setup.

---

## Install

```bash
pip install negative-skills
```

> **Windows users:** If `negative-skills` isn't recognized after installing, make sure Python was added to PATH during installation. If not, run the Python installer again and check that box.

---

## Usage

### CLI
```bash
negative-skills
```

Follow the prompts. Your SKILL.md will be saved to the `output/` folder and optionally installed directly into Claude Code.

### Web
Try it without installing anything at [your-deployed-url-here]

### Claude Code (MCP)
Add it as a native tool inside Claude Code:
```bash
claude mcp add negative-skills -- negative-skills-mcp
```

Once added, just tell Claude: *"Generate a negative skill for my coding sessions"* and it will run the interview and install the skill for you.

---

## Output format

Each generated skill includes:

- **Description** — what the skill is for
- **Context** — when Claude should apply it
- **Constraints** — CRITICAL / WARNING / PREFERENCE rules
- **Instructions** — behavioral directives for Claude

---

## Development setup

```bash
git clone https://github.com/melvinthoompunkal/claude-negative-skills
cd claude-negative-skills
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:
```
ANTHROPIC_API_KEY=your-key-here
```

---

## What's next

- [ ] Skill conflict detection
- [ ] Export to multiple formats
- [ ] Obsidian second brain integration
- [ ] Claude Code MCP end-to-end testing

---

## About

Built with Python, Click, and the Anthropic SDK.
