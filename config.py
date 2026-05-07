import os

TOKEN_API = os.getenv("TOKEN_API", "")
ID = os.getenv("ADMIN_ID", "")

if not TOKEN_API:
    raise RuntimeError("Set TOKEN_API environment variable before starting the bot.")
