"""
timer.py
Countdown timer for each task.
"""
import time
import sys
import select


class Timer:
    def __init__(self):
        """Create a timer."""
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False
        self.is_paused = False
        self.stopped_early = False


    def start(self, minutes):
        """
        Start countdown timer.
        
        How it works:
        1. Main loop runs every second, updating the progress bar
        2. Uses non-blocking input check (select) to detect ENTER key
        3. If user presses ENTER, shows pause menu
        4. Loop ends when time runs out OR user chooses 'done'

        :param minutes: how many minutes to count down
        :return: "completed" if timer finished, "stopped" if user stopped early
        """
        self.total_seconds = minutes * 60
        self.remaining_seconds = self.total_seconds
        self.is_running = True
        self.is_paused = False
        self.stopped_early = False

        print()
        print("    Press ENTER to pause or finish early")
        print()

        # Main loop: check for input, display time, wait 1 second, repeat
        while self.remaining_seconds > 0 and self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue

            # Check for input (non-blocking)
            if self._check_for_input():
                self._handle_pause()

            if not self.is_running:
                break

            self._display_time()
            time.sleep(1)
            self.remaining_seconds -= 1

        self.is_running = False

        if self.stopped_early:
            self._stopped_message()
            return "stopped"
        else:
            self._time_up()
            return "completed"


    def _check_for_input(self):
        """
        Check if user pressed Enter (non-blocking).

        :return: True if input detected, False otherwise
        """
        try:
            # Unix/macOS: use select for non-blocking check
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.readline()
                return True
        except (ValueError, OSError, TypeError):
            pass
        return False


    def _handle_pause(self):
        """Handle pause menu."""
        self.is_paused = True
        print()
        print()
        print("  ⏸️  Paused!")

        while True:
            print("  Type 'resume' to continue, or 'done' to finish: ", end="", flush=True)
            choice = input().strip().lower()

            if choice == "done":
                self.is_running = False
                self.stopped_early = True
                return
            elif choice == "resume":
                self.is_paused = False
                print("\r  ▶️  Resumed! Press ENTER to pause" + " " * 25)
                return
            else:
                print("  Invalid input. Please type 'resume' or 'done'.")


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
        self._play_alert_sound()
        print("⏰ Time's up! ⏰")


    def _play_alert_sound(self):
        """Play alert sound when timer finishes."""
        import platform
        import os

        system = platform.system()

        try:
            if system == "Darwin":  # macOS
                os.system('afplay /System/Library/Sounds/Glass.aiff &')
            elif system == "Windows":
                import winsound
                winsound.MessageBeep()
            else:  # Linux
                print("\a")  # Terminal bell
        except Exception:
            print("\a")  # Fallback to terminal bell


    def _stopped_message(self):
        """Notify user they stopped early."""
        print()
        print()
        print("⏹️ Timer stopped!")


if __name__ == "__main__":
    pass