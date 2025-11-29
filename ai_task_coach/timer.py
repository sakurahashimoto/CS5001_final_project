"""
timer.py
Countdown timer for each task.
"""
import threading
import time

from google.ai.generativelanguage_v1beta.services.permission_service.transports.rest import PermissionServiceRestStub


# TODO Add pause()
class Timer:
    def __init__(self):
        """Create a timer."""
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False     # Flag to track if timer is active (False = not running)
        self.stopped_early = False  # If user stops timer early


    def start(self, minutes):
        """
        Start countdown timer.

        :param minutes: how many minutes to count down
        :return: "completed" if timer finished, "stopped" if user stopped early
        """
        self.total_seconds = minutes * 60           # Convert min to sec
        self.remaining_seconds = self.total_seconds
        self.is_running = True
        self.stopped_early = False

        print()
        print("    Press ENTER to finish early")
        print()

        # Start a thread to listen for Enter key
        input_thread = threading.Thread(target=self._wait_for_input)
        input_thread.daemon = True
        input_thread.start()

        # Keep running as long as time is left and timer is still running
        # Each loop = 1 second passing in real life
        while self.remaining_seconds > 0 and self.is_running:
            self._display_time()
            time.sleep(1)
            self.remaining_seconds -= 1

        if self.stopped_early:
            self._stopped_message()
            return "stopped"
        else:
            self._time_up()
            return "completed"


    def _wait_for_input(self):
        """Wait for user to press Enter."""
        input()
        self.is_running = False
        self.stopped_early = True


    def _display_time(self):
        """Show the remaining time."""
        mins = int(self.remaining_seconds // 60)
        secs = int(self.remaining_seconds % 60)

        # Calculate progress
        elapsed = self.total_seconds - self.remaining_seconds
        progress = elapsed / self.total_seconds
        percent = int((elapsed / self.total_seconds) * 100)

        # Build progress bar
        # "█" * 5 =     "█████"
        # "░" * 15 =    "░░░░░░░░░░░░░░░"
        # Combined:     "█████░░░░░░░░░░░░░░░"
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"\r  {bar} {percent}% complete | Time left: {mins:02d}:{secs:02d}", end="")  # Overwriting


    def _time_up(self):
        """Notify user when timer is done."""
        bar = "█" * 20
        print(f"\r  {bar} 100% complete | Time left: 00:00")
        print()
        print("⏰ Time's up! ⏰")


    def _stopped_message(self):
        """Notify user they stopped early."""
        print()
        print()
        print("⏹️ Timer stopped!")


if __name__ == "__main__":
    pass