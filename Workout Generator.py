import random
import json
import datetime 
class WorkoutGenerator:

    def __init__(self):
        """
        Initializes the generator with the exercise bank, sets the file path, 
        and loads the user database from the file.
        """
        self.exercise_bank = {
            'push': [
                'Bench Press', 'Overhead Press', 'Incline Dumbbell Press',
                'Tricep Pushdown', 'Lateral Raises', 'Chest Dips'
            ],
            'pull': [
                'Pull-Ups', 'Bent Over Rows', 'Lat Pulldowns',
                'Bicep Curls', 'Face Pulls', 'Seated Cable Rows'
            ],
            'legs': [
                'Squats', 'Deadlifts (RDL)', 'Leg Press',
                'Leg Curls', 'Calf Raises', 'Lunges'
            ],
            'cardio': [
                'Burpees', 'Jumping Jacks', 'High Knees',
                'Mountain Climbers', 'Jump Squats', 'Lunge Jumps'
            ]
        }
        
        self.DATABASE_FILE = "workout_users.json"
        
        self.user_database = self.load_database() 
        self.current_user_id = None
        
    def load_database(self):
        """
        Loads the user database from the JSON file on startup.
        """
        try:
            with open(self.DATABASE_FILE, 'r') as file: 
                data = json.load(file)
                result = {}
                for k, v in data.items():
                    try:
                        ik = int(k)
                    except (ValueError, TypeError):
                        ik = k
                    result[ik] = v
                return result
        except FileNotFoundError:
            print("Starting fresh database: No user file found.")
            return {}
        except json.JSONDecodeError:
            print("Error reading user database file. Starting fresh.")
            return {}

    def save_database(self):
        """
        Saves the current user database to the JSON file before program exit.
        """
        data_to_save = {str(k): v for k, v in self.user_database.items()}
        try:
            with open(self.DATABASE_FILE, 'w') as file: 
                json.dump(data_to_save, file, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save database: {e}")

    def register_user(self):
        """
        Prompts user for profile details and creates a new ID.
        """
        print("\n--- NEW USER REGISTRATION ---")
        
        name = input("Enter your name: ").strip()
        
        while True:
            try:
                age = int(input("Enter your age (years): "))
                weight = float(input("Enter your weight (lbs/kg): "))
                height = float(input("Enter your height (inches/cm): "))
                break 
            except ValueError:
                print("Error: Age, weight, and height must be valid numbers. Try again.")

        user_id = random.randint(1000, 9999) 
        while user_id in self.user_database:
            user_id = random.randint(1000, 9999)

        user_data = {
            'name': name,
            'age': age,
            'weight': weight,
            'height': height,
            'history': [] 
        }
        
        self.user_database[user_id] = user_data
        
        print(f"\nWelcome, {name}! Your unique ID is: {user_id}")
        print("Please remember this ID for future use.")
        
        return user_id

    def display_workout_history(self):
        """
        Reviews and prints the current user's past workout history.
        """
        if self.current_user_id not in self.user_database:
            print("No user found. Please register or enter a valid ID.")
            return

        history = self.user_database.get(self.current_user_id, {}).get('history', [])

        if history:
            print("\n--- Your Last Workouts ---")
            for i, item in enumerate(history[-5:], 1): 
                print(f"{i}. {item}")
            print("---------------------------")
        else:
            print("No workout history found yet. Let's create your first one!")

    def run_menu(self):
        print("---  Welcome to the Workout Generator!  ---")
        
        while self.current_user_id is None:
            initial_choice = input("Do you have an ID number? (y/n/quit): ").lower().strip()
            
            if initial_choice == 'quit':
                self.save_database() 
                print("Goodbye!")
                return 
            
            elif initial_choice == 'y':
                id_input = input("Enter your ID: ").strip() 
                try:
                    user_id = int(id_input) 
                    if user_id in self.user_database:
                        self.current_user_id = user_id
                        print(f"\nWelcome back, **{self.user_database[user_id]['name']}**!")
                        self.display_workout_history() 
                    else:
                        print("Error: ID not found. Please try again or register.")
                except ValueError:
                    print("Error: ID must be a number.")
            
            elif initial_choice == 'n':
                self.current_user_id = self.register_user() 
            
            else:
                print("Invalid choice. Please enter 'y', 'n', or 'quit'.")
        
        while True:
            print("\nWhat do you want to train?")
            print("Options: 'push', 'pull', 'legs', 'cardio', or 'quit'")
            
            choice = input("> ").lower().strip()

            if choice == 'quit':
                self.save_database() 
                print("Hope you enjoyed your workout, see you next time! ⭐")
                break 
            
            if choice in self.exercise_bank:
                try:
                    print(f"Selected '{choice}'. What's your experience level?")
                    print(" (1 for Beginner, 2 for Intermediate, 3 for Advanced)")
                    level_input = input("> ").strip()
                    
                    level = int(level_input) 

                    if level in [1, 2, 3]:
                        self.generate_workout(choice, level)
                    else:
                        print("Error: Please enter 1, 2, or 3 for the level.")
                        
                except ValueError:
                    print(f"Error: '{level_input}' is not a valid number. Please enter 1, 2, or 3.")
            
            else:
                print(f"Error: '{choice}' is not a valid option. Please try again.")

    def generate_workout(self, group, level):
        print(f"\n...Generating a Lvl {level} {group} workout...")
        
        exercises_list = self.exercise_bank[group]
        num_exercises = 4 
        selected_exercises = random.sample(exercises_list, num_exercises)
        
        now = datetime.datetime.now()
        
        timestamp = now.strftime("%Y-%m-%d %H:%M") 
        
        history_entry = f"[{timestamp}] Lvl {level} {group} workout: {', '.join(selected_exercises)}"
        
        if self.current_user_id is not None:
            self.user_database[self.current_user_id]['history'].append(history_entry)
            
        print("--- Here is your workout: ---")
        
        if group == 'cardio':
            sets = 4 
            seconds_on = 20 + (level * 10) 
            seconds_off = 30
            
            for i, exercise in enumerate(selected_exercises, start=1):
                print(f"{i}. {exercise}: {sets} sets of {seconds_on}s on, {seconds_off}s off.")
        
        else: 
            sets = 3
            reps = 8 + (level * 2) 
            
            for i, exercise in enumerate(selected_exercises, start=1):
                print(f"{i}. {exercise}: {sets} sets of {reps} reps.")
                
        print("-----------------------------------------------")


def main():
    """
    The main entry point for the program.
    """
    my_workout = WorkoutGenerator()
    my_workout.run_menu()

if __name__ == "__main__":
    main()