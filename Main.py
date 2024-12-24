import subprocess


def run_server():
    try:
        subprocess.run(["python", "Server.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Server.py: {e}")


if __name__ == "__main__":
    run_server()
