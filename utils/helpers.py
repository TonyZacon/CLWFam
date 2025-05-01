from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_USER_IDS = os.getenv("ADMIN_USER_IDS", "").split(",")

group_settings = {}
active_users = set()
inactive_users = set()

def is_admin(user_id):
    return str(user_id) in ADMIN_USER_IDS
