"""
Hyunjoo Shim (NUID: 002505607)
streamlit_app.py
Streamlit web UI for the Task Coach app.
Run with: streamlit run ai_task_coach/streamlit_app.py
"""

import streamlit as st
import time
import random
import sys
import os
import quotes

# Add the ai_task_coach directory to Python path so imports work when running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from storage import Storage
from ai_helper import AIHelper
from session import Session
from task import Task

# PAGE CONFIG & STYLING

st.set_page_config(
    page_title="Scratch One More!",
    page_icon="✏️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Soft UI design with subtle gradients
def set_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap');
        
        /* BACKGROUND - clean white */
        .stApp {
            background: #FFFFFF;
            background-attachment: fixed;
            min-height: 100vh;
        }
        
        /* TYPOGRAPHY */
        h1, h2, h3 {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 700 !important;
            color: #2D2A26 !important;
        }
        
        p, li, label, .stMarkdown, span {
            font-family: 'DM Sans', sans-serif !important;
            color: #4A4540 !important;
        }
        
        /* TASK CARDS - soft cream with diffused shadows */
        .task-card {
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            border-radius: 24px;
            padding: 22px 26px;
            margin: 14px 0;
            border: none;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 6px 24px rgba(180, 140, 100, 0.1);
            transition: all 0.3s ease;
        }
        
        .task-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 12px 36px rgba(180, 140, 100, 0.14);
        }
        
        .task-card-completed {
            background: linear-gradient(135deg, #E8EFD5 0%, #E0E8CB 100%);
        }
        
        .task-card-skipped {
            background: linear-gradient(135deg, #FFF5EE 0%, #FFE8D9 100%);
            opacity: 0.85;
        }
        
        .task-card-current {
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            box-shadow: 0 6px 25px rgba(180, 140, 100, 0.2);
            border: 2px solid rgba(200, 160, 100, 0.2);
        }
        
        /* TIMER DISPLAY */
        .timer-display {
            font-family: 'DM Mono', monospace !important;
            font-size: 4.5rem !important;
            font-weight: 500;
            text-align: center;
            color: #2D2A26;
            margin: 30px 0;
            letter-spacing: -2px;
        }
        
        /* SOFT UI BUTTONS - soft light yellow/cream */
        .stButton > button {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border-radius: 50px !important;
            padding: 0.75rem 1.8rem !important;
            transition: all 0.3s ease !important;
            background: linear-gradient(135deg, #FFFDF5 0%, #FFF8E8 100%) !important;
            color: #2D2A26 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 6px 20px rgba(180, 160, 100, 0.1) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 10px 30px rgba(180, 160, 100, 0.14) !important;
            background: linear-gradient(135deg, #FFFBE8 0%, #FFF5DC 100%) !important;
        }
        
        /* Primary buttons - Softer light sage green */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #E2ECC8 0%, #D8E5BC 100%) !important;
            color: #4A5540 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 6px 20px rgba(165, 185, 120, 0.2) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #DAE6BC 0%, #D0DEB0 100%) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 10px 30px rgba(165, 185, 120, 0.28) !important;
        }
        
        /* PROGRESS BAR */
        .stProgress > div {
            height: 10px !important;
            background-color: rgba(255, 255, 255, 0.6) !important;
            border-radius: 10px !important;
        }
        
        .stProgress > div > div {
            height: 10px !important;
            background-color: rgba(255, 255, 255, 0.6) !important;
            border-radius: 10px !important;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #D4B896, #E8CBA8) !important;
            border-radius: 10px !important;
            height: 10px !important;
        }
        
        /* CELEBRATION */
        .celebration {
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            border-radius: 32px;
            margin: 25px 0;
            border: none;
            box-shadow: 0 8px 35px rgba(180, 140, 100, 0.15);
        }
        
        /* HIDE STREAMLIT BRANDING */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* INPUT STYLING */
        .stTextInput > div > div > input {
            font-family: 'DM Sans', sans-serif !important;
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            border: none;
            border-radius: 16px;
            color: #2D2A26 !important;
            padding: 14px 18px !important;
            box-shadow: 0 3px 12px rgba(180, 140, 100, 0.1);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            box-shadow: 0 4px 18px rgba(180, 140, 100, 0.18);
        }
        
        .stNumberInput > div > div > input {
            font-family: 'DM Mono', monospace !important;
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            border: none;
            border-radius: 16px;
            color: #2D2A26 !important;
            box-shadow: 0 3px 12px rgba(180, 140, 100, 0.1);
        }
        
        /* SELECT BOX */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);
            border: none;
            border-radius: 16px;
            box-shadow: 0 3px 12px rgba(180, 140, 100, 0.1);
        }
        
        /* ALERTS/INFO BOXES - light green gradient */
        .stAlert {
            background: linear-gradient(135deg, #E8F5E0 0%, #D8ECCE 100%) !important;
            border-radius: 20px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(140, 180, 100, 0.15) !important;
        }
        
        .stAlert > div {
            background: transparent !important;
            border: none !important;
        }
        
        .stAlert p, .stAlert span {
            color: #3D4A2D !important;
        }
        
        /* METRICS */
        [data-testid="stMetricValue"] {
            font-family: 'DM Mono', monospace !important;
            color: #2D2A26 !important;
        }
        
        /* TIME BADGE IN CARDS - soft yellow-green */
        .time-badge {
            color: #5C6B3D;
            font-family: 'DM Mono', monospace;
            font-weight: 500;
            background: linear-gradient(135deg, #E8EFD5 0%, #DDE6C8 100%);
            padding: 8px 16px;
            border-radius: 20px;
            white-space: nowrap;
            font-size: 0.85rem;
        }
        
        /* ABSTRACT DECORATIVE SHAPES */
        .abstract-shape {
            position: absolute;
            pointer-events: none;
            z-index: 0;
        }
        
        /* BOUNCING ANIMATION for Continue Session button */
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            15% {
                transform: translateY(-8px);
            }
            30% {
                transform: translateY(0);
            }
            45% {
                transform: translateY(-5px);
            }
            60% {
                transform: translateY(0);
            }
            75% {
                transform: translateY(-2px);
            }
            90% {
                transform: translateY(0);
            }
        }
        
        /* Unfinished Session Banner - Light green with mini Continue button */
        .unfinished-session-btn {
            background: linear-gradient(135deg, #E8F5E0 0%, #D8ECCE 100%) !important;
            color: #3D4A2D !important;
            box-shadow: 0 4px 15px rgba(140, 180, 100, 0.15) !important;
            padding: 18px 22px !important;
            padding-right: 120px !important;
            font-weight: 600 !important;
            border-radius: 20px !important;
            position: relative !important;
            text-align: left !important;
            border: none !important;
        }
        
        .unfinished-session-btn:hover {
            background: linear-gradient(135deg, #DCF0D0 0%, #CEEABE 100%) !important;
            box-shadow: 0 6px 20px rgba(140, 180, 100, 0.22) !important;
        }
        
        .unfinished-session-btn::after {
            content: "Continue ▶";
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.75);
            padding: 8px 14px;
            border-radius: 18px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #4A5A38;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        }
    </style>
    """, unsafe_allow_html=True)


# INITIALIZE SESSION STATE & SERVICES

def init_session_state():
    """Initialize all session state variables."""
    if "storage" not in st.session_state:
        st.session_state.storage = Storage()
    
    if "ai" not in st.session_state:
        st.session_state.ai = AIHelper()
    
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    
    if "timer_paused" not in st.session_state:
        st.session_state.timer_paused = False
    
    if "timer_seconds" not in st.session_state:
        st.session_state.timer_seconds = 0
    
    if "regenerate_count" not in st.session_state:
        st.session_state.regenerate_count = 0


# ENCOURAGEMENT MESSAGES - shown when tasks complete

ENCOURAGEMENTS = {
    "completed": [
        "Great job! You did it! 🎉",
        "Amazing work! Keep going! 💪",
        "You're on fire! 🔥",
        "One step closer to done! ⭐",
        "Crushing it! 🚀"
    ],
    "skipped": [
        "No worries, you can come back to it 👌",
        "Sometimes we need to skip ahead. That's okay! 🙂",
        "Moving forward is what matters! ➡️"
    ]
}


def get_encouragement(status):
    """Get a random encouragement message."""
    messages = ENCOURAGEMENTS.get(status, ENCOURAGEMENTS["completed"])
    return random.choice(messages)


# UI COMPONENTS - reusable render functions

def render_quotes():
    """Render a random encouraging quote."""
    random_quote = quotes.get_random_quote()
    quote_parts = random_quote.split('-')
    quote_sentence = quote_parts[0].strip()
    if len(quote_parts) > 1:
        quote_author = quote_parts[1].strip()
        quote_text = f'🎁 "{quote_sentence}" - {quote_author}'
    else:
        quote_text = f'🎁 "{quote_sentence}"'
    # Quote display - simple with quotation marks, larger font, black color
    st.markdown(f"""
    <p style="font-size: 1.8rem; font-weight: 600; font-style: italic; color: #000000; font-family: 'DM Sans', sans-serif; line-height: 1.5; margin: 0 0 20px 0;">{quote_text}</p>
    """, unsafe_allow_html=True)

def render_task_card(task, is_current=False):
    """Render a single task card."""
    # Determine card styling based on status
    if task.status == "completed":
        accent_color = "rgba(180, 200, 140, 0.6)"
        title_color = "#5C6B3D"
        bg_style = "background: linear-gradient(135deg, #F0F5E5 0%, #E8EFD8 100%);"
        border_style = ""
        shadow_style = "0 4px 18px rgba(180, 140, 100, 0.1)"
        animation_style = ""
    elif task.status == "skipped":
        accent_color = "rgba(220, 190, 160, 0.5)"
        title_color = "#9A8570"
        bg_style = "background: linear-gradient(135deg, #FFF8F0 0%, #FFEFE0 100%); opacity: 0.8;"
        border_style = ""
        shadow_style = "0 4px 18px rgba(180, 140, 100, 0.1)"
        animation_style = ""
    elif is_current:
        # Current task - make it highly visible with animation
        accent_color = "rgba(255, 200, 100, 0.8)"
        title_color = "#2D2A26"
        bg_style = "background: linear-gradient(135deg, #FFF9E6 0%, #FFEECC 100%);"
        border_style = "border: 3px solid rgba(240, 200, 150, 0.4);"
        shadow_style = "0 8px 32px rgba(240, 200, 150, 0.2), 0 4px 16px rgba(255, 220, 160, 0.15);"
        animation_style = """
            animation: pulse-glow 2s ease-in-out infinite, subtle-scale 3s ease-in-out infinite;
        """
    else:
        accent_color = "rgba(230, 220, 200, 0.4)"
        title_color = "#6B635A"
        bg_style = "background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%);"
        border_style = ""
        shadow_style = "0 4px 18px rgba(180, 140, 100, 0.1)"
        animation_style = ""
    
    # Add CSS animations for current task
    css_animations = """
    <style>
        @keyframes pulse-glow {
            0%, 100% {
                box-shadow: 0 8px 32px rgba(240, 200, 150, 0.2), 0 4px 16px rgba(255, 220, 160, 0.15);
                border-color: rgba(240, 200, 150, 0.4);
            }
            50% {
                box-shadow: 0 12px 40px rgba(240, 200, 150, 0.3), 0 6px 20px rgba(255, 220, 160, 0.25);
                border-color: rgba(240, 200, 150, 0.6);
            }
        }
        @keyframes subtle-scale {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.02);
            }
        }
    </style>
    """ if is_current else ""
    
    padding = "24px 26px" if is_current else "20px 22px"
    margin = "16px 0" if is_current else "12px 0"
    
    st.markdown(css_animations, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="position: relative; {bg_style} {border_style} border-radius: 20px; padding: {padding}; margin: {margin}; box-shadow: {shadow_style}; overflow: hidden; {animation_style}">
        <div style="position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: radial-gradient(circle, {accent_color} 0%, transparent 70%); border-radius: 50%;"></div>
        <div style="position: relative; z-index: 1;">
            <h4 style="margin: 0 0 8px 0; font-size: {'1.2rem' if is_current else '1.1rem'}; font-weight: {'700' if is_current else '600'}; color: {title_color}; font-family: 'DM Sans', sans-serif;">Task {task.task_number}{' ⭐' if is_current else ''}</h4>
            <p style="margin: 0 0 16px 0; font-size: 0.9rem; color: #7A7268; line-height: 1.5; font-family: 'DM Sans', sans-serif;">{task.description}</p>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="width: 28px; height: 28px; background: rgba(255,255,255,0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; color: #6B635A; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">▶</span>
                <span style="font-size: 0.85rem; color: #8B8078; font-family: 'DM Mono', monospace;">{task.timer_minutes} min</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_welcome():
    """Render the welcome banner."""
    # Welcome box - clean minimal style with large corner blobs
    st.markdown("""
    <div style="position: relative; text-align: center; padding: 55px 40px; background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%); border-radius: 28px; margin-bottom: 35px; box-shadow: 0 8px 40px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04); overflow: hidden;">
        <div style="position: absolute; top: -80px; right: -100px; width: 320px; height: 320px; background: radial-gradient(circle, rgba(195, 215, 150, 0.6) 0%, rgba(195, 215, 150, 0) 60%); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -120px; left: -120px; width: 380px; height: 380px; background: radial-gradient(circle, rgba(235, 200, 170, 0.5) 0%, rgba(235, 200, 170, 0) 60%); border-radius: 50%;"></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 2.4rem; font-weight: 700; margin-bottom: 10px; color: #2D2A26; font-family: 'DM Sans', sans-serif;">Scratch <em style="font-style: italic; font-weight: 500;">One More!</em></h1>
            <p style="font-size: 1rem; color: #8B8078; font-weight: 400; margin-top: 8px;">Break it down, scratch it out</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_timer(minutes, seconds, total_seconds, elapsed_seconds):
    """Render the timer display."""
    progress = elapsed_seconds / total_seconds if total_seconds > 0 else 0
    percent = int(progress * 100)
    
    st.markdown(f"""
    <div class="timer-display">{minutes:02d}:{seconds:02d}</div>
    """, unsafe_allow_html=True)
    
    # Custom HTML progress bar - green aesthetic
    st.markdown(f"""
    <div style="width: 100%; height: 14px; background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%); border-radius: 20px; overflow: hidden; margin: 15px 0; box-shadow: 0 3px 12px rgba(180, 140, 100, 0.12);">
        <div style="width: {percent}%; height: 100%; background: linear-gradient(90deg, #A8D5BA, #95C9A8, #82BD96); border-radius: 20px; transition: width 0.3s ease;"></div>
    </div>
    <p style="text-align: center; color: #8B8078; font-family: 'DM Mono', monospace; font-size: 0.9rem; font-weight: 400; margin-top: 10px;">
        {percent}% complete
    </p>
    """, unsafe_allow_html=True)


# PAGE: HOME - main landing page with new goal / history options

def page_home():
    """Home page with main menu."""
    # Check for unfinished session
    unfinished = st.session_state.storage.get_unfinished_session()
    render_quotes()
    st.write("")
    st.markdown("### What would you like to do?")
    st.write("")
    
    # All buttons stacked vertically with same width
    if st.button("🚀 Start a New Goal", use_container_width=True):
        if unfinished:
            st.session_state.page = "handle_existing"
        else:
            st.session_state.page = "new_goal"
        st.rerun()
    
    st.write("")
    
    if st.button("📜 View History", use_container_width=True):
        st.session_state.page = "history"
        st.rerun()
    
    if unfinished:
        st.write("")
        if st.button(f"📌 Unfinished Session: {unfinished.goal}", use_container_width=True, key="continue_unfinished"):
            st.session_state.current_session = unfinished
            st.session_state.page = "run_session"
            st.rerun()

    st.write("")

    if st.button("Main Menu", use_container_width=True):
        st.session_state.page = "full_home"
        st.rerun()


# PAGE: HANDLE EXISTING SESSION - resume or discard incomplete session

def page_handle_existing():
    """Handle existing session when starting new goal."""
    unfinished = st.session_state.storage.get_unfinished_session()
    
    if not unfinished:
        st.session_state.page = "new_goal"
        st.rerun()
        return
    
    st.markdown("### ⚠️ Existing Session Found")
    st.write("")
    
    st.warning(f"You have an existing session: **\"{unfinished.goal}\"**")
    st.write("Starting a new goal will delete this session.")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Delete and Start New", use_container_width=True):
            st.session_state.storage.delete_session(unfinished.session_id)
            st.session_state.page = "new_goal"
            st.rerun()
    
    with col2:
        if st.button("← Go Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()


# PAGE: NEW GOAL - user inputs goal and available time

def page_new_goal():
    """Create a new goal and get AI breakdown."""
    st.markdown("### 🎯 What do you want to accomplish?")
    st.write("")
    
    st.caption("💡 Tip: Be specific! e.g., 'Study Big-O Notation of discrete math' instead of 'study math'")
    
    goal = st.text_input("Your goal:", placeholder="Enter your goal here...")
    
    time_available = st.number_input(
        "How much time do you have? (minutes)",
        min_value=5,
        max_value=480,
        value=30,
        step=5
    )
    
    st.write("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back to Menu", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    
    with col2:
        if st.button("✨ Break It Down!", use_container_width=True, type="primary"):
            if not goal.strip():
                st.error("Please enter a goal first!")
                return
            
            # Validate goal with AI
            with st.spinner("Checking your goal..."):
                if not st.session_state.ai.validate_goal(goal):
                    st.error("I didn't understand that. Please describe your goal more clearly.")
                    return
            
            # Break down the goal
            with st.spinner("Breaking down your goal... 🤔"):
                tasks = st.session_state.ai.break_down_goal(goal, time_available)
            
            if not tasks:
                st.error("Sorry, I couldn't break down your goal. Please try again with a different description.")
                return
            
            # Create and save session
            session = Session(goal=goal, time_available=time_available, tasks=tasks)
            st.session_state.storage.save_session(session)
            st.session_state.current_session = session
            st.session_state.regenerate_count = 0
            st.session_state.page = "confirm_tasks"
            st.rerun()


# PAGE: CONFIRM TASKS - review AI-generated tasks before starting

def page_confirm_tasks():
    """Show tasks and let user confirm or adjust."""
    session = st.session_state.current_session
    
    if not session:
        st.session_state.page = "home"
        st.rerun()
        return
    
    st.markdown(f"### 📋 Your Plan for: {session.goal}")
    st.write("")
    
    # Calculate total time
    total_minutes = sum(task.timer_minutes for task in session.tasks)
    st.markdown(f"**Total time: {total_minutes} minutes**")
    st.write("")
    
    # Show all tasks
    for task in session.tasks:
        render_task_card(task)
    
    st.write("")
    st.markdown("---")
    
    # Regenerate info
    can_regenerate = st.session_state.regenerate_count < 3
    remaining = 3 - st.session_state.regenerate_count
    
    if can_regenerate:
        st.caption(f"🔄 You can regenerate up to 3 times. Remaining: {remaining}")
    else:
        st.caption("🔄 You've used all 3 regenerate attempts.")
    
    st.write("")
    
    # Action buttons
    st.markdown("### Are these tasks okay?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, let's start!", use_container_width=True, type="primary"):
            st.session_state.page = "run_session"
            st.rerun()
    
    with col2:
        if st.button("⏱️ Adjust Time", use_container_width=True):
            st.session_state.page = "adjust_time"
            st.rerun()
    
    if can_regenerate:
        st.write("")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if st.button("😅 Too Hard", use_container_width=True):
                regenerate_tasks("too_hard")
        
        with col4:
            if st.button("📝 Need More Detail", use_container_width=True):
                regenerate_tasks("not_enough")
        
        with col5:
            if st.button("🔍 Specify Topic", use_container_width=True):
                st.session_state.page = "different_focus"
                st.rerun()
    
    st.write("")
    if st.button("❌ Cancel Session", use_container_width=True):
        st.session_state.storage.delete_session(session.session_id)
        st.session_state.current_session = None
        st.session_state.page = "home"
        st.rerun()


def regenerate_tasks(adjust_type, focus=None):
    """Regenerate tasks with adjustment."""
    session = st.session_state.current_session
    
    if not session:
        st.error("No session found.")
        return
    
    with st.spinner("Regenerating tasks... 🔄"):
        tasks = st.session_state.ai.break_down_goal(
            session.goal,
            session.time_available,
            adjust=adjust_type,
            focus=focus
        )
    
    if tasks:
        session.tasks = tasks
        st.session_state.storage.save_session(session)
        st.session_state.regenerate_count += 1
        st.rerun()
    else:
        st.error("Sorry, I couldn't regenerate. Let's keep the current plan.")


# PAGE: ADJUST TIME - modify task time before starting

def page_adjust_time():
    """Let user adjust time for a specific task."""
    session = st.session_state.current_session
    
    if not session or not session.tasks:
        st.error("No tasks available to adjust.")
        if st.button("← Back"):
            st.session_state.page = "confirm_tasks"
            st.rerun()
        return
    
    st.markdown("### ⏱️ Adjust Task Time")
    st.write("")
    
    # Show tasks with selection
    task_options = {f"Task {t.task_number}: {t.description} ({t.timer_minutes} min)": t.task_number 
                    for t in session.tasks}
    
    selected = st.selectbox("Select a task to adjust:", list(task_options.keys()))
    task_num = task_options[selected]
    task = session.tasks[task_num - 1]
    
    new_time = st.number_input(
        f"New time for this task (current: {task.timer_minutes} min):",
        min_value=1,
        max_value=120,
        value=task.timer_minutes
    )
    
    st.write("")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "confirm_tasks"
            st.rerun()
    
    with col2:
        if st.button("💾 Save Changes", use_container_width=True, type="primary"):
            task.update_time(new_time)
            st.session_state.storage.save_session(session)
            st.session_state.page = "confirm_tasks"
            st.rerun()


# PAGE: DIFFERENT FOCUS - regenerate tasks with user feedback

def page_different_focus():
    """Let user specify different focus area."""
    session = st.session_state.current_session
    
    if not session:
        st.session_state.page = "home"
        st.rerun()
        return
    
    st.markdown("### 🔍 What topic would you like to focus on?")
    st.write("")
    st.caption(f"Current goal: **{session.goal}**")
    st.write("")
    
    # Use session state to persist focus input
    if "focus_input" not in st.session_state:
        st.session_state.focus_input = ""
    
    focus = st.text_input(
        "Specify the topic or area:",
        value=st.session_state.focus_input,
        placeholder="e.g., 'graphs', 'chapter 3', 'the introduction'",
        key="focus_text_input"
    )
    st.session_state.focus_input = focus
    
    st.write("")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.focus_input = ""
            st.session_state.page = "confirm_tasks"
            st.rerun()
    
    with col2:
        regenerate_clicked = st.button("🔄 Regenerate with Topic", use_container_width=True, type="primary")
    
    # Handle regeneration outside button context
    if regenerate_clicked:
        if not focus.strip():
            st.error("Please enter a topic to focus on.")
        else:
            with st.spinner("Regenerating tasks with new focus... 🔄"):
                tasks = st.session_state.ai.break_down_goal(
                    session.goal,
                    session.time_available,
                    adjust="different_focus",
                    focus=focus
                )
            
            if tasks:
                session.tasks = tasks
                st.session_state.storage.save_session(session)
                st.session_state.regenerate_count += 1
                st.session_state.focus_input = ""
                st.session_state.page = "confirm_tasks"
                st.rerun()
            else:
                st.error("Sorry, I couldn't regenerate. Please try a different topic.")


# PAGE: RUN SESSION - main timer page with task execution

def page_run_session():
    """Run through tasks with timer."""
    session = st.session_state.current_session
    
    if not session:
        st.session_state.page = "home"
        st.rerun()
        return
    
    task = session.get_current_task()
    
    # All tasks done!
    if task is None:
        complete_session()
        return
    
    # Show progress
    total_tasks = len(session.tasks)
    completed_tasks = sum(1 for t in session.tasks if t.status == "completed")
    
    st.markdown(f"### 📌 {session.goal}")
    
    # Overall task progress bar - light gray accent (different from timer)
    task_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    st.markdown(f"""
    <div style="width: 100%; height: 14px; background-color: #F5F5F5; border-radius: 10px; overflow: hidden; margin: 10px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.08); border: 1px solid rgba(0, 0, 0, 0.06);">
        <div style="width: {task_percent}%; height: 100%; background: linear-gradient(90deg, #B8B8B8, #A0A0A0, #909090); border-radius: 10px;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Use empty placeholder to ensure task list is completely cleared when timer runs
    task_list_placeholder = st.empty()
    
    # Show task list and current task details only when timer is NOT running
    if not st.session_state.timer_running:
        with task_list_placeholder.container():
            # Show all tasks list (like confirm_tasks page)
            st.markdown("### Tasks")
            st.write("")
            for t in session.tasks:
                is_current = (t.task_number == task.task_number)
                render_task_card(t, is_current=is_current)
            
            st.write("")
            st.markdown("---")
            st.write("")
            
            # Show current task details - focused view
            st.markdown(f"### ▶️ Task {task.task_number} of {total_tasks}: {task.description}")
            st.markdown(f"**Time: {task.timer_minutes} minutes**")
            st.write("")
            
            # Timer controls
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Start Timer", use_container_width=True, type="primary"):
                    st.session_state.timer_running = True
                    st.session_state.timer_paused = False
                    st.session_state.timer_seconds = task.timer_minutes * 60
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Skip Task", use_container_width=True):
                    task.skip()
                    session.next_task()
                    st.session_state.storage.save_session(session)
                    st.toast(get_encouragement("skipped"))
                    st.rerun()
    else:
        # Timer is running - clear the task list placeholder completely
        task_list_placeholder.empty()
        
        # Show current task information before timer starts
        st.markdown(f"### ▶️ Task {task.task_number} of {total_tasks}: {task.description}")
        st.markdown(f"**Time: {task.timer_minutes} minutes**")
        st.write("")
        
        run_timer(task)


def run_timer(task):
    """Run the countdown timer."""
    session = st.session_state.current_session
    total_seconds = task.timer_minutes * 60
    total_tasks = len(session.tasks)
    
    # Create placeholders
    task_info_placeholder = st.empty()
    timer_placeholder = st.empty()
    button_placeholder = st.empty()
    
    while st.session_state.timer_seconds > 0 and st.session_state.timer_running:
        if st.session_state.timer_paused:
            # Show paused state
            with timer_placeholder.container():
                mins = st.session_state.timer_seconds // 60
                secs = st.session_state.timer_seconds % 60
                elapsed = total_seconds - st.session_state.timer_seconds
                render_timer(mins, secs, total_seconds, elapsed)
                st.warning("⏸️ Timer Paused")
            
            with button_placeholder.container():
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("▶️ Resume", use_container_width=True, key="resume", type="primary"):
                        st.session_state.timer_paused = False
                        st.rerun()
                with col2:
                    if st.button("✅ I'm Done", use_container_width=True, key="done_paused"):
                        st.session_state.timer_running = False
                        st.session_state.page = "task_complete"
                        st.rerun()
                with col3:
                    if st.button("💾 Save & Exit", use_container_width=True, key="save_paused"):
                        session.pause()
                        st.session_state.storage.save_session(session)
                        st.session_state.current_session = None
                        st.session_state.timer_running = False
                        st.session_state.timer_paused = False
                        st.session_state.timer_seconds = 0
                        st.session_state.page = "home"
                        st.toast("Session saved! See you next time!")
                        st.rerun()
            return  # Exit the loop, wait for user interaction
        
        # Running timer
        mins = st.session_state.timer_seconds // 60
        secs = st.session_state.timer_seconds % 60
        elapsed = total_seconds - st.session_state.timer_seconds
        
        with timer_placeholder.container():
            render_timer(mins, secs, total_seconds, elapsed)
        
        with button_placeholder.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("💾 Save & Exit", use_container_width=True, key=f"save_{st.session_state.timer_seconds}"):
                    session.pause()
                    st.session_state.storage.save_session(session)
                    st.session_state.current_session = None
                    st.session_state.timer_running = False
                    st.session_state.timer_paused = False
                    st.session_state.timer_seconds = 0
                    st.session_state.page = "home"
                    st.toast("Session saved! See you next time!")
                    st.rerun()
            with col2:
                if st.button("⏸️ Pause", use_container_width=True, key=f"pause_{st.session_state.timer_seconds}"):
                    st.session_state.timer_paused = True
                    st.rerun()
            with col3:
                if st.button("✅ I'm Done", use_container_width=True, key=f"done_{st.session_state.timer_seconds}"):
                    st.session_state.timer_running = False
                    st.session_state.page = "task_complete"
                    st.rerun()
        
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()
    
    # Timer finished
    if st.session_state.timer_seconds <= 0:
        st.session_state.timer_running = False
        st.balloons()
        st.session_state.page = "task_complete"
        st.rerun()


# PAGE: TASK COMPLETE - shown when timer finishes for a task

def page_task_complete():
    """Handle task completion."""
    session = st.session_state.current_session
    
    if not session:
        st.session_state.page = "home"
        st.rerun()
        return
    
    task = session.get_current_task()
    
    if not task:
        st.session_state.page = "run_session"
        st.rerun()
        return
    
    # Nice completion banner - matches Task Coach style (white/frosted glass)
    # With celebration animation
    st.markdown("""
    <style>
        @keyframes celebrate-bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        @keyframes fade-in-up {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .celebration-icon {
            animation: celebrate-bounce 0.6s ease-in-out 3;
        }
        .celebration-text {
            animation: fade-in-up 0.5s ease-out;
        }
    </style>
    <div style="text-align: center; padding: 45px 35px; background: linear-gradient(135deg, #FFFEF8 0%, #FBF7F0 100%); border-radius: 28px; margin-bottom: 20px; box-shadow: 0 8px 35px rgba(180, 140, 100, 0.12);">
        <p class="celebration-icon" style="font-size: 3rem; margin: 0;">✨</p>
        <h2 class="celebration-text" style="color: #2D2A26 !important; margin: 15px 0 10px 0; font-size: 1.8rem; font-weight: 700;">Time's up!</h2>
        <p class="celebration-text" style="font-size: 1.05rem; color: #6B635A; margin: 0; font-weight: 400;">Great effort on this task!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Task:** {task.description}")
    st.write("")
    
    st.markdown("### How did it go?")
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Done!", use_container_width=True, type="primary"):
            task.complete()
            session.next_task()
            st.session_state.storage.save_session(session)
            st.toast(get_encouragement("completed"))
            st.session_state.page = "run_session"
            st.rerun()
    
    with col2:
        if st.button("⏰ Need More Time", use_container_width=True):
            st.session_state.page = "extend_time"
            st.rerun()
    
    with col3:
        if st.button("⏭️ Skip", use_container_width=True):
            task.skip()
            session.next_task()
            st.session_state.storage.save_session(session)
            st.toast(get_encouragement("skipped"))
            st.session_state.page = "run_session"
            st.rerun()


# PAGE: EXTEND TIME - add more time to current task

def page_extend_time():
    """Let user add more time to current task."""
    st.markdown("### ⏰ How many more minutes do you need?")
    st.write("")
    
    extra_minutes = st.number_input(
        "Additional minutes:",
        min_value=1,
        max_value=60,
        value=5
    )
    
    st.write("")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "task_complete"
            st.rerun()
    
    with col2:
        if st.button(f"▶️ Add {extra_minutes} Minutes", use_container_width=True, type="primary"):
            st.session_state.timer_seconds = extra_minutes * 60
            st.session_state.timer_running = True
            st.session_state.timer_paused = False
            # Update task timer to track total allocated time (persistent data)
            session = st.session_state.current_session
            if session:
                task = session.get_current_task()
                if task:
                    task.timer_minutes += extra_minutes
                    st.session_state.storage.save_session(session)
            st.session_state.page = "run_session"
            st.rerun()


# PAGE: HISTORY - view past completed sessions

def page_history():
    """Show completed sessions."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #1a3a36 !important;">Completed Goals</h2>
        <p style="color: #636e72; font-size: 0.95rem;">Every goal completed is a victory</p>
    </div>
    """, unsafe_allow_html=True)
    
    completed = st.session_state.storage.get_completed_sessions()
    
    if not completed:
        st.markdown("""
        <div class="task-card" style="text-align: center; padding: 40px;">
            <p style="font-size: 1.1rem; color: #636e72; margin: 0;">No completed goals yet</p>
            <p style="color: #5DCFAD; font-weight: 600; margin-top: 8px;">Start your first session!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for session in completed:
            st.markdown(f"""
            <div class="task-card task-card-completed">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 15px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.2rem; color: #5DCFAD;">✓</span>
                        <strong style="color: #1a3a36; font-size: 1rem;">{session.goal}</strong>
                    </div>
                    <span style="color: #636e72; font-size: 0.85rem; white-space: nowrap;">{session.created_at}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    if st.button("← Back", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()


# SESSION COMPLETE - celebration screen when all tasks done

def complete_session():
    """Complete the current session and show summary."""
    session = st.session_state.current_session
    session.complete()
    st.session_state.storage.save_session(session)
    
    # Show confetti celebration
    st.balloons()
    
    st.markdown("""
    <div class="celebration">
        <p style="font-size: 2.5rem; margin: 0 0 15px 0;">🌟</p>
        <h1 style="color: #2D2A26 !important; font-size: 2rem; font-weight: 700;">Session Complete!</h1>
        <p style="font-size: 1.05rem; color: #6B635A !important; margin-top: 12px; font-style: italic;">Amazing work showing up today</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown(f"### 📊 Session Summary")
    st.markdown(f"**Goal:** {session.goal}")
    st.write("")
    
    # Count stats
    completed = sum(1 for t in session.tasks if t.status == "completed")
    skipped = sum(1 for t in session.tasks if t.status == "skipped")
    total = len(session.tasks)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Completed", f"{completed}/{total}")
    with col2:
        st.metric("⏭️ Skipped", f"{skipped}/{total}")
    
    st.write("")
    st.markdown("### Tasks")
    for task in session.tasks:
        render_task_card(task)
    
    st.write("")
    if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
        st.session_state.current_session = None
        st.session_state.page = "home"
        st.rerun()


# MAIN APP - page router based on st.session_state.page

def main():
    """Main app entry point."""
    init_session_state()
    
    # Route to correct page
    page = st.session_state.page
    
    if page == "home":
        page_home()
    elif page == "handle_existing":
        page_handle_existing()
    elif page == "new_goal":
        page_new_goal()
    elif page == "confirm_tasks":
        page_confirm_tasks()
    elif page == "adjust_time":
        page_adjust_time()
    elif page == "different_focus":
        page_different_focus()
    elif page == "run_session":
        page_run_session()
    elif page == "task_complete":
        page_task_complete()
    elif page == "extend_time":
        page_extend_time()
    elif page == "history":
        page_history()
    else:
        page_home()


if __name__ == "__main__":
    main()
