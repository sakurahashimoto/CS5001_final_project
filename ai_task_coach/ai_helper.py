"""
ai_helper.py
Connects to Gemini AI to break down a goal into small tasks.
"""

import google.generativeai as genai
from config import GEMINI_API_KEY
from task import Task


class AIHelper:
    def __init__(self):
        """Set up connection to Gemini AI."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")


    def break_down_goal(self, goal, adjust=None, retries=3):
        """
        Break down a goal (big task) into small tasks.

        :param goal: the big goal from user
        :param adjust: adjustment type ("too_hard", "not_enough", "different", or None)
        :param retries: number of attempts
        :return: list of Task objects, or None if all retries fail
        """

        for attempt in range(retries):
            prompt = self._build_prompt(goal, adjust)
            response_text = self._call_ai(prompt)

            if response_text is None:
                continue

            tasks = self._parse_response(response_text)

            if len(tasks) == 0:
                continue

            return tasks

        return None


    def _build_prompt(self, goal, adjust=None):
        """
        Build the prompt based on goal and adjustment.

        :param goal: the user's goal
        :param adjust: adjustment type ("too_hard", "not_enough", "different", or None)
        :return: prompt string
        """
        prompt = f"""
        You are a productivity coach specializing in helping people who struggle with procrastination.
        Your goal is to make overwhelming tasks feel manageable and achievable.
        The user should feel confident and pressure-free when they see your breakdown.
    
        The user has been procrastinating on this task: {goal}
    
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
        elif adjust == "different":
            prompt += """
            Instead of the standard way, suggest shortcuts, tools, or workarounds.
            Suggest a fresh, creative way to tackle this task.
            Start from a different angle or use a different method.
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