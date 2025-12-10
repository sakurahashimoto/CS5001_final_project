"""
Author: Hyunjoo Shim (NUID: 002505607)
config.py
Central place for all settings (like API keys).
Other files import from here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
