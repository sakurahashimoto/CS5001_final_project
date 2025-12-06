import pytest 
import task_app
import os

#py test gives this parameter for test tmp_path which does not affect to 
#codes
def test_create_if_empty(tmp_path):
   #when we make an object called app that takes constractor parametor file_name
   #we are testing create if empty from the task_app.py
   file_name = tmp_path.joinpath("data.json")
   app = task_app.TaskApp(file_name)
   assert os.path.exists(file_name) == True

def test_load_data(tmp_path):
   file_name = tmp_path.joinpath("data.json")
   app = task_app.TaskApp(file_name)
   assert task_app.TASK_LIST_KEY in app.data
   assert task_app.COMPLETED_TASK_LIST_KEY in app.data

def test_add_task(tmp_path, monkeypatch):
   task = "Do my homework"
   # Patch input so that it simulates a user entering "do my homework"
   monkeypatch.setattr("builtins.input", lambda _ : task)

   file_name = tmp_path.joinpath("data.json")
   app = task_app.TaskApp(file_name)
   app.add_task()
   # assert that data contains the task
   assert task in app.data[task_app.TASK_LIST_KEY]

def test_remove_task(tmp_path, monkeypatch):
   task = "Do homework1"
   # Patch input so that it simulates a user entering "do my homework"
   monkeypatch.setattr("builtins.input", lambda _ : task)
   file_name = tmp_path.joinpath("data.json")
   app = task_app.TaskApp(file_name)
   app.add_task()
   assert task in app.data[task_app.TASK_LIST_KEY]

   monkeypatch.setattr("builtins.input", lambda _ : "1")
   app.remove_task()
   assert len(app.data[task_app.TASK_LIST_KEY]) == 0

def test_completed_task(tmp_path, monkeypatch):
   task = "Eat breakfast"
   monkeypatch.setattr("builtins.input", lambda _ : task)
   file_name = tmp_path.joinpath("data.json")
   app = task_app.TaskApp(file_name)
   app.add_task()

   monkeypatch.setattr("builtins.input", lambda _ : "1")
   app.complete_task()
   assert len(app.data[task_app.TASK_LIST_KEY]) == 0
   assert len(app.data[task_app.COMPLETED_TASK_LIST_KEY]) == 1

def full_reset(tmp_path, monkeypatch):
    task = "Clean the house"
    monkeypatch.setattr("builtins.input", lambda _ : task)
    # call function save_list that takes TASK_LIST_FILE, and give empty list so reset
    file_name = tmp_path.joinpath("data.json")
    app = task_app.TaskApp(file_name)
    app.add_task()
    assert len(app.data) == 1
    app.full_reset()
    assert len(app.data) == 0
   














if __name__ == "__main__":
   pytest.main()