# 🚫 Negative Skills CLI

Turn your Claude frustrations into an installable SKILL.md constraint file.

## What it does
Instead of telling Claude what to do, this tool encodes what Claude should
**never** do — packaged as a portable skill file you can drop into any
Claude-compatible setup.

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Anthropic API key:
ANTHROPIC_API_KEY=your-key-here

## Usage
python main.py

Follow the prompts. Your skill file will be saved to the `output/` folder.

## Output format
Each generated skill includes:
- Description
- Context (when the skill applies)
- Constraints (CRITICAL / WARNING / PREFERENCE)
- Behavioral instructions for Claude

## What's next
- [ ] Web UI
- [ ] Skill conflict detection
- [ ] Export to multiple formats
- [ ] Integration with Obsidian second brain
