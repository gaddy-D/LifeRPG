# OuRPG — Offline Single‑User Pitch for Engineering

## 1) One‑page summary
**OuRPG** is a minimalist, offline‑first, single‑user “life RPG.” The player defines **skills** (e.g., Writing, Cardio), creates **missions** (tasks) linked to those skills, and progresses via **Levels** (overall) and **per‑skill levels**. The design intentionally resists Goodhart’s Law: you can’t grind one easy mission to level forever. Progress depends on **per‑skill cycles**, **≥8 missions readiness**, and a simple **one‑credit‑per‑cycle** rule. Reflection Journals and Time Capsules reinforce meaning without becoming farmable rewards.

**Target platform:** iOS + Android via Flutter. **Mode:** single‑user, 100% local by default (no sign‑in, no analytics, no network dependency). Optional encrypted JSON export/import.

---

## 2) Product philosophy (why this is different)
- **Anti‑Goodhart by construction:** metrics are multi‑dimensional and capped per cycle; repetition produces no extra credit within the same cycle; meaningful progress comes from completing a single, pre‑selected target mission per skill per cycle (hidden by default) rather than spamming.
- **Autonomy and depth:** users name their **Class** (overall identity) and write optional descriptions for their **Class** and each **Skill**. They pick cycle cadence per skill (daily/weekly/monthly/custom). **Focus** mode halves leveling speed for a skill to signal real mastery.
- **Offline, private, durable:** all data local; works on airplanes; export/import for backups; optional per‑capsule encryption. No social features in v1.

---

## 3) Core gameplay loop (single‑user)
1. **Plan** — Player defines or refines a handful of **Skills**; creates **Missions** and assigns them to 1–2 skills. Sets cycle cadence per skill.
2. **Do** — Player completes a mission (one tap). System awards small **Base XP** and **Coins**. If this mission is the (hidden) **Cycle Target** for an attached skill and hasn’t been hit this cycle, award **Cycle XP** for that skill and mark it done for this cycle.
3. **Reflect** — Occasionally (≈1‑in‑10 eligible completions, rate‑limited), prompt a single‑line reflection; write freely in Journal anytime.
4. **Review** — Skills view shows per‑skill progress (Level, Cycle status, readiness `x/8`, Variety and Consistency chips). Timeline shows completions and reflections. Optional Time Capsules unlock on milestones (date/mission/skill level/level) and archive to Journal.
5. **Repeat** — New cycles start per skill cadence; a fresh target is seeded; progress accumulates slowly and honestly.

**Loop simplicity:** 1–2 taps to complete; no punishments by default; base feedback is present even when the target isn’t hit.

---

## 4) Mechanics (numbers kept small and legible)
### 4.1 Readiness & cycles
- **Readiness:** a skill “really levels” only if it has **≥ 8 missions** assigned (distinct mission IDs). If <8, completions still grant Base XP, but no Cycle XP will ever apply.
- **Per‑skill cycles:** each skill has its own cadence: `daily | weekly | monthly | custom RRULE`. Cycles align to `dayStartsAt` (user setting). At **cycle start**, a **Cycle Target** mission is **uniformly** chosen from the skill’s assigned missions. (Hidden by default; optional per‑skill reveal in Settings.)
- **One‑credit‑per‑cycle:** any given mission grants XP/coins **at most once per skill per cycle**. Repeat completions of the same mission within the same cycle are recorded but grant 0 additional credit.

### 4.2 XP / coins
- **Base Player XP**: `4 × D` (D=difficulty 1..5) — intentionally small.
- **Base Skill XP**: `8 × D` per attached skill — small.
- **Coins**: `2 × D` — simple shop economy.
- **Cycle XP** (applied **once** when target mission is completed for that skill in the cycle):
  - **Player**: `40 × D`
  - **Skill (targeted skill only)**: `80 × D`
- **Level curve** (player & skills): `XP_next(level) = ceil(120 × level^1.5)`.

### 4.3 Focus skills (depth over display)
- Marking a skill as **Focus** multiplies its **level thresholds ×2** (half‑speed leveling). No extra rewards. Copy explains: “Levels rise slower; mastery signals are stronger.”

### 4.4 Journals, reflections, capsules (non‑farmable)
- **Journal**: freeform, local. Optional tags to link entries to a skill/mission. Searchable.
- **Reflection Tokens**: ~**10%** chance on eligible completions, capped at **2/day** and **7/skill‑cycle**. One‑line prompt. **No XP/coins** awarded. Dismissible.
- **Time Capsules**: letters to future self; unlock by **date**, **mission completion**, **skill level**, or **level**. Optional per‑capsule passphrase. On unlock: modal + Timeline card; user can Read/Snooze/Archive to Journal. **No XP/coins**.

### 4.5 Variety & Consistency (v1.1 optional)
- **Variety**: evenness of completions across a skill’s missions in the current cycle (entropy‑lite). Shown as a chip (“Variety: good/fair/low”).
- **Consistency**: rolling success rate per skill (e.g., “hit target in 4 of last 6 cycles”). Shown as a chip. No streak anxiety.

---

## 5) Single‑user offline architecture
**Framework:** Flutter (Dart) with Material 3. **State:** Riverpod. **Nav:** GoRouter. **Local storage:** Hive (NoSQL) with generated adapters; JSON export/import. **Notifications:** flutter_local_notifications (local only). **Charts:** minimalist custom painter or fl_chart.

### 5.1 Boxes & types
- Boxes: `player`, `skills`, `missions`, `completions`, `rewards`, `journal`, `capsules`.
- **Player**: `id, displayName, className, classDescription, level, xp, coins, createdAt`.
- **Skill**: `id, name, description?, color, iconKey, level, xp, isArchived, order, cycleType, cycleStart, cycleEnd, targetMissionId?, hasHitTargetThisCycle, missionsCount`.
- **Mission**: `id, title, note, skillIds[], difficulty(1..5), energy(1..5), schedule(oneOff/daily/weekly/customRRULE), dueAt?, reminders[], isArchived, createdAt, updatedAt`.
- **Completion**: `id, missionId, completedAt, award{ basePlayerXp, baseSkillXpMap, coins, cycleXpAppliedSkillId? }, cycleId, reflectionRequested(bool)`.
- **Reward**: `id, title, priceCoins, note, isArchived`.
- **JournalEntry**: `id, createdAt, text, skillId?, missionId?, isReflectionToken, editedAt?`.
- **Capsule**: `id, title, body, createdAt, isEncrypted, passphraseHint?, unlockType(date/missionCompletion/skillLevel/level), unlockParams{…}, unlockedAt?, archivedToJournalEntryId?`.

### 5.2 Deterministic time & cycles
- **Day start**: per user (`dayStartsAt` hour). All cycle boundaries and due‑date logic reference this.
- **Cycle IDs**: `cycleId = skillId + ':' + cycleStartISO`. Used to enforce one‑credit‑per‑cycle.
- **Seeding target**: at cycle start, pick target uniformly from `missions where mission.skillIds includes skillId`. Persist `targetMissionId`.
- **Edge cases**: if missions <8 at cycle start → no target seeded; if missions drop <8 mid‑cycle → keep existing target but hide Cycle XP unless readiness is met (simplest path: require readiness at cycle start).

### 5.3 Services (core)
- **ProgressionService**: base/cycle XP math; level‑up routines (player, skills).
- **CycleService**: cycle boundary detection; target seeding; one‑credit‑per‑cycle checks; completion processing.
- **CapsuleService**: evaluate date triggers on app open/periodic tick; hook mission/skill/level triggers.
- **Notifications**: schedule local reminders from mission schedules; optional daily “Review” nudge.

### 5.4 Export/import & encryption
- **Export**: single JSON file containing all boxes; optional passphrase → encrypt payload (AES‑GCM). Store no keys server‑side.
- **Import**: validate schema version; show preview (counts per entity) before overwrite/merge.

---

## 6) Key algorithms (pseudocode)
### 6.1 On app open (or hourly tick)
```
now = localNowAlignedToDayStart()
for each skill in Skills:
  if now >= skill.cycleEnd:
    finalizeCycle(skill)
    startNewCycle(skill)
```

`startNewCycle(skill)`
```
if missionsAssignedTo(skill).length >= 8:
  skill.cycleStart = now.alignToCadence(skill.cycleType)
  skill.cycleEnd = nextBoundary(skill.cycleType, dayStartsAt)
  skill.targetMissionId = uniformPick(missionsAssignedTo(skill))
  skill.hasHitTargetThisCycle = false
  save(skill)
else:
  clearTarget(skill) // not ready this cycle
```

### 6.2 Completing a mission
```
complete(mission):
  // base credit always
  grantBaseXP(player, mission)
  for each skill in mission.skillIds:
    if alreadyCreditedThisCycle(mission, skill): continue
    markCredited(mission, skill)
    if skill.targetMissionId == mission.id && !skill.hasHitTargetThisCycle:
      grantCycleXP(player, skill, mission)
      skill.hasHitTargetThisCycle = true
      save(skill)
  maybePromptReflectionToken()
  appendTimelineEntry()
```

`alreadyCreditedThisCycle` uses `cycleId = skill.id + ':' + skill.cycleStartISO` and searches `completions` for a match.

### 6.3 Reflection Token selection (rate‑limited)
```
if eligible:
  p = 0.10
  if rand() < p and dailyCount < 2 and skillCycleCount < 7:
    showOneLinerPrompt()
    saveJournalEntry(isReflectionToken=true)
```

### 6.4 Time Capsule evaluation
- **Date**: on tick, unlock if `now >= unlockParams.date`.
- **Mission**: on mission completion, unlock capsules whose `unlockParams.missionId == mission.id`.
- **Skill level**: on skill level‑up, unlock capsules with matching `skillId` and `level <= skill.level`.
- **Level**: on player level‑up, unlock capsules with `level <= player.level`.

---

## 7) Screens (single‑user)
- **Home**: Level bar, Coins, Energy slider (1–5), Class name (editable via Profile), suggested missions (sorted by Energy proximity, due date, uncredited‑this‑cycle), metrics chips (Cycle XP · Variety · Consistency – display only).
- **Missions**: List + filters (All/Today/Upcoming/Recurring/Completed), quick add, detail sheet with skill chips, difficulty, energy, schedule, reminders, and one‑credit‑per‑cycle info line. Action: “Add Time Capsule for this mission…”.
- **Skills**: cards with Level (+Depth ring if Focus), `Ready x/8`, cycle cadence selector, cycle countdown, chips for Variety/Consistency; detail view lists assigned missions and which are uncredited this cycle. Action: “Add Capsule when this skill reaches Level …”.
- **Profile (Class)**: edit Class name + description; lifetime stats.
- **Journal**: freeform entries, Reflections subfilter, Capsules subfilter. Entries are local; search by text/skill/mission.
- **Rewards**: user‑defined shop; coins deduct on redemption; logged to Timeline.
- **Timeline**: reverse‑chrono feed of completions, reflections, capsule unlocks.
- **Settings**: theme, day start, export/import, per‑skill advanced (reveal target toggle, change cycle cadence), privacy (capsule encryption toggle, reflection frequency).

---

## 8) Testing plan (offline)
- **Unit**: progression math (base/cycle XP), level thresholds, cycle boundary math (cadences, dayStartsAt), one‑credit‑per‑cycle, target seeding.
- **Widget**: add/edit mission, completion flow, skill card chips, profile edits, journal/capsule CRUD.
- **Golden**: Home, Missions, Skills (light/dark, large text).
- **Property‑based**: cycle boundary fuzzing (random date inputs), variety computation sanity.

---

## 9) Performance & resilience
- Hive lookups are O(1) per entity; lists are small (single user). Cache `missionsCount` per skill to avoid repeated counts. Lazy‑load Timeline. No network code.
- Time arithmetic centralized (one utility for all boundary calculations). All random picks persisted once at cycle start (no reseeding).

---

## 10) Privacy, safety, and non‑goals
- **Private by default:** all local; no trackers. Export with optional passphrase.
- **No manipulative randomness:** no loot boxes, no variable‑ratio XP, no punitive damage by default.
- **Non‑goals for v1:** no accounts, no sync, no multiplayer, no server.

---

## 11) Build checklist (MVP)
1. Models + Hive adapters; boxes open.
2. ProgressionService + CycleService wired to completion flow.
3. Missions CRUD + completion; one‑credit‑per‑cycle enforcement in UI (✓ badge).
4. Skills screen: cadence selector, readiness meter, cycle countdown; optional reveal toggle.
5. Profile/Class editor.
6. Journal (freeform) + Reflection Token prompt (rate‑limited).
7. Time Capsules: create → unlock flows → archive to Journal.
8. Export/Import JSON; Settings (day start, privacy toggles).
9. Polish (animations, toasts), a11y, light/dark.

---

## 12) Stretch (after MVP)
- Variety & Consistency chips with simple heuristics.
- Optional Focus mode (half‑speed) toggle per skill.
- iOS/Android widgets for quick add/complete.
- Optional iCloud/Drive backup (still offline by default).

---

## 13) Why this is buildable & valuable
- **Small surface area:** no auth, no backend, no social. It’s a clean, deterministic app with a tight loop and a few services.
- **Clear mechanics:** anti‑grind rules are legible and easy to implement/test.
- **Meaning over metrics:** journaling and capsules deepen motivation without turning writing into a points economy.
- **Technical fit:** Flutter + Hive gives us fast iteration, native feel, and true offline capability.

> In short: OuRPG is a calm, privacy‑first life RPG that rewards real variety and honest cadence, not button‑mashing. It’s deliberately simple to build and resilient to gaming. Perfect for a single engineer to ship an MVP and iterate.

