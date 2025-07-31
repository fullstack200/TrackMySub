import time
import os
from auth.SignIn import SignIn

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome_screen():
    clear_screen()
    print("=" * 50)
    print("Welcome to TrackMySubs!".center(50))
    print("Your Subscription Tracker, Simplified".center(50))
    print("=" * 50)
    time.sleep(2) 

def main():
    welcome_screen()

    while True:
        print("\n📋 Main Menu")
        print("1. Existing user? Sign In")
        print("2. New here? Sign Up")
        print("0. Exit")

        choice = input("Enter your option number: ").strip()

        if choice not in ['1', '2', '0']:
            print("\n❌ Invalid input. Please enter 1, 2, or 0.\n")
            continue

        if choice == '1':
            signin = SignIn()
            signin.handle()
            
        elif choice == '2':
            print("\n📝 Sign Up selected.\n")
            # SignUp().handle()
            
        elif choice == '0':
            print("\n👋 Exiting application. Goodbye!")
            break


if __name__ == "__main__":
    main()