"""
Author: Hyunjoo Shim (NUID: 002505607)
storage.py
Handles saving and loading session data to/from JSON file.

The JSON file is a dictionary
the key is session ID
the value is JSON representation of each session

Example:
    {
      "8ccacbf0-0ec4-49c2-8751-d7feb71af71c": {
          "session_id": "20251127_233611",
          "goal": "Write essay",
          "status": "in_progress",
          "current_task": 0,
          "created_at": "2025-11-27 23:36:11",
          "tasks": [
            {
              "task_number": 1,
              "description": "Open document",
              "timer_minutes": 5,
              "status": "pending"
            },
            {
              "task_number": 2,
              "description": "Write intro",
              "timer_minutes": 10,
              "status": "pending"
            }
          ]
        },
  "8b5659e0-76e4-46f8-8fd1-bd56063bdd3a": {...},
}
"""

import json
from session import Session
from task import Task

# Data: The entire file contents (all sessions)
# Session: One single task breakdown
# Path to the file where all sessions are stored

class Storage:
    def __init__(self, filename="data/sessions.json"):
        """
        Create storage handler.
        Saves/loads session data to/from a JSON file.

        :param filename: path to the JSON file
        """
        self.filename = filename
        self._initialize()


    def _initialize(self):
        """Create the data directory and file if they don't exist."""
        import os

        # Create parent directory if it doesn't exist
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        data = self._load_file()
        if data == {}:
            self._save_file({})


    def _save_file(self, data):
        """
        Save dictionary to JSON file.

        :param data: dictionary to save
        """
        with open(self.filename, "w") as file:
            json.dump(data, file)


    def _load_file(self):
        """
        Load dictionary from JSON file

        :return: dictionary or empty dict if file doesn't exist
        """
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:       # If file doesn't exist
            return {}
        except json.JSONDecodeError:    # If file is empty
            return {}


    def save_session(self, session):
        """
        Save a session (add new or update existing).

        :param session: Session object to save
        """
        data = self._load_file()                        # Load all existing data
        session_dict = session.to_dict()                # Convert Session object -> dictionary to save in JSON
        data[str(session.session_id)] = session_dict

        self._save_file(data)


    def get_session_by_id(self, session_id):
        """
        Find a specific session by ID.

        :param session_id: the ID to search for
        :return: Session object, or None if not found or invalid
        """
        data = self._load_file()

        session_id_str = str(session_id)                # Convert to string in case UUID is passed

        if session_id_str in data:
            session = self._dict_to_session(data[session_id_str])
            return session  # May be None if data is invalid

        return None


    def get_unfinished_session(self):
        """
        Get the first session that is not completed.
        paused: user did it
        in_progress: app closed unexpectedly

        :return: Session object, or None if no unfinished session
        """
        data = self._load_file()

        for session_id, session_dict in data.items():
            if session_dict.get("status") in ["paused", "in_progress"]:
                session = self._dict_to_session(session_dict)
                if session:  # Skip if None (invalid data)
                    return session

        return None

    def get_completed_sessions(self):
        """
        Get all completed sessions (history).

        :return: list of Session objects
        """
        data = self._load_file()
        completed = []

        for session_id, session_dict in data.items():
            if session_dict.get("status") == "completed":
                session = self._dict_to_session(session_dict)
                if session:  # Skip if None (invalid data)
                    completed.append(session)

        return completed


    def get_total_completed_count(self):
        """
        Get total number of completed sessions (all time).

        :return: count of all completed sessions
        """
        data = self._load_file()
        count = 0

        for session_id, session_dict in data.items():
            if session_dict.get("status") == "completed":
                count += 1

        return count


    def delete_session(self, session_id):
        """
        Delete a session by ID.

        :param session_id: the ID to delete
        """
        data = self._load_file()

        session_id_str = str(session_id)

        if session_id_str in data:
            del data[session_id_str]

        self._save_file(data)


    def _dict_to_session(self, session_dict):
        """
        Convert dictionary to Session object.

        :param session_dict: dictionary from JSON
        :return: Session object, or None if data is invalid
        """
        try:
            tasks = []
            for task_dict in session_dict.get("tasks", []):
                task = Task(
                    task_number=task_dict.get("task_number", 0),
                    description=task_dict.get("description", ""),
                    timer_minutes=task_dict.get("timer_minutes", 5),
                    status=task_dict.get("status", "pending")
                )
                tasks.append(task)

            return Session(
                goal=session_dict.get("goal", "Unknown"),
                time_available=session_dict.get("time_available", 60),
                status=session_dict.get("status", "in_progress"),
                tasks=tasks,
                current_task=session_dict.get("current_task", 0),
                session_id=session_dict.get("session_id"),
                created_at=session_dict.get("created_at")
            )
        except (KeyError, TypeError, ValueError):
            # Invalid data - return None to skip this session
            return None


if __name__ == "__main__":
    pass