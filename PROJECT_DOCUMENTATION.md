# CS5001 Final Project - Comprehensive Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [File Structure](#file-structure)
7. [Object-Oriented Design](#object-oriented-design)
8. [Technical Details](#technical-details)
9. [Development Guide](#development-guide)
10. [Contributors](#contributors)

---

## Project Overview

### What is This Project?

**CS5001 Final Project** is a comprehensive productivity application designed to help users overcome procrastination and accomplish difficult tasks. The application combines two complementary tools:

1. **AI Task Coach** - An intelligent task breakdown system that uses Google's Gemini AI to break overwhelming goals into manageable, time-boxed tasks
2. **Quick Daily Tasks** - A simple task manager for day-to-day to-do items

The project is built with **Python** and provides both a **command-line interface (CLI)** and a **web-based interface** using Streamlit.

### Core Philosophy

The application addresses the common problem of procrastination by:
- **Breaking down large goals** into small, actionable steps (5-40 minutes each)
- **Using AI** to intelligently decompose complex tasks
- **Time-boxing** each task with countdown timers
- **Gamifying progress** with encouragement messages and progress tracking
- **Persisting sessions** so users can pause and resume work

### Target Users

- Students facing overwhelming assignments
- Professionals with complex projects
- Anyone struggling with procrastination
- People who benefit from structured task breakdown

---

## Features

### AI Task Coach Features

#### 1. **AI-Powered Task Breakdown**
- Input a goal (e.g., "Write an essay on climate change")
- AI breaks it down into 3-5 manageable tasks
- Each task has a realistic time estimate (5-40 minutes)
- Tasks are ordered from simplest to more complex

#### 2. **Smart Task Adjustment**
- **"Too Hard"** - Regenerate simpler, smaller tasks
- **"Not Enough Detail"** - Generate more comprehensive steps
- **"Different Focus"** - Specify a particular area to concentrate on
- Up to 3 regeneration attempts per session

#### 3. **Time Management**
- Countdown timer for each task
- Visual progress bar showing completion percentage
- Pause/resume functionality
- Extend time if needed
- Skip tasks if necessary

#### 4. **Session Management**
- Save and resume unfinished sessions
- View history of completed goals
- Track progress across multiple sessions
- Automatic session persistence (JSON storage)

#### 5. **User Interface Options**
- **CLI Version** (`task_coach.py`) - Terminal-based interface
- **Web Version** (`streamlit_app.py`) - Modern, beautiful web UI with:
  - Soft UI design with gradients
  - Animated task cards
  - Real-time timer with progress visualization
  - Responsive layout

#### 6. **Motivation & Gamification**
- Encouragement messages when completing tasks
- Celebration animations (confetti, balloons)
- Progress tracking and statistics
- Motivational quotes

### Quick Daily Tasks Features

#### 1. **Simple Task Management**
- Add tasks to a list
- Mark tasks as completed
- Remove tasks
- View completed task history

#### 2. **Motivational Elements**
- Random motivational quotes on home page
- Compliment messages when completing tasks
- Celebration animations

#### 3. **Data Persistence**
- Tasks saved to JSON file (`/tmp/cs5001_tasklist.json`)
- Persistent across sessions

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    main.py (Entry Point)                │
│  ┌──────────────────────┐  ┌────────────────────────┐ │
│  │  AI Task Coach       │  │  Quick Daily Tasks      │ │
│  │  (Strategic Planning)│  │  (Task Manager)         │ │
│  └──────────────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### AI Task Coach Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │  task_coach.py   │          │ streamlit_app.py │         │
│  │  (CLI Orchestrator)        │  (Web UI Router)  │         │
│  └──────────────────┘          └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                     │
┌───────▼──────┐  ┌─────────▼─────────┐  ┌──────▼──────┐
│  Domain      │  │  Service Layer    │  │  Data Layer │
│  Models      │  │                   │  │             │
├──────────────┤  ├───────────────────┤  ├─────────────┤
│ Session      │  │ AIHelper          │  │ Storage     │
│ Task         │  │ Timer             │  │ (JSON)      │
└──────────────┘  │ Display           │  └─────────────┘
                  │ InputHandler      │
                  └───────────────────┘
```

### Component Responsibilities

#### **Domain Models**
- **`Session`** - Represents a complete task breakdown session
- **`Task`** - Represents a single atomic task

#### **Service Layer**
- **`AIHelper`** - Interfaces with Gemini AI for task breakdown
- **`Timer`** - Countdown timer with pause/resume
- **`Display`** - Terminal output formatting (CLI)
- **`InputHandler`** - User input collection and validation (CLI)

#### **Data Layer**
- **`Storage`** - Persistence to/from JSON files

#### **Application Layer**
- **`TaskCoach`** - CLI orchestrator, coordinates all components
- **`streamlit_app.py`** - Web UI, functional programming approach

---

## Installation & Setup

### Prerequisites

- **Python 3.13+** (specified in `pyproject.toml`)
- **uv** - Python package manager ([Installation Guide](https://github.com/astral-sh/uv))
- **Google Gemini API Key** - For AI task breakdown

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd CS5001_final_project
```

### Step 2: Install Dependencies

The project uses `uv` for dependency management:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync
```

This will install:
- `google-generativeai` - For Gemini AI integration
- `pytest` - For testing
- `python-dotenv` - For environment variable management
- `streamlit` - For web UI (if not already installed)

### Step 3: Configure API Key

1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   To get a Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy it to your `.env` file

### Step 4: Verify Installation

```bash
# Run the web application
uv run streamlit run main.py
```

The application should open in your browser at `http://localhost:8501`

---

## Usage Guide

### Starting the Application

#### Web Interface (Recommended)

```bash
uv run streamlit run main.py
```

This opens the main menu where you can choose:
- **🗺️ Strategic Planning (AI Coach)** - For breaking down complex goals
- **✅ Quick Daily Tasks (Task Manager)** - For simple to-do lists

#### CLI Interface

```bash
# Run the CLI version of AI Task Coach
uv run python -m ai_task_coach.task_coach
```

### Using AI Task Coach

#### 1. **Start a New Goal**

1. Click "Start a New Goal" (web) or select option 1 (CLI)
2. Enter your goal (be specific!):
   - ✅ Good: "Study chapter 3 of discrete math"
   - ❌ Bad: "Study math"
3. Enter how much time you have (in minutes)
4. Wait for AI to break down your goal into tasks

#### 2. **Review and Adjust Tasks**

After AI generates tasks, you can:
- **✅ Start** - Begin working on tasks
- **⏱️ Adjust Time** - Modify time estimates for specific tasks
- **😅 Too Hard** - Regenerate simpler tasks
- **📝 Need More Detail** - Get more comprehensive steps
- **🔍 Specify Topic** - Focus on a particular area

#### 3. **Work Through Tasks**

For each task:
- **Start Timer** - Begin countdown
- **Pause** - Temporarily stop timer
- **Done** - Mark task as completed
- **Skip** - Move to next task
- **Extend Time** - Add more minutes if needed

#### 4. **Session Management**

- **Save & Exit** - Pause session and resume later
- **View History** - See all completed goals
- **Continue Session** - Resume unfinished work

### Using Quick Daily Tasks

1. Click "Quick Daily Tasks" from main menu
2. **Add Task** - Enter a new task
3. **Complete Task** - Mark a task as done (moves to completed list)
4. **Remove Task** - Delete a task
5. **View Completed Tasks** - See your accomplishments
6. **Reset** - Clear all tasks

---

## File Structure

```
CS5001_final_project/
│
├── main.py                          # Main entry point (Streamlit app router)
├── README.md                        # Basic project README
├── PROJECT_DOCUMENTATION.md         # This comprehensive documentation
├── pyproject.toml                  # Project dependencies and metadata
├── uv.lock                         # Locked dependency versions
│
├── .env                            # Environment variables (API keys) - NOT in git
├── .gitignore                      # Git ignore rules
├── .python-version                 # Python version specification
│
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                # Streamlit settings
│
├── ai_task_coach/                  # AI Task Coach module
│   ├── __init__.py                # Package marker
│   │
│   ├── task.py                    # Task domain model
│   ├── session.py                # Session domain model
│   │
│   ├── ai_helper.py              # Gemini AI integration
│   ├── storage.py                # JSON persistence layer
│   ├── timer.py                  # Countdown timer
│   ├── display.py                # CLI output formatting
│   ├── input_handler.py          # CLI input collection
│   │
│   ├── task_coach.py             # CLI orchestrator
│   ├── streamlit_app.py          # Web UI implementation
│   │
│   ├── config.py                 # Configuration (API keys)
│   │
│   ├── tests/                    # Test suite
│   │   ├── pytest.ini
│   │   └── test_critical_functions.py
│   │
│   ├── OOP_ANALYSIS_REPORT.md    # Detailed OOP analysis
│   └── INPUT_HANDLER_ANALYSIS.md # InputHandler design analysis
│
├── task_app.py                    # Quick Daily Tasks implementation
├── test_task_app.py               # Tests for task_app
│
├── quotes.py                      # Motivational quotes collection
└── compliment_quotes.py          # Compliment messages collection
```

### Key Files Explained

#### **main.py**
- Entry point for the Streamlit application
- Routes between AI Task Coach and Quick Daily Tasks
- Handles session state initialization

#### **ai_task_coach/task_coach.py**
- CLI version of AI Task Coach
- Orchestrates all components for terminal interface
- Implements menu-driven workflow

#### **ai_task_coach/streamlit_app.py**
- Web UI implementation
- Page-based routing system
- Beautiful, modern interface with animations

#### **ai_task_coach/ai_helper.py**
- Interfaces with Google Gemini AI
- Validates goals using AI
- Breaks down goals into tasks
- Handles retry logic and error recovery

#### **ai_task_coach/storage.py**
- Manages session persistence
- Saves/loads from JSON files
- Provides query methods (get unfinished, get completed, etc.)

#### **task_app.py**
- Simple task manager implementation
- Handles CRUD operations for tasks
- JSON-based persistence

---

## Object-Oriented Design

### Design Principles

The project follows **SOLID principles** and uses several **design patterns**:

#### **Single Responsibility Principle (SRP)**
Each class has one clear responsibility:
- `Task` - Task state management
- `Session` - Session lifecycle
- `Storage` - Data persistence
- `AIHelper` - AI communication
- `Display` - Output formatting
- `InputHandler` - Input collection

#### **Dependency Injection**
Classes accept dependencies through constructors for testability:
```python
class AIHelper:
    def __init__(self, model=None):  # Injectable model
        ...
    
class Display:
    def __init__(self, print_func=None):  # Injectable print function
        ...
```

#### **Composition over Inheritance**
- `TaskCoach` composes multiple services (Storage, AIHelper, Timer, etc.)
- `Session` contains a list of `Task` objects
- No inheritance hierarchy

### Design Patterns Used

1. **Repository Pattern** (`Storage`)
   - Abstracts data access
   - Provides clean interface for persistence

2. **Facade Pattern** (`TaskCoach`)
   - Simplifies complex subsystem interactions
   - Single entry point for CLI application

3. **Adapter Pattern** (`AIHelper`)
   - Adapts Gemini AI API to application needs
   - Isolates external system changes

4. **Aggregate Pattern** (`Session`)
   - Contains and manages collection of `Task` objects
   - Maintains consistency boundaries

5. **Strategy Pattern** (`Display`, `InputHandler`)
   - Injectable functions for different behaviors
   - Enables testing and flexibility

### Class Relationships

```
TaskCoach (Facade)
    ├── composes → Storage (Repository)
    ├── composes → AIHelper (Adapter)
    ├── composes → Timer
    ├── composes → Display (View)
    ├── composes → InputHandler (Controller)
    └── manages → Session (Aggregate)
            └── contains → List[Task] (Entity)

Storage (Repository)
    ├── serializes → Session
    └── deserializes → Session

AIHelper (Adapter)
    └── creates → List[Task]

InputHandler (Controller)
    └── uses → AIHelper (optional, for validation)
```

### Detailed OOP Analysis

For a comprehensive analysis of the OOP design, see:
- **`ai_task_coach/OOP_ANALYSIS_REPORT.md`** - Detailed file-by-file OOP analysis
- **`ai_task_coach/INPUT_HANDLER_ANALYSIS.md`** - Analysis of InputHandler design

---

## Technical Details

### Technology Stack

- **Language:** Python 3.13+
- **Web Framework:** Streamlit
- **AI Service:** Google Gemini 2.0 Flash
- **Data Storage:** JSON files
- **Package Management:** uv
- **Testing:** pytest

### Data Models

#### **Task**
```python
{
    "task_number": 1,
    "description": "Open document and create outline",
    "timer_minutes": 10,
    "status": "pending"  # or "completed", "skipped"
}
```

#### **Session**
```python
{
    "session_id": "uuid-string",
    "goal": "Write an essay",
    "time_available": 60,
    "status": "in_progress",  # or "paused", "completed"
    "current_task": 0,
    "created_at": "2025-01-15 10:30:00",
    "tasks": [/* Task objects */]
}
```

### AI Integration

#### **Model Used**
- **Gemini 2.0 Flash** - Fast, efficient model for task breakdown

#### **Prompt Engineering**
The AI is prompted with:
- User's goal
- Available time
- Adjustment preferences (if any)
- Focus area (if specified)

#### **Response Format**
AI responds in structured format:
```
1 | Open document | 5
2 | Write introduction | 15
3 | Write body paragraphs | 20
```

This is parsed into `Task` objects.

### Persistence

#### **Storage Location**
- **Sessions:** `data/sessions.json` (created automatically)
- **Quick Tasks:** `/tmp/cs5001_tasklist.json`

#### **File Structure**
```json
{
  "session-uuid-1": {
    "session_id": "uuid-1",
    "goal": "Write essay",
    "status": "completed",
    "tasks": [...]
  },
  "session-uuid-2": {...}
}
```

### Timer Implementation

#### **CLI Timer**
- Non-blocking input detection using `select`
- Visual progress bar with Unicode characters
- System sound alerts (platform-specific)
- Pause/resume functionality

#### **Web Timer**
- Streamlit's `st.rerun()` for real-time updates
- HTML/CSS progress bars
- Visual countdown display
- Pause/resume via session state

### Error Handling

- **AI Failures:** Retry logic (3 attempts) with graceful degradation
- **File I/O:** Try-except blocks with fallback to empty data
- **Invalid Input:** Validation loops until valid input received
- **API Errors:** Returns `None` and allows caller to handle

---

## Development Guide

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest ai_task_coach/tests/test_critical_functions.py

# Run with verbose output
uv run pytest -v
```

### Code Style

The project follows Python PEP 8 style guidelines:
- 4 spaces for indentation
- Descriptive variable names
- Docstrings for classes and methods
- Type hints where appropriate

### Adding New Features

#### **Adding a New AI Adjustment Type**

1. Update `ai_helper.py`:
   ```python
   def _build_prompt(self, goal, time_available, adjust=None, focus=None):
       # Add new adjust type handling
       if adjust == "new_type":
           prompt += "New adjustment instructions..."
   ```

2. Update `task_coach.py`:
   ```python
   def _show_confirm_menu(self, ...):
       # Add menu option
       print("6. New adjustment type")
   ```

3. Update `streamlit_app.py`:
   ```python
   # Add button in confirm_tasks page
   if st.button("New Adjustment", ...):
       regenerate_tasks("new_type")
   ```

#### **Adding a New Display Method**

1. Add method to `display.py`:
   ```python
   def show_new_feature(self, data):
       """Display new feature."""
       self._print(f"New feature: {data}")
   ```

2. Use in `task_coach.py`:
   ```python
   self.display.show_new_feature(data)
   ```

### Debugging

#### **CLI Debugging**
- Add `print()` statements (will be removed in production)
- Use Python debugger: `import pdb; pdb.set_trace()`

#### **Streamlit Debugging**
- Use `st.write()` to display variable values
- Check browser console for JavaScript errors
- Use Streamlit's built-in debugger

### Environment Variables

Required:
- `GEMINI_API_KEY` - Google Gemini API key

Optional:
- `STREAMLIT_SERVER_PORT` - Port for Streamlit (default: 8501)
- `STREAMLIT_THEME_*` - Streamlit theme customization

---

## Project Statistics

- **Total Files:** ~20 Python files
- **Lines of Code:** ~3,500+ lines
- **Classes:** 8 main classes
- **Test Coverage:** Critical functions tested
- **Dependencies:** 4 main packages

---

## Known Issues & Limitations

1. **InputHandler Overlap**
   - `InputHandler` mixes input and output (overlaps with `Display`)
   - See `INPUT_HANDLER_ANALYSIS.md` for detailed analysis
   - Potential refactoring: Merge into `CLIInterface`

2. **CLI Timer Platform Support**
   - Non-blocking input uses Unix `select` - may not work perfectly on Windows
   - Fallback to blocking input on unsupported platforms

3. **Session Storage**
   - Currently uses JSON files (not suitable for production scale)
   - No database support
   - No user authentication

4. **AI Rate Limiting**
   - No explicit rate limiting handling
   - Relies on Gemini API's built-in limits

---

## Future Enhancements

### Potential Improvements

1. **Database Integration**
   - Replace JSON with SQLite or PostgreSQL
   - Support multiple users
   - User authentication

2. **Enhanced AI Features**
   - Learning from user preferences
   - Customizable prompt templates
   - Multiple AI model support

3. **Analytics & Reporting**
   - Time tracking analytics
   - Productivity insights
   - Goal completion statistics

4. **Mobile App**
   - Native iOS/Android apps
   - Push notifications
   - Offline support

5. **Collaboration Features**
   - Shared goals
   - Team task breakdown
   - Progress sharing

---

## Contributors

### Primary Contributors

- **Hyunjoo Shim (NUID: 002505607)**
  - AI Task Coach module (`ai_task_coach/`)
  - OOP design and architecture
  - AI integration and task breakdown logic

- **Sakura Hashimoto (NUID: 003186429)**
  - Quick Daily Tasks module (`task_app.py`)
  - Main application router (`main.py`)
  - Motivational quotes and UI elements

### Acknowledgments

- Google Gemini AI team for the API
- Streamlit team for the web framework
- CS5001 course instructors

---

## License

This project is developed as part of CS5001 coursework. Please refer to the course guidelines for usage and distribution policies.

---

## Support & Contact

For questions or issues:
1. Check this documentation
2. Review code comments
3. Consult OOP analysis reports in `ai_task_coach/`
4. Contact course instructors

---

## Appendix

### A. Quick Reference Commands

```bash
# Run web app
uv run streamlit run main.py

# Run CLI version
uv run python -m ai_task_coach.task_coach

# Run tests
uv run pytest

# Install new dependency
uv add package-name

# Sync dependencies
uv sync
```

### B. File Locations Reference

- **Sessions Data:** `data/sessions.json`
- **Quick Tasks Data:** `/tmp/cs5001_tasklist.json`
- **Environment Variables:** `.env` (root directory)
- **Streamlit Config:** `.streamlit/config.toml`

### C. API Reference

#### **AIHelper Methods**
- `validate_goal(goal: str) -> bool`
- `break_down_goal(goal, time, adjust, focus, retries) -> List[Task]`

#### **Storage Methods**
- `save_session(session: Session) -> None`
- `get_session_by_id(session_id) -> Session | None`
- `get_unfinished_session() -> Session | None`
- `get_completed_sessions() -> List[Session]`

#### **Session Methods**
- `pause() -> None`
- `complete() -> None`
- `get_current_task() -> Task | None`
- `next_task() -> None`

---

**Last Updated:** January 2025  
**Version:** 1.0.0  
**Status:** Production Ready
