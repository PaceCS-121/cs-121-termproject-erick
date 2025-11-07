import random

class WorkoutGenerator:
    """
    Holds all the logic and data for generating a workout.
    """
    def __init__(self):
        """
        Initializes the generator with the exercise bank.
        """
        self.exercise_bank = {
            'push': [
                'Bench Press',
                'Overhead Press',
                'Incline Dumbbell Press',
                'Tricep Pushdown',
                'Lateral Raises',
                'Chest Dips'
            ],
            'pull': [
                'Pull-Ups',
                'Bent Over Rows',
                'Lat Pulldowns',
                'Bicep Curls',
                'Face Pulls',
                'Seated Cable Rows'
            ],
            'legs': [
                'Squats',
                'Deadlifts (RDL)',
                'Leg Press',
                'Leg Curls',
                'Calf Raises',
                'Lunges'
            ],
            'cardio': [
                'Burpees',
                'Jumping Jacks',
                'High Knees',
                'Mountain Climbers',
                'Jump Squats',
                'Lunge Jumps'
            ]
        }
        
    def run_menu(self):
        """
        Runs the main menu loop to get user input.
        """
        print("---  Welcome to the Workout Generator!  ---")

        while True:
            print("\nWhat do you want to train?")
            print("Options: 'push', 'pull', 'legs', 'cardio', or 'quit'")
            
            choice = input("> ").lower().strip()

            if choice == 'quit':
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
        """
        Generates and prints a random workout based on user's choice.
        Handles different logic for cardio vs. strength.
        """
        print(f"\n...Generating a Lvl {level} {group} workout...")
        
        exercises_list = self.exercise_bank[group]
        
        num_exercises = 4 
        
        selected_exercises = random.sample(exercises_list, num_exercises)
        
        print("--- Here is your workout: ---")
        
        if group == 'cardio':
            rounds = 4
            seconds_on = 20 + (level * 10) 
            seconds_off = 30
            
            
            for i, exercise in enumerate(selected_exercises, start=1):
                print(f"{i}. {exercise}: {rounds} rounds of {seconds_on}s on, {seconds_off}s off.")
        
        else:
            
            sets = 3
            reps = 8 + (level * 2) 
            
            
            for i, exercise in enumerate(selected_exercises, start=1):
                print(f"{i}. {exercise}: {sets} sets of {reps} reps.")
                
        print("-----------------------------------------------")
        


if __name__ == "__main__":
    
    my_workout = WorkoutGenerator()
    
    
    my_workout.run_menu()
    
