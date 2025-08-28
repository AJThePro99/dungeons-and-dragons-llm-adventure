from components.orchestrator import Orchestrator

def main():
    try:
        orchestrator = Orchestrator()
        orchestrator.start_game()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    main()