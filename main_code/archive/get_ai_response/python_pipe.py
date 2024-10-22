import os

fifo_path = "/tmp/python_pipe"

# Open the named pipe
with open(fifo_path, 'r') as fifo:
    while True:
        # Read a command from the pipe
        command = fifo.readline().strip()
        if command == "exit":
            break
        try:
            # Execute the command
            exec(command)
        except Exception as e:
            print(f"Error executing command: {e}")
