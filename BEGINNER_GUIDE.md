# New Game Plus - Beginner's Guide

Welcome to **New Game Plus**! This comprehensive guide will help you understand every aspect of the game and how to use it effectively to level up your real life.

## Table of Contents

1. [What is New Game Plus?](#what-is-new-game-plus)
2. [Core Concepts](#core-concepts)
3. [The Five Loops Explained](#the-five-loops-explained)
4. [Getting Started](#getting-started)
5. [Understanding Skills](#understanding-skills)
6. [Working with Missions](#working-with-missions)
7. [The Cycle System](#the-cycle-system)
8. [Progression & Leveling](#progression--leveling)
9. [Reflection & Journaling](#reflection--journaling)
10. [The Navigator](#the-navigator)
11. [Rewards Shop](#rewards-shop)
12. [Time Capsules](#time-capsules)
13. [Tips & Best Practices](#tips--best-practices)
14. [Troubleshooting](#troubleshooting)

---

## What is New Game Plus?

**New Game Plus** is a terminal-based life RPG (Role-Playing Game) that gamifies your personal development. It transforms your real-life activities into missions, tracks your progress through skills, and provides intelligent feedback to help you grow.

### Why Use It?

- **Motivation**: Earn XP and level up by completing real tasks
- **Structure**: Organize your development across different skill areas
- **Insight**: Get intelligent feedback on your patterns and progress
- **Privacy**: 100% offline, all data stays on your machine
- **Anti-Gaming**: Designed to resist exploitation and encourage genuine progress

---

## Core Concepts

### 1. **Player (You)**
- Has a **Class** (your role, e.g., "Digital Craftsman")
- Has a **Level** (overall progress)
- Earns **XP** (experience points) and **Coins**
- Grows through completing missions

### 2. **Skills**
- Areas you want to develop (e.g., "Writing", "Fitness", "Coding")
- Each skill has its own level and XP
- Requires **8+ missions** to be "ready" (unlock cycle bonuses)
- Can be set to **Focus mode** for deeper mastery

### 3. **Missions**
- Tasks you complete to develop skills
- Have **difficulty** (1-5) and **energy** (1-5) ratings
- Can contribute to 1-2 skills
- Award XP and coins when completed

### 4. **Cycles**
- Time periods for each skill (daily/weekly/monthly)
- Each cycle has a hidden "target mission"
- Hitting the target grants 10x bonus XP
- Prevents grinding the same easy mission

### 5. **The Navigator**
- AI-like system that analyzes your patterns
- Detects imbalances, gaps, and opportunities
- Provides subtle, non-intrusive suggestions

---

## The Five Loops Explained

New Game Plus operates on a continuous improvement cycle with five interconnected loops:

### Loop 1: Action Loop
**What**: Complete missions to earn XP and coins

**How it works**:
1. You see available missions
2. You select and complete one
3. System awards base XP + coins
4. If it's the hidden cycle target, you get 10x bonus XP
5. Each mission can only be credited once per cycle per skill

**Why**: This is where actual progress happens in your real life

---

### Loop 2: Reflection Loop
**What**: Write journals and reflections about your progress

**How it works**:
1. After completing missions, you might be prompted to reflect (~10% chance)
2. Prompts are rate-limited (max 2/day, 7/skill-cycle)
3. You can also write freeform journal entries anytime
4. Reflections give NO XP (they're non-farmable)

**Why**: Deepens your understanding and prevents the system from being purely mechanical

---

### Loop 3: Analysis Loop
**What**: The Navigator analyzes your patterns

**How it works**:
1. Navigator examines your skills, missions, and completions
2. Detects patterns like:
   - Skill imbalances
   - Low cycle performance
   - Readiness gaps
   - Reflection lapses
   - Coin hoarding
3. Assigns confidence scores to each pattern

**Why**: Provides objective insight into your behavior

---

### Loop 4: Suggestion Loop
**What**: Get subtle corrective feedback

**How it works**:
1. Navigator converts patterns into suggestions
2. Suggestions are prioritized (high/normal/low)
3. You see 1-3 suggestions at a time
4. Suggestions are gentle, not pushy

**Why**: Helps you course-correct without being manipulative

---

### Loop 5: Adjustment Loop
**What**: You refine your approach

**How it works**:
1. Based on suggestions and experience, you make changes:
   - Change skill cycle cadence
   - Toggle Focus mode
   - Adjust mission difficulty
   - Reorganize missions
2. These adjustments feed back into the Action Loop

**Why**: Puts you in control of your growth trajectory

---

## Getting Started

### First Launch

1. **Install**:
   ```bash
   pip install -r requirements.txt
   python -m ngp.main
   ```

2. **Create Your Character**:
   - Choose a name (your real name or nickname)
   - Choose a class (your role/identity, e.g., "Aspiring Writer", "Digital Nomad")
   - Optionally add a class description

3. **Create Your First Skill**:
   - Pick something you want to develop
   - Examples: "Writing", "Fitness", "Coding", "Music"
   - Choose an emoji icon (optional but fun!)
   - Set cycle cadence (weekly is a good default)

4. **Add Missions**:
   - Create at least 8 missions for your first skill
   - Vary the difficulty (mix of 1s, 2s, and 3s)
   - Examples for "Writing" skill:
     - "Write 500 words" (difficulty 2, energy 2)
     - "Edit one chapter" (difficulty 3, energy 3)
     - "Write for 15 minutes" (difficulty 1, energy 1)
     - "Research topic for blog post" (difficulty 2, energy 2)

5. **Complete Your First Mission**:
   - Select a mission that matches your current energy
   - Complete it in real life
   - Mark it complete in the game
   - Celebrate your first XP!

---

## Understanding Skills

### What Makes a Good Skill?

✅ **Good Skills**:
- Specific enough to track ("Writing", not "Life")
- Important to you personally
- Can be practiced regularly
- Has clear actions associated with it

❌ **Avoid**:
- Too broad ("Everything")
- One-time goals ("Buy a car")
- Skills you don't care about

### Skill Properties

#### Level & XP
- Starts at level 1
- Gains XP from completing missions
- Level formula: `XP_needed = ceil(120 × level^1.5)`
- Example: Level 1→2 needs 120 XP, Level 2→3 needs 203 XP

#### Readiness
- Skill needs **8+ missions** to be "ready"
- Ready skills can earn cycle bonuses (10x XP)
- Shown as "Ready 10/8" or "Not Ready 3/8"

#### Cycle Cadence
- **Daily**: New cycle every day
- **Weekly**: New cycle every Monday
- **Monthly**: New cycle on 1st of month

Choose based on how often you can practice the skill

#### Focus Mode
- Marks skill for deeper mastery
- **2x XP requirement** for leveling (slower progression)
- No extra rewards
- Signals: "I'm serious about this one"

**When to use Focus**:
- Your most important skill
- Something you want to master deeply
- Limit to 1-2 skills maximum

---

## Working with Missions

### Creating Missions

#### Mission Properties

**Title**: Clear, actionable description
- Good: "Write 500 words"
- Bad: "Do writing stuff"

**Difficulty** (1-5):
- **1**: Very easy, takes <15 minutes
- **2**: Easy, takes 15-30 minutes
- **3**: Moderate, takes 30-60 minutes
- **4**: Hard, takes 1-2 hours
- **5**: Very hard, takes 2+ hours or high cognitive load

**Energy** (1-5):
- **1**: Can do when exhausted
- **2**: Need to be alert
- **3**: Need good energy
- **4**: Need to be sharp
- **5**: Need peak performance

**Skills** (1-2):
- Assign mission to the skill(s) it develops
- Can contribute to 2 skills max
- Example: "Write technical blog post" → Writing + Coding

### XP & Coin Rewards

**Base Rewards** (every completion):
- Player XP: `4 × difficulty`
- Skill XP: `8 × difficulty` per skill
- Coins: `2 × difficulty`

**Cycle Bonus** (when hitting target):
- Player XP: `40 × difficulty` (10x base!)
- Skill XP: `80 × difficulty` (10x base!)
- Coins: Same as base

**Example**: Difficulty 3 mission
- Normal: 12 player XP, 24 skill XP, 6 coins
- Target hit: +120 player XP, +240 skill XP!

### Mission Strategies

#### Energy Matching
Keep missions with different energy levels:
- Energy 1-2: For tired evenings
- Energy 3: For normal energy
- Energy 4-5: For peak hours

Complete missions that match your current state.

#### Difficulty Balance
Don't make everything difficulty 1:
- More difficulty = More XP & coins
- Challenge yourself appropriately
- Mix easy wins with harder challenges

#### The 8-Mission Rule
Each skill needs 8+ missions to unlock cycle bonuses:
- Start with 8-10 varied missions per skill
- Add more over time
- Remove missions that don't serve you

---

## The Cycle System

### How Cycles Work

1. **Cycle Starts**:
   - Happens automatically based on cadence
   - System picks a random mission as the "target"
   - Target is **hidden** from you

2. **During Cycle**:
   - Complete any missions for that skill
   - When you hit the target: **BONUS XP!**
   - Each mission can only grant XP **once per cycle**

3. **Cycle Ends**:
   - New cycle begins
   - New target selected
   - Mission credit counters reset

### Anti-Goodhart Mechanics

**Problem**: In most RPGs, you can "grind" by repeating the easiest mission.

**Solution**: New Game Plus prevents this:

1. **One-credit-per-cycle**: Repeating a mission in the same cycle gives 0 XP
2. **Hidden targets**: You don't know which mission is the target
3. **Readiness requirement**: Need 8+ missions to get any cycle bonuses
4. **Variety rewarded**: Completing different missions increases chance of hitting target

**Result**: You're encouraged to complete a variety of missions, not just grind one easy task.

### Cycle Indicators

**In the Skills view**:
- **⚡** = Cycle target hit this cycle
- **○** = Cycle target not yet hit
- **✓ 10/8** = Skill is ready (has enough missions)
- **✗ 3/8** = Skill not ready (needs more missions)

---

## Progression & Leveling

### Player Level
- Represents overall progress across all skills
- Goes up from any mission completion (base + cycle XP)
- Shows in dashboard as level + progress bar

### Skill Levels
- Each skill levels independently
- Goes up from missions assigned to that skill
- Focus skills level at half speed (2x XP needed)

### Level Curve
Both player and skills use the same formula:
```
XP_needed(level) = ceil(120 × level^1.5)
```

**Progression**:
- Level 1 → 2: 120 XP
- Level 2 → 3: 203 XP
- Level 3 → 4: 296 XP
- Level 5 → 6: 506 XP
- Level 10 → 11: 1,265 XP

This creates **meaningful progression**: each level takes longer, making achievements feel significant.

### Coins
Earned alongside XP, used for rewards:
- `2 × difficulty` per mission
- Save up for rewards you define
- No pressure to spend (they don't decay)

---

## Reflection & Journaling

### Reflection Prompts

**When they appear**:
- ~10% chance after mission completion
- Max 2 per day
- Max 7 per skill-cycle
- Can be dismissed

**Sample prompts**:
- "What did you learn from this?"
- "How did this make you feel?"
- "What would you do differently next time?"

**Important**: Reflections give **NO XP**. They exist purely for depth, not points.

### Journal Entries

**Freeform writing**:
- Write anytime from the Journal menu
- No prompts, no limits
- Can link to skills or missions
- Searchable

**Why journal**?
- Track insights
- Notice patterns the Navigator might miss
- Create a record of your journey
- Deepen your practice

### Time Capsules

**Letters to your future self**:
- Write a message
- Set unlock condition:
  - **Date**: Opens on specific date
  - **Mission**: Opens when you complete a specific mission
  - **Skill Level**: Opens when skill reaches level X
  - **Player Level**: Opens when you reach level X
- Optional encryption with passphrase

**Example**:
"Write a letter to yourself that unlocks when your Writing skill hits level 10. What advice would level-1 you give to level-10 you?"

---

## The Navigator

### What It Does

The Navigator is New Game Plus's analysis system. It:
- Examines your patterns
- Detects potential issues
- Provides gentle suggestions
- Respects your autonomy

### Patterns It Detects

1. **Skill Imbalance**: One skill way ahead of others
2. **Cycle Performance**: Are you hitting cycle targets?
3. **Readiness Gaps**: Skills that need more missions
4. **Reflection Lapses**: Haven't reflected in a while
5. **Focus Analysis**: Too many/few focus skills
6. **Coin Patterns**: Hoarding or no rewards defined
7. **Difficulty Distribution**: All easy or all hard missions

### How Suggestions Work

**Priority Levels**:
- **High** (red): Important issues to address
- **Normal** (yellow): Worth considering
- **Low** (blue): Nice-to-know info

**Example Suggestion**:
```
💡 Navigator
Skill Balance
Your Coding skill is 5 levels ahead of others
Consider creating missions for your other skills
```

### Using Navigator Insights

**Menu: View Navigator Insights**
- See all detected patterns
- Understand confidence levels
- Get actionable recommendations

**Best practice**: Check Navigator weekly to course-correct.

---

## Rewards Shop

### Creating Rewards

**Rewards are things you want**:
- Real-world treats
- Break activities
- Purchases you're saving for
- Experiences

**Examples**:
- "Coffee at favorite café" (20 coins)
- "1 hour gaming" (30 coins)
- "New book" (50 coins)
- "Nice dinner out" (100 coins)
- "Weekend trip" (500 coins)

### Redeeming Rewards

1. Go to Rewards menu
2. Select a reward
3. System checks if you have enough coins
4. Coins deducted, reward logged
5. **You actually give yourself the reward in real life**

**Important**: The system tracks redemptions, but **you** are responsible for actually giving yourself the reward. This is an honor system.

### Reward Strategy

**Start small**:
- Create a few affordable rewards (20-50 coins)
- Add aspirational rewards (100+ coins)
- Redeem regularly to maintain motivation

**Balance**:
- Don't hoard coins indefinitely
- Don't spend recklessly
- Find your sustainable pace

---

## Time Capsules

### Creating a Capsule

1. **Menu → Journal → Time Capsules → Create**
2. Write your message
3. Choose unlock condition:
   - **Date**: "Open this on my birthday next year"
   - **Mission**: "Open when I finish writing my book"
   - **Skill Level**: "Open when Writing hits level 10"
   - **Player Level**: "Open when I reach level 20"
4. Optional: Add encryption passphrase

### Capsule Ideas

**Milestone reflections**:
- "Letter to my level-10 self"
- "Goals for this year, open in 365 days"
- "Advice for when I complete my first marathon"

**Encouragement**:
- "Remember why you started" (opens when motivation dips)
- "You can do hard things" (opens on difficult missions)

**Time travel**:
- Write about current struggles
- Open when you've overcome them
- See how far you've come

### Viewing Capsules

**Locked capsules**: Listed but content hidden
**Unlocked capsules**: Can be read and archived to journal

---

## Tips & Best Practices

### Starting Out

1. **Start with one skill** until you understand the system
2. **Create 8-10 varied missions** for that skill
3. **Complete missions daily** for the first week
4. **Check Navigator after a week** to see patterns
5. **Add second skill** once comfortable

### Sustainable Habits

**Daily**:
- Complete 1-3 missions matching your energy
- Check which skills have hit cycle targets (⚡)

**Weekly**:
- Review Navigator insights
- Add/remove missions as needed
- Check if any skills need more missions (readiness)

**Monthly**:
- Review overall progress
- Adjust skill cadences if needed
- Consider toggling Focus mode
- Create new rewards or redeem coins

### Common Mistakes

❌ **Making all missions difficulty 1**
- You'll progress slowly
- Increase variety for better XP

❌ **Creating too many skills at once**
- Hard to maintain 8+ missions per skill
- Start with 2-3 skills maximum

❌ **Never redeeming rewards**
- Defeats the purpose of coins
- Treat yourself regularly!

❌ **Grinding same mission repeatedly**
- Won't work due to one-credit-per-cycle
- Embrace variety

❌ **Ignoring Navigator suggestions**
- Missing out on valuable insights
- At least read them weekly

### Advanced Strategies

**Focus Mode Mastery**:
- Pick your #1 priority skill
- Set to Focus mode
- Accept slower leveling
- Celebrate depth over breadth

**Cycle Optimization**:
- Track which skills haven't hit targets
- Prioritize those skills next cycle
- Don't chase the hidden target (it's random!)

**Reflection Depth**:
- Don't just answer prompts
- Write detailed journal entries weekly
- Link entries to skills for future reference

**Time Capsule Planning**:
- Create capsules at level milestones
- Set date capsules for quarterly reviews
- Use encryption for truly personal messages

---

## Troubleshooting

### "My skill isn't earning cycle bonuses"

**Check**:
- Does skill have 8+ missions? (Look for "Ready 8/8" or higher)
- Are you completing different missions, not the same one?
- Have you hit the target this cycle? (Look for ⚡ symbol)

**Fix**:
- Add more missions if below 8
- Complete variety of missions
- Be patient - target is random

### "I'm not getting reflection prompts"

**Why**:
- Only 10% chance per mission
- Max 2 per day
- Max 7 per skill-cycle

**This is intentional** - reflections are meant to be occasional, not constant.

### "Leveling feels slow"

**Remember**:
- Base XP is intentionally small (4-8 per mission)
- **Cycle bonuses are 10x** (40-80 per mission)
- Focus on hitting cycle targets
- Increase mission difficulty for more XP

### "I lost my data!"

**Prevention**:
- Use Export function (Menu → Settings → Export)
- Save to cloud storage
- Export weekly for safety

**Recovery**:
- Use Import function with your backup file

### "How do I know which mission is the cycle target?"

**You don't!** The target is **intentionally hidden**. This prevents gaming the system. Just complete a variety of missions and you'll eventually hit it.

---

## Export & Import

### Exporting Your Data

**When to export**:
- Before major changes
- Weekly backups
- Before uninstalling
- When switching computers

**How to export**:
1. Menu → Settings → Export
2. Choose filepath (e.g., `~/backups/ngp-2025-01-15.json.gz`)
3. Optionally compress (recommended)
4. File saved!

### Importing Data

**Importing replaces all current data**, so be careful!

**How to import**:
1. Menu → Settings → Import
2. Choose file
3. Review preview (counts)
4. Confirm import

---

## Final Thoughts

New Game Plus is designed to **support genuine growth**, not to be optimized or gamed. The system has built-in protections against exploitation, but it still requires your honest participation.

**Trust the process**:
- The loop system works
- The Navigator's insights are valuable
- Variety beats grinding
- Reflection deepens practice

**Make it yours**:
- Customize your skills
- Define your own rewards
- Write capsules to your future self
- Use the system in ways that serve you

**Most importantly**: **Actually do the missions in real life.** No amount of XP means anything if you're not building real skills and making real progress.

Good luck on your New Game Plus journey! 🎮✨

---

## Quick Reference Card

### XP Formulas
- Base Player XP: `4 × difficulty`
- Base Skill XP: `8 × difficulty`
- Cycle Player XP: `40 × difficulty`
- Cycle Skill XP: `80 × difficulty`
- Coins: `2 × difficulty`
- XP for Next Level: `ceil(120 × level^1.5)`

### Key Limits
- Missions per skill: Min 8 (for readiness)
- Skills per mission: Max 2
- Reflection prompts: Max 2/day, 7/skill-cycle
- Focus skills: Recommended 1-2 max

### Cycle Mechanics
- One credit per mission per skill per cycle
- Hidden random target selected at cycle start
- Hitting target = 10x bonus XP
- Cycles run on cadence (daily/weekly/monthly)

### Commands
```bash
# Run game
python -m ngp.main

# Or if installed
ngp

# Export data
Menu → Settings → Export

# Import data
Menu → Settings → Import
```

---

**Version**: 1.1.0
**Last Updated**: 2025
**For more info**: See README.md
