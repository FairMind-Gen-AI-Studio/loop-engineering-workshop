"""Shared set-up for the DISC-1 checks: import the shop from the repository root."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
