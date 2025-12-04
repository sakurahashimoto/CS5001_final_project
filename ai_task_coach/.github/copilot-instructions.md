# AI Task Coach - AI Agent Instructions

## Project Overview

**AI Task Coach** is a CLI productivity application that breaks down overwhelming goals into manageable tasks using Gemini AI. Users provide a goal (e.g., "Write an essay"), the app creates a task breakdown with time estimates, and guides users through execution with a countdown timer and session persistence.

**Key domains:** Procrastination management, task decomposition, session state management, Gemini AI integration.

---

## Architecture & Data Flow

### Core Components

1. **`task_coach.py`** - Main orchestrator
   - Entry point; coordinates all other components
   - Handles user menu (new session, history, resume unfinished)
   - Manages session lifecycle (create → confirm tasks → run → complete)
   - Handles task regeneration loops (too hard / not enough / different approach)
   - Known issue: TODO comment indicates skip logic sometimes advances 2 tasks instead of 1

2. **`session.py`** - Session model
   - Represents one complete task breakdown session
   - State: `in_progress` (active), `paused` (user quit), `completed` (finished)
   - Tracks `current_task` index (0-based) and list of Task objects
   - Generated with UUID; includes `created_at` timestamp

3. **`task.py`** - Individual task model
   - Immutable structure: task_number, description, timer_minutes, status
   - Status values: `"pending"`, `"completed"`, `"skipped"`
   - Methods: `complete()`, `skip()`, `update_time()`, `to_dict()` for serialization

4. **`ai_helper.py`** - Gemini AI integration
   - **Model:** `gemini-2.0-flash` (configured in `config.py`)
   - `break_down_goal(goal, adjust=None, retries=3)` - Main entry point
   - `adjust` parameter enables regeneration: `"too_hard"` (simplify), `"not_enough"` (expand), `"different"` (alternative approach)
   - **Response format:** Parses `[number] | [description] | [timer_minutes]` lines into Task objects
   - Returns `None` if all retries fail; calling code retries indefinitely

5. **`storage.py`** - Persistent session storage
   - **Format:** JSON with session_id as key, Session dict as value
   - **File:** `data/sessions.json` (auto-created on first run)
   - Core methods: `save_session()`, `get_session_by_id()`, `get_unfinished_session()`, `get_completed_sessions()`, `delete_session()`
   - Bidirectional conversion: `Session ↔ dict` via `to_dict()` and `_dict_to_session()`

6. **`timer.py`** - Task countdown timer
   - Uses threading for concurrent timer + user input listening
   - Return value: `"completed"` (full time) or `"stopped"` (user pressed Enter)
   - Displays progress bar with visual feedback

7. **`display.py`** - UI/UX layer
   - Emoji-based task status icons: `⬜` pending, `✅` completed, `⏭️` skipped
   - Randomized encouragement messages for different outcomes
   - Session summary reporting (completed/skipped counts)

8. **`config.py`** - Environment configuration
   - Centralizes API keys via `.env`
   - Currently: `GEMINI_API_KEY` only

---

## Data Model & State Management

### Session Lifecycle
```
User Input → AIHelper breaks down goal → Session created → show_tasks() → user confirms/regenerates
→ _run_session() loop → per-task: timer → completion dialog → next_task() → complete() when no tasks left
→ summary + save to storage
```

### JSON Schema Example
```json
{
  "8ccacbf0-0ec4-49c2-8751-d7feb71af71c": {
    "session_id": "8ccacbf0-0ec4-49c2-8751-d7feb71af71c",
    "goal": "Write essay",
    "status": "completed",
    "current_task": 3,
    "created_at": "2025-11-27 23:36:11",
    "tasks": [
      {"task_number": 1, "description": "Open document", "timer_minutes": 5, "status": "completed"},
      {"task_number": 2, "description": "Write intro", "timer_minutes": 10, "status": "completed"},
      {"task_number": 3, "description": "Draft body", "timer_minutes": 20, "status": "skipped"}
    ]
  }
}
```

---

## Developer Workflows

### Running the App
```bash
cd /Users/joo/CS5001_final_project/ai_task_coach
python task_coach.py
```

### Testing & Debugging
- **No automated test suite exists.** Manual testing via CLI required.
- **Debugging notes:**
  - Timer display overwrites via `\r` (carriage return)
  - Known bug: skip task advancement may double-advance (see TODO in `_run_session()`)
  - AI parsing assumes strict `[number] | [description] | [minutes]` format; deviations return empty list

### Environment Setup
- Requires `.env` file with `GEMINI_API_KEY` (Gemini API v2.0-flash)
- `data/` directory auto-created on first run
- Python 3.x required; uses `google-generativeai`, `python-dotenv`

---

## Code Patterns & Conventions

### State Persistence Pattern
Every mutable state change (task completion, time adjustment, regeneration) calls `storage.save_session()` immediately. This ensures crash resilience—sessions recover via `get_unfinished_session()`.

### User Loop Pattern
Most workflows follow:
1. Show menu → get choice
2. Invalid choice → recursively call same method
3. Valid choice → call next workflow method

Example: `_confirm_tasks()` → recursive on invalid input → calls `_run_session()` on acceptance.

### AI Regeneration Caps
Limited to 3 regeneration attempts (controlled by `regenerate_count` parameter). After 3, the UI no longer shows regeneration options—prevents infinite loops.

### UI/Status Conventions
- Status icons: `⬜` = pending, `✅` = completed, `⏭️` = skipped, emoji in messages convey tone
- Task display: always `Task N: description (Xm min)` format

---

## Integration Points & External Dependencies

### Gemini AI (google-generativeai)
- **Configuration:** `config.py` loads `GEMINI_API_KEY` from `.env`
- **Usage:** `AIHelper._call_ai(prompt)` sends prompt; catches all exceptions, returns `None` on failure
- **Robustness:** Caller (_break_down_goal_) retries 3 times before giving up

### File I/O (data/sessions.json)
- Single source of truth for all sessions
- No locking mechanism—not thread-safe for concurrent writes
- `json.JSONDecodeError` handled gracefully (returns empty dict)

### CLI Input/Output
- Input: `input()` function (blocking)
- Output: Direct `print()` statements; timer uses `\r` for overwrite
- No alternative UI layers (web, GUI)

---

## Cross-Component Communication

- **task_coach.py ↔ storage.py:** Session persistence
- **task_coach.py ↔ ai_helper.py:** Goal breakdown + regeneration
- **task_coach.py ↔ timer.py:** Timer lifecycle for each task
- **task_coach.py ↔ display.py:** All user messages (encouragement, summaries, task lists)
- **ai_helper.py ↔ config.py:** API key retrieval
- **session.py, task.py:** Bidirectional dict conversion for JSON serialization via storage.py

---

## Common Modifications

### Adding a New AI Adjustment Type
1. Add `elif adjust == "new_type"` in `AIHelper._build_prompt()`
2. Add UI option in `TaskCoach._confirm_tasks()`
3. Call `_regenerate("new_type", count)` on user selection

### Changing Task Status Values
Affects: `Task.status` values (pending/completed/skipped), `Display._get_status_icon()` emoji mapping, `Storage._dict_to_session()` parsing.

### Modifying Timer Behavior
- Duration: `Timer.start(minutes)`
- Early exit: caught in `_wait_for_input()` thread
- Display: `_display_time()` controls format; 20-char progress bar hardcoded

### Adding Persistence to New Fields
Update `to_dict()` and `_dict_to_session()` in both `Session` and `Task` classes.

---

## Edge Cases & Gotchas

1. **Crash during session:** `_handle_unfinished()` recovers via `get_unfinished_session()` - retrieves first paused/in-progress session (not random).
2. **AI response parsing:** Expects exactly 3 `|`-separated parts. Blank lines or extra fields return empty list, triggering retry.
3. **Timer thread:** Daemon thread won't block app shutdown, but may orphan input listener.
4. **Regeneration caps:** After 3 regenerations, UI hides options but doesn't prevent code-level calls.
5. **Storage file corruption:** Any `JSONDecodeError` silently returns `{}`, losing all data—consider backup pattern.

---

## Testing Checklist

- [ ] Create new goal → AI breaks down → confirm → run through all tasks
- [ ] Skip a task → verify status updates correctly
- [ ] Extend time on task → verify timer restarts
- [ ] Quit session → verify recovery on restart
- [ ] Regenerate 3x → verify UI hides further options
- [ ] View history → verify only completed sessions shown
- [ ] Adjust task time → verify persisted to JSON

