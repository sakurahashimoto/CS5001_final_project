# Sakura Hashimoto(003186429)
import streamlit as st
import task_app
import quotes
import compliment_quotes
import ai_task_coach.streamlit_app as ai

TASKS_HOME = "tasks_home"
APP = "app"
ADD_TASK = "add_task"
COMPLETE_TASK = "complete_task"
REMOVE_TASK = "remove_task"


def setup():
    if "page" not in st.session_state:
        st.session_state.page = "full_home"
    if APP not in st.session_state:
        # From the task_app module, construct a TaskApp object instance.
        # Store the object instance in the session state dictionary inside
        # the st module.
        st.session_state[APP] = task_app.TaskApp("/tmp/cs5001_tasklist.json")
    ai.init_session_state()
    ai.set_style()


def home_page():
    app = st.session_state[APP]
    ai.render_quotes()
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        render_tasks()
    with col2:
        if st.button("Add Task", key="add_task", use_container_width=True):
            app.page = task_app.ADD_TASK_PAGE
            st.rerun()
        st.write("")
        if st.button("Complete A Task", key="complete_task", use_container_width=True):
            app.page = task_app.COMPLETE_TASK_PAGE
            st.rerun()
        st.write("")
        if st.button("Remove A Task", key="remove_task", use_container_width=True):
            app.page = task_app.REMOVE_TASK_PAGE
            st.rerun()
        st.write("")
        if st.button(
            "View Completed Tasks", key="view_completed_tasks", use_container_width=True
        ):
            app.page = task_app.VIEW_COMPLETED_TASKS_PAGE
            st.rerun()
        st.write("")
        if st.button("Reset", key="reset", use_container_width=True):
            app.full_reset()
            st.rerun()
        st.write("")
        if st.button("Main Menu", key="main_menu", use_container_width=True):
            app.page = task_app.HOME_PAGE
            st.session_state.page = "full_home"
            st.rerun()


def add_task_callback():
    app = st.session_state[APP]
    task = st.session_state[ADD_TASK]
    app.add_task(task)
    st.session_state[ADD_TASK] = ""


def render_tasks():
    app = st.session_state[APP]
    if len(app.data[task_app.TASK_LIST_KEY]) == 0:
        st.markdown("## You have no tasks, enter one to get started!")
    else:
        st.markdown("## Tasks:")
        for index, task in enumerate(app.data[task_app.TASK_LIST_KEY]):
            st.markdown(f"{index + 1}. {task}")


def add_task_page():
    app = st.session_state[APP]
    render_tasks()
    st.text_input("Enter your task", key=ADD_TASK, on_change=add_task_callback)
    if st.button("Back", key="add_task_back"):
        app.page = task_app.HOME_PAGE
        st.rerun()


def complete_task_callback():
    app = st.session_state[APP]
    task_number = st.session_state[COMPLETE_TASK]
    try:
        app.complete_task(task_number)
        st.toast(compliment_quotes.get_random_compliment_quote(), icon="🎉" )
        st.balloons()

    except Exception as e:
        st.toast(str(e))

    st.session_state[COMPLETE_TASK] = ""
   

def complete_task_page():
    app = st.session_state[APP]
    render_tasks()
    st.text_input(
        "Enter task number to mark as completed",
        key=COMPLETE_TASK,
        on_change=complete_task_callback,
    )
    if st.button("Back", key="complete_task_back"):
        app.page = task_app.HOME_PAGE
        st.rerun()


def remove_task_callback():
    app = st.session_state[APP]
    task_number = st.session_state[REMOVE_TASK]
    try:
        app.remove_task(task_number)
    except Exception as e:
        st.toast(str(e))

    st.session_state[REMOVE_TASK] = ""


def remove_task_page():
    app = st.session_state[APP]
    render_tasks()
    st.text_input(
        "Enter task number to remove", key=REMOVE_TASK, on_change=remove_task_callback
    )
    if st.button("Back", key="remove_task_back"):
        app.page = task_app.HOME_PAGE
        st.rerun()


def view_completed_tasks_page():
    app = st.session_state[APP]
    completed_tasks = app.data[task_app.COMPLETED_TASK_LIST_KEY]
    if len(completed_tasks) == 0:
        st.markdown("## You currently have no completed tasks")
    else:
        st.markdown(f"🎉 {compliment_quotes.get_random_compliment_quote()}")
        st.markdown("## Completed Tasks:")
        for index, task in enumerate(completed_tasks):
            st.markdown(f"{index + 1}. {task}")
    if st.button("Back", key="view_completed_tasks_back"):
        app.page = task_app.HOME_PAGE
        st.rerun()


def tasks_main():
    # Get the object instance from the session state dictionary
    app = st.session_state[APP]
    # Check if we should display the home page
    if app.page == task_app.HOME_PAGE:
        home_page()
    if app.page == task_app.ADD_TASK_PAGE:
        add_task_page()
    if app.page == task_app.COMPLETE_TASK_PAGE:
        complete_task_page()
    if app.page == task_app.REMOVE_TASK_PAGE:
        remove_task_page()
    if app.page == task_app.VIEW_COMPLETED_TASKS_PAGE:
        view_completed_tasks_page()

def home():
    ai.render_welcome()
    if st.button("🗺️ Strategic Planning (AI Coach)", key="goto_ai", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    st.write("")

    if st.button("✅ Quick Daily Tasks (Task Manager)", key="goto_tasks", use_container_width=True):
        st.session_state.page = TASKS_HOME
        st.rerun()

def main():
    setup()

    page = st.session_state.page
    if page == "full_home":
        home()
    if page in [
        "home",
        "handle_existing",
        "new_goal",
        "confirm_tasks",
        "adjust_time",
        "different_focus",
        "run_session",
        "task_complete",
        "extend_time",
        "history",
    ]:
        ai.main()
    if page == TASKS_HOME:
        tasks_main()


if __name__ == "__main__":
    main()
