"""
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

        :param filename: path to the JSON file
        """
        self.filename = filename
        self._initialize()


    def _initialize(self):
        """Create the file if it doesn't exist"""
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
        :return: Session object, or None if not found
        """
        data = self._load_file()

        session_id_str = str(session_id)                # Convert to string in case UUID is passed

        if session_id_str in data:
            return self._dict_to_session(data[session_id_str])

        return None


    def get_unfinished_session(self):
        """
        Get all sessions that are not completed.
        paused: user did it
        in_progress: app closed unexpectedly

        :return: list of Session objects
        """
        data = self._load_file()

        for session_id, session_dict in data.items():
            if session_dict["status"] in ["paused", "in_progress"]:
                return self._dict_to_session(session_dict)

        return None

    def get_completed_sessions(self):
        """
        Get all completed sessions (history).

        :return: list of Session objects
        """
        data = self._load_file()
        completed = []

        for session_id, session_dict in data.items():
            if session_dict["status"] == "completed":
                completed.append(self._dict_to_session(session_dict))

        return completed


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
        :return: Session object
        """
        tasks = []
        for task_dict in session_dict["tasks"]:
            task = Task(
                task_number=task_dict["task_number"],
                description=task_dict["description"],
                timer_minutes=task_dict["timer_minutes"],
                status=task_dict["status"]
            )
            tasks.append(task)

        return Session(goal=session_dict["goal"], status=session_dict["status"], tasks=tasks,
                       current_task=session_dict["current_task"])


if __name__ == "__main__":
    pass