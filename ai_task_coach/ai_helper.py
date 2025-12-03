"""
ai_helper.py
Connects to Gemini AI to break down a goal into small tasks.
"""

import google.generativeai as genai
from config import GEMINI_API_KEY
from task import Task


class AIHelper:
    def __init__(self, model=None):
        """
        Set up connection to Gemini AI with injectable model.

        :param model: AI model instance for testing (default: Gemini)
        """
        if model is None:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.model = model


    def validate_goal(self, goal):
        """
        Check if the goal is meaningful and actionable.

        :param goal: the user's input
        :return: True if valid goal, False if gibberish/unclear
        """
        prompt = f"""
        Is the following a clear, actionable goal or task that someone might want to accomplish?
        
        Input: "{goal}"
        
        Reply with only "YES" if it's a meaningful goal (like "write an essay", "clean my room", "study for exam").
        Reply with only "NO" if it's gibberish, random characters, single letters, or doesn't make sense as a task.
        """

        response = self._call_ai(prompt)
        if response and "YES" in response.upper():
            return True
        return False


    def break_down_goal(self, goal, time_available, adjust=None, focus=None, retries=3):
        """
        Break down a goal (big task) into small tasks.

        :param goal: the big goal from user
        :param time_available: how many minutes user has right now
        :param adjust: adjustment type ("too_hard", "not_enough", "different_focus", or None)
        :param focus: specific focus area when adjust="different_focus"
        :param retries: number of attempts
        :return: list of Task objects, or None if all retries fail
        """

        for attempt in range(retries):
            prompt = self._build_prompt(goal, time_available, adjust, focus)
            response_text = self._call_ai(prompt)

            if response_text is None:
                continue

            tasks = self._parse_response(response_text)

            if len(tasks) == 0:
                continue

            return tasks

        return None


    def _build_prompt(self, goal, time_available, adjust=None, focus=None):
        """
        Build the prompt based on goal and adjustment.

        :param goal: the user's goal
        :param time_available: how many minutes user has right now
        :param adjust: adjustment type ("too_hard", "not_enough", "different_focus", or None)
        :param focus: specific focus area when adjust="different_focus"
        :return: prompt string
        """
        prompt = f"""
        You are a productivity coach specializing in helping people who struggle with procrastination.
        Your goal is to make overwhelming tasks feel manageable and achievable.
        The user should feel confident and pressure-free when they see your breakdown.
    
        The user has been procrastinating on this task: {goal}
        The user only has {time_available} minutes right now.
        Make sure all tasks combined fit within {time_available} minutes.
        Scope the goal appropriately - focus on what can realistically be accomplished in this time.

        Break it down into up to 5 small, actionable steps that directly accomplish the task.
        Do not provide only planning or preparation steps. Focus on the actual execution.
        
        Follow these guidelines:
        - The first step must be extremely simple and require almost no thinking
        - Each step should take no more than 40 minutes
        - Use clear, specific action verbs (e.g., "Write," "Open," "List")
        - Avoid vague language like "think about" or "consider"
    
        For each step, provide:
        - description: a clear, specific action
        - timer_minutes: realistic time estimate to complete the step
    
        Respond in this exact format only:
        [step number] | [description] | [timer_minutes]
        """

        if adjust == "too_hard":
            prompt += """
            Important: Make the steps extra simple.
            Break each action into the smallest possible piece.
            Each step should feel effortless and take no more than 15 minutes.
            """
        elif adjust == "not_enough":
            prompt += """
            Important: Provide more comprehensive steps.
            Cover the entire task from start to finish.
            Make sure the user can actually complete the task by following all the steps.
            """
        elif adjust == "different_focus" and focus:
            prompt += f"""
            Important: The user wants to focus specifically on: {focus}
            Adjust the task breakdown to concentrate on this specific area.
            Make sure all steps are related to this focus area.
            """

        return prompt


    def _call_ai(self, prompt):
        """
        Send prompt to Gemini and get response.

        :param prompt: the prompt string to send
        :return: response text, or None if something goes wrong
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return None


    def _parse_response(self, response_text):
        """
        Parse AI response into a list of Task objects.

        :param response_text: raw text from AI
        :return: list of Task objects, or empty list if parsing fails
        """
        tasks = []
        lines = response_text.strip().split("\n")

        for line in lines:
            if "|" in line:
                parts = line.split("|")

                if len(parts) != 3:
                    return []

                try:
                    task_number = int(parts[0].strip())
                except ValueError:
                    return []

                description = parts[1].strip()

                try:
                    minutes = int(parts[2].strip())
                except ValueError:
                    return []

                tasks.append(Task(
                    task_number=task_number,
                    description=description,
                    timer_minutes=minutes
                ))

        return tasks


if __name__ == "__main__":
    pass