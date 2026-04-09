import sys

def main():
    # Your inference logic here
    # For example:
    task_name = "example_task"
    
    # STEP 1: Print START block
    print(f"[START] task={task_name}", flush=True)
    
    # STEP 2: Do your processing
    # ... your model inference code ...
    result = 0.5  # example reward
    
    # STEP 3: Print STEP block
    print(f"[STEP] step=1 reward={result}", flush=True)
    
    # STEP 4: Print END block with final score
    final_score = 0.95  # calculate your actual score
    steps_taken = 1
    
    print(f"[END] task={task_name} score={final_score} steps={steps_taken}", flush=True)

if __name__ == "__main__":
    main()
