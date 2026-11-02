import random

print("====================================")
print("       PYTHON MINI PROJECT")
print("====================================")
print("1. Number Guessing Game")
print("2. Word Counter")
print("3. Exit")

while True:

    choice = input("\nEnter your choice (1-3): ")

    # NUMBER GUESSING GAME
    if choice == "1":

        print("\n===== NUMBER GUESSING GAME =====")

        while True:
            number = random.randint(1, 100)
            attempts = 0

            print("Guess a number between 1 and 100")

            while True:
                try:
                    guess = int(input("Enter your guess: "))
                    attempts += 1

                    if guess < number:
                        print("Too Low! Try Again.")

                    elif guess > number:
                        print("Too High! Try Again.")

                    else:
                        print("\nCongratulations! You won!")
                        print("Correct Number:", number)
                        print("Total Attempts:", attempts)
                        break

                except ValueError:
                    print("Please enter a valid number.")

            again = input("\nPlay Again? (yes/no): ").lower()

            if again != "yes":
                break

    # WORD COUNTER
    elif choice == "2":

        print("\n========== WORD COUNTER ==========")

        text = input("Enter your text: ")

        words = text.split()
        characters = len(text)
        no_spaces = len(text.replace(" ", ""))
        sentences = sum(text.count(x) for x in ".!?")
        lines = len(text.splitlines())

        print("\n========== RESULT ==========")
        print("Total Words:", len(words))
        print("Total Characters:", characters)
        print("Characters Without Spaces:", no_spaces)
        print("Total Sentences:", sentences)
        print("Total Lines:", lines)

    # EXIT
    elif choice == "3":
        print("\nThank you for using this program!")
        break

    else:
        print("Invalid Choice! Please select 1, 2 or 3.")