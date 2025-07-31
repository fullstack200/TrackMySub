import os

def clear_screen_with_banner():
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows: cls, Unix/Linux/Mac: clear
    print("=" * 50)
    print("             Welcome to TrackMySubs!")
    print("      Your Subscription Tracker, Simplified       ")
    print("=" * 50)
