# Code Review: streamlit_app.py

## 🔴 CRITICAL BUGS

### 1. **Missing `save_session()` after extending time (Line 1136)**
**Location:** `page_extend_time()` function, line 1136
**Issue:** When extending time, `task.timer_minutes` is updated but the session is never saved. If the app crashes or user navigates away, the extended time is lost.
**Fix:** Add `st.session_state.storage.save_session(session)` after line 1136.

```python
# Current (BUGGY):
task.timer_minutes += extra_minutes
st.session_state.page = "run_session"
st.rerun()

# Should be:
task.timer_minutes += extra_minutes
st.session_state.storage.save_session(session)  # ADD THIS
st.session_state.page = "run_session"
st.rerun()
```

### 2. **`time.sleep(1)` blocks UI (Line 809)**
**Location:** `page_adjust_time()` function, line 809
**Issue:** `time.sleep(1)` in Streamlit blocks the entire app UI. The success message won't be visible properly, and it creates poor UX.
**Fix:** Remove `time.sleep(1)` and just use `st.rerun()` immediately. The success message pattern doesn't work well in Streamlit's rerun model.

```python
# Current (BUGGY):
st.success(f"Updated to {new_time} minutes!")
time.sleep(1)  # ❌ Blocks entire app
st.session_state.page = "confirm_tasks"
st.rerun()

# Should be:
st.session_state.storage.save_session(session)
st.session_state.page = "confirm_tasks"
st.rerun()  # Success message won't persist, but that's OK
```

---

## ⚠️ POTENTIAL ISSUES

### 3. **Overly Complex JavaScript Injection (Lines 468-582)**
**Location:** `page_home()` function
**Issue:** 115 lines of JavaScript injected via `components.html()` to style buttons. This is:
- Hard to maintain
- May not work reliably across browsers
- Could be simplified with CSS or removed if styling isn't critical
**Recommendation:** Consider removing or simplifying. The CSS already styles buttons (lines 102-132), so this JavaScript might be redundant.

### 4. **Redundant `save_session()` calls (Multiple locations)**
**Location:** Lines 937, 939, 1083, 1085, 1098, 1100
**Issue:** Some functions call `save_session()` twice in a row (e.g., after `task.skip()` and after `session.next_task()`). While not a bug, it's inefficient.
**Example:**
```python
# Lines 936-940:
task.skip()
st.session_state.storage.save_session(session)  # Save 1
session.next_task()
st.session_state.storage.save_session(session)  # Save 2 (redundant)
```
**Recommendation:** Save once after all changes are made.

### 5. **Timer loop with `time.sleep(1)` (Line 1022)**
**Location:** `run_timer()` function
**Issue:** While necessary for countdown, the combination of `time.sleep(1)` + `st.rerun()` in a while loop can cause performance issues and high CPU usage.
**Status:** This is actually correct for Streamlit's model, but could be optimized with `st.empty()` placeholders (which you're already using - good!).

---

## 🟡 CODE QUALITY ISSUES

### 6. **Unused/Redundant Function: `show_confetti()` (Line 358)**
**Location:** Line 358-360
**Issue:** Function is only used once (line 1191). Could be inlined.
**Recommendation:** Either keep it for clarity or inline it:
```python
# Current:
def show_confetti():
    st.balloons()

# Could be:
st.balloons()  # Direct call
```

### 7. **Comment doesn't match behavior (Line 1133)**
**Location:** `page_extend_time()`, line 1133
**Issue:** Comment says "Update task timer for display purposes" but it's actually updating persistent data.
**Fix:** Update comment to reflect that it's updating persistent data:
```python
# Current comment:
# Update task timer for display purposes - add extra time to original

# Better comment:
# Update task timer to track total allocated time (persistent data)
```

### 8. **Complex CSS that could be simplified**
**Location:** Lines 35-301
**Issue:** 267 lines of CSS. While not a bug, it's a lot to maintain.
**Status:** This is intentional styling, so it's acceptable. But consider extracting to a separate CSS file if it grows.

---

## ✅ GOOD PRACTICES FOUND

1. ✅ Proper session state initialization
2. ✅ Good error handling for missing sessions
3. ✅ Proper use of `st.rerun()` for navigation
4. ✅ Good separation of concerns (page functions)

---

## 📋 SUMMARY OF FIXES

**✅ FIXED (Priority 1 - Critical Bugs):**
1. ✅ Added `save_session()` after extending time (line 1136)
2. ✅ Removed `time.sleep(1)` from line 809 (was blocking UI)
3. ✅ Updated comment on line 1133 to be more accurate
4. ✅ Optimized redundant `save_session()` calls (lines 934-937, 1080-1083, 1094-1098)

**✅ FIXED (Priority 2 - Code Quality):**
5. ✅ Removed all JavaScript injection (115 lines removed) - No JavaScript in project
6. ✅ Removed unused `components.html` import
7. ✅ Inlined `show_confetti()` function - replaced with direct `st.balloons()` call

**✅ ALL ISSUES RESOLVED!**
