"""
Author: Critical Functions Test Suite
Tests the most important functions across all modules for core functionality.
"""
import pytest
import sys
import os
import json
import tempfile
import uuid
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task import Task
from session import Session
from storage import Storage
from ai_helper import AIHelper


class TestCriticalFunctions:
    """Test suite for critical functions across all modules."""
    
    # From task.py
    
    def test_task_complete(self):
        """Critical: Task.complete() - Mark task as completed."""
        task = Task(1, "Study math", 30, status="pending")
        task.complete()
        assert task.status == "completed"
    
    def test_task_to_dict(self):
        """Critical: Task.to_dict() - Serialize task for persistence."""
        task = Task(2, "Write essay", 45, status="completed")
        result = task.to_dict()
        
        assert result == {
            "task_number": 2,
            "description": "Write essay",
            "timer_minutes": 45,
            "status": "completed"
        }
        # Verify it can be JSON serialized
        assert json.dumps(result) is not None
    
    # From session.py
    
    def test_session_get_current_task(self):
        """Critical: Session.get_current_task() - Get active task."""
        tasks = [
            Task(1, "Task 1", 10),
            Task(2, "Task 2", 20)
        ]
        session = Session("Study math", 60, tasks=tasks, current_task=0)
        
        current = session.get_current_task()
        assert current is not None
        assert current.task_number == 1
        assert current.description == "Task 1"
    
    def test_session_next_task(self):
        """Critical: Session.next_task() - Advance to next task."""
        tasks = [
            Task(1, "Task 1", 10),
            Task(2, "Task 2", 20),
            Task(3, "Task 3", 15)
        ]
        session = Session("Study math", 60, tasks=tasks, current_task=0)
        
        # Move to next task
        session.next_task()
        assert session.current_task == 1
        
        current = session.get_current_task()
        assert current.task_number == 2
        
        # Move to last task
        session.next_task()
        assert session.current_task == 2
        
        # Move past last task - should complete session
        session.next_task()
        assert session.current_task == 3
        assert session.status == "completed"
    
    def test_session_to_dict(self):
        """Critical: Session.to_dict() - Serialize session for persistence."""
        session_id = uuid.uuid4()
        created_at = "2025-01-15 10:30:00"
        tasks = [
            Task(1, "Task 1", 10, status="completed"),
            Task(2, "Task 2", 20, status="pending")
        ]
        session = Session(
            "Study math",
            60,
            status="in_progress",
            tasks=tasks,
            current_task=1,
            session_id=session_id,
            created_at=created_at
        )
        
        result = session.to_dict()
        
        assert result["session_id"] == str(session_id)
        assert result["goal"] == "Study math"
        assert result["time_available"] == 60
        assert result["status"] == "in_progress"
        assert result["current_task"] == 1
        assert result["created_at"] == created_at
        assert len(result["tasks"]) == 2
        # Verify task data is correctly serialized
        assert result["tasks"][0]["task_number"] == 1
        assert result["tasks"][0]["description"] == "Task 1"
        assert result["tasks"][0]["status"] == "completed"
        assert result["tasks"][1]["task_number"] == 2
        assert result["tasks"][1]["status"] == "pending"
        # Verify it can be JSON serialized
        assert json.dumps(result) is not None
    
    def test_session_complete(self):
        """Critical: Session.complete() - Mark session as completed."""
        session = Session("Study math", 60, status="in_progress")
        session.complete()
        assert session.status == "completed"
    
    # From storage.py
    
    def test_storage_save_session(self):
        """Critical: Storage.save_session() - Persist session to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            storage = Storage(filename=temp_filename)
            task = Task(1, "Test task", 10)
            session = Session("Test goal", 60, tasks=[task])
            
            storage.save_session(session)
            
            # Verify file was written and contains session
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            assert str(session.session_id) in data
            assert data[str(session.session_id)]["goal"] == "Test goal"
            assert len(data[str(session.session_id)]["tasks"]) == 1
        finally:
            os.unlink(temp_filename)
    
    def test_storage_get_session_by_id(self):
        """Critical: Storage.get_session_by_id() - Retrieve session from storage."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            storage = Storage(filename=temp_filename)
            
            # Save a session
            tasks = [Task(1, "Task 1", 10), Task(2, "Task 2", 20)]
            session = Session("Study math", 60, tasks=tasks)
            storage.save_session(session)
            
            # Retrieve it
            retrieved = storage.get_session_by_id(session.session_id)
            
            assert retrieved is not None
            assert retrieved.goal == "Study math"
            assert len(retrieved.tasks) == 2
            assert retrieved.tasks[0].description == "Task 1"
            assert retrieved.tasks[1].description == "Task 2"
        finally:
            os.unlink(temp_filename)
    
    def test_storage_get_unfinished_session(self):
        """Critical: Storage.get_unfinished_session() - Find paused/in-progress sessions."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            storage = Storage(filename=temp_filename)
            
            # Create paused session
            paused_session = Session("Paused goal", 60, status="paused")
            storage.save_session(paused_session)
            
            # Create completed session
            completed_session = Session("Completed goal", 60, status="completed")
            storage.save_session(completed_session)
            
            # Should return paused session
            unfinished = storage.get_unfinished_session()
            assert unfinished is not None
            assert unfinished.goal == "Paused goal"
            assert unfinished.status == "paused"
        finally:
            os.unlink(temp_filename)
    
    def test_storage_dict_to_session(self):
        """Critical: Storage._dict_to_session() - Deserialize session from JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_filename = f.name
        
        try:
            storage = Storage(filename=temp_filename)
            
            # Create session dict (as it would appear in JSON)
            session_dict = {
                "session_id": str(uuid.uuid4()),
                "goal": "Test goal",
                "time_available": 60,
                "status": "in_progress",
                "current_task": 0,
                "created_at": "2025-01-15 10:30:00",
                "tasks": [
                    {
                        "task_number": 1,
                        "description": "Task 1",
                        "timer_minutes": 10,
                        "status": "pending"
                    },
                    {
                        "task_number": 2,
                        "description": "Task 2",
                        "timer_minutes": 20,
                        "status": "completed"
                    }
                ]
            }
            
            # Convert to Session object
            session = storage._dict_to_session(session_dict)
            
            assert session.goal == "Test goal"
            assert session.time_available == 60
            assert session.status == "in_progress"
            assert session.current_task == 0
            assert len(session.tasks) == 2
            assert session.tasks[0].task_number == 1
            assert session.tasks[0].description == "Task 1"
            assert session.tasks[0].status == "pending"
            assert session.tasks[1].task_number == 2
            assert session.tasks[1].description == "Task 2"
            assert session.tasks[1].status == "completed"
        finally:
            os.unlink(temp_filename)
    
    # From ai_helper.py
    
    def test_ai_helper_parse_response(self):
        """Critical: AIHelper._parse_response() - Parse AI response into tasks."""
        mock_model = Mock()
        helper = AIHelper(model=mock_model)
        
        # Valid AI response format
        response_text = "1 | Open textbook | 5\n2 | Read chapter 1 | 15\n3 | Take notes | 10"
        tasks = helper._parse_response(response_text)
        
        assert len(tasks) == 3
        assert tasks[0].task_number == 1
        assert tasks[0].description == "Open textbook"
        assert tasks[0].timer_minutes == 5
        assert tasks[1].task_number == 2
        assert tasks[1].description == "Read chapter 1"
        assert tasks[1].timer_minutes == 15
        assert tasks[2].task_number == 3
        assert tasks[2].description == "Take notes"
        assert tasks[2].timer_minutes == 10
    
    def test_ai_helper_validate_goal(self):
        """Critical: AIHelper.validate_goal() - Validate user input."""
        mock_model = Mock()
        
        # Test valid goal
        mock_response_valid = Mock()
        mock_response_valid.text = "YES"
        mock_model.generate_content.return_value = mock_response_valid
        
        helper = AIHelper(model=mock_model)
        result = helper.validate_goal("Study discrete math")
        
        assert result is True
        mock_model.generate_content.assert_called_once()
        
        # Test invalid goal
        mock_response_invalid = Mock()
        mock_response_invalid.text = "NO"
        mock_model.generate_content.return_value = mock_response_invalid
        
        result = helper.validate_goal("x")
        assert result is False
        assert mock_model.generate_content.call_count == 2
