# New Game Plus

> A minimalist offline life RPG system for the Linux terminal

**New Game Plus** is a terminal-based life RPG that helps you level up your real life through a continuous improvement loop. Track missions, develop skills, reflect on your journey, and receive intelligent feedback from the Navigator.

## 🎮 The Core Loop

New Game Plus follows a five-stage continuous improvement cycle:

```
[Action Loop] → (Missions, completions)
      ↓
[Reflection Loop] → (Journals, Reflections)
      ↓
[Analysis Loop] → (Navigator interprets patterns)
      ↓
[Suggestion Loop] → (Subtle corrective feedback)
      ↓
[Player Adjustment] → (User tweaks cadence, tasks, focus)
      ↓
Back to [Action Loop]
```

## ✨ Key Features

### Anti-Goodhart Design
- **One-credit-per-cycle**: Each mission grants XP only once per skill per cycle
- **Readiness threshold**: Skills need 8+ missions before cycle bonuses apply
- **Hidden targets**: Each skill has a secret target mission per cycle
- **Multi-dimensional progress**: Can't just grind one easy mission

### Meaningful Progression
- **Dual leveling**: Player level + individual skill levels
- **Focus mode**: Mark skills as "Focus" for 2x XP requirement (deeper mastery)
- **Cycle cadence**: Each skill has its own rhythm (daily/weekly/monthly)
- **Variety matters**: Completing diverse missions is rewarded

### Reflection & Insight
- **Journal system**: Freeform writing with optional skill/mission links
- **Reflection tokens**: Rate-limited prompts (10% chance, max 2/day, 7/cycle)
- **Navigator analysis**: AI-like pattern detection and insights
- **Time capsules**: Letters to your future self (v1.1)

### Privacy First
- **100% offline**: All data stored locally in SQLite
- **No accounts**: Single-user game
- **No tracking**: Your data stays on your machine
- **Portable**: Easy export/import (planned)

## 📦 Installation

### Requirements
- Python 3.10 or higher
- Linux terminal (or WSL on Windows)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/NewGamePlus.git
cd LifeRPG  # Note: folder will be renamed in next update

# Install dependencies
pip install -r requirements.txt

# Run the game
python -m ngp.main

# Or install as a command
pip install -e .
ngp
```

## 🎯 Getting Started

### First Launch

1. **Create your character**: Choose a name and class (e.g., "Digital Craftsman")
2. **Create your first skill**: Something you want to develop (e.g., "Writing", "Fitness")
3. **Add missions**: Create tasks that help you practice that skill
4. **Complete missions**: Start earning XP and coins!

### Core Concepts

#### Skills
Skills represent areas you want to develop. Each skill:
- Has its own level and XP
- Requires 8+ missions to be "ready" (unlock cycle bonuses)
- Has a cycle cadence (daily/weekly/monthly)
- Can be marked as "Focus" for deeper mastery

#### Missions
Missions are tasks you complete to develop skills. Each mission:
- Can contribute to 1-2 skills
- Has difficulty (1-5) and energy (1-5) ratings
- Grants base XP and coins on completion
- Grants 10x bonus XP when it's the hidden cycle target

#### Cycles
Each skill has its own cycle (e.g., weekly):
- At cycle start, a random mission is chosen as the "target"
- Completing the target grants massive bonus XP
- Each mission can only be credited once per cycle
- This prevents grinding the same easy mission

#### The Navigator
The Navigator analyzes your patterns and provides insights:
- Detects skill imbalances
- Tracks cycle performance
- Identifies readiness gaps
- Suggests adjustments

## 🎲 Progression Math

### XP Awards
- **Base Player XP**: 4 × difficulty
- **Base Skill XP**: 8 × difficulty per skill
- **Cycle Bonus (Player)**: 40 × difficulty
- **Cycle Bonus (Skill)**: 80 × difficulty
- **Coins**: 2 × difficulty

### Level Curve
Both player and skills use: `XP_needed = ceil(120 × level^1.5)`

Focus skills: `XP_needed × 2` (slower progression)

## 🧭 Menu Structure

- **Complete a Mission**: Select and complete missions to earn XP
- **Create New Mission**: Add new tasks to your queue
- **Manage Skills**: Create, view, and configure skills
- **Journal & Reflections**: Write entries and view past reflections
- **View Navigator Insights**: See pattern analysis and suggestions
- **Adjustments**: Change cadence, toggle Focus mode, adjust difficulty
- **Profile**: View your character stats

## 🏗️ Architecture

```
ngp/
├── models/          # Data models (Player, Skill, Mission, etc.)
├── services/        # Core services (Storage, Progression, Cycle)
├── loops/           # The 5 loops (Action, Reflection, Analysis, Suggestion, Adjustment)
├── ui/              # Terminal UI (Dashboard, Menu)
└── main.py          # Entry point
```

### The Five Loops

1. **ActionLoop**: Mission creation and completion
2. **ReflectionLoop**: Journal entries and reflection prompts
3. **AnalysisLoop**: Pattern detection and insight generation
4. **SuggestionLoop**: Contextual feedback based on analysis
5. **AdjustmentLoop**: Player-driven tuning (cadence, focus, difficulty)

## 📊 Data Storage

All data is stored in `data/ngp.db` (SQLite):
- `player` - Your character
- `skills` - Your skills
- `missions` - Your missions
- `completions` - Completion history
- `journal_entries` - Reflections and journal entries
- `time_capsules` - Letters to your future self (planned)

## 🛠️ Development

### Project Structure
```
.
├── ngp/                    # Main package
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── loops/             # Game loops
│   └── ui/                # Terminal UI
├── data/                  # User data (gitignored)
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Package configuration
└── README.md             # This file
```

### Running Tests
```bash
# Unit tests (coming soon)
pytest tests/

# Manual testing
python -m ngp.main --db test.db
```

## 🗺️ Roadmap

### v1.0 (MVP) ✅
- [x] Core data models
- [x] Five-loop system
- [x] SQLite storage
- [x] Terminal UI
- [x] Mission completion flow
- [x] Skill management
- [x] Journal system
- [x] Navigator insights

### v1.1 (Planned)
- [ ] Time Capsules (unlock by date/milestone)
- [ ] Variety & Consistency scores
- [ ] Export/Import system
- [ ] Mission scheduling & reminders
- [ ] Enhanced Navigator analysis
- [ ] Rewards shop system

### v2.0 (Future)
- [ ] Plugin system
- [ ] Custom themes
- [ ] Advanced statistics
- [ ] Goal tracking
- [ ] Habit streaks (optional)

## 📖 Philosophy

**New Game Plus** is designed around three principles:

1. **Anti-Goodhart**: The system resists gaming and exploitation. You can't farm XP by spamming easy missions. Progress requires variety, consistency, and actual engagement.

2. **Autonomy & Depth**: You control your cycle cadences, skill definitions, and progression pace. Focus mode lets you signal deeper mastery over faster leveling.

3. **Meaning over Metrics**: Reflections and journals are non-farmable. They exist to deepen your journey, not to be optimized for points.

## 🤝 Contributing

This is a personal project, but suggestions and bug reports are welcome! Please open an issue or submit a pull request.

## 📜 License

GPL-3.0-or-later

Original LifeRPG concept by Jayvant Javier Pujara (2012)
New Game Plus redesign and implementation (2025)

## 🙏 Acknowledgments

- Inspired by the original [LifeRPG](http://www.reddit.com/r/LifeRPG/) project
- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal UI
- Follows the OuRPG offline single-user design philosophy

---

**Start your New Game Plus today. Level up your life, one mission at a time.** ✨
