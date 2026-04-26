# test_nvidia.py
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("NVIDIA_API_KEY")
print(f"Key loaded: {key[:10]}...")  # prints first 10 chars only