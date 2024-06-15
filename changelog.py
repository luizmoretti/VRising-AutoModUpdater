import os
import subprocess
import datetime

def get_git_log():
    try:
        # Captura o log do git com mensagens de commit formatadas
        log_output = subprocess.check_output(["git", "log", "--pretty=format:* %s (%h)"], text=True)
        return log_output
    except subprocess.CalledProcessError as e:
        print(f"Error capturing git log: {e}")
        return None

def write_changelog(log):
    changelog_file = "CHANGELOG.md"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"## Changelog - {timestamp}\n\n"

    try:
        with open(changelog_file, "a") as file:
            file.write(header)
            file.write(log)
            file.write("\n\n")
        print(f"Changelog updated successfully: {changelog_file}")
    except IOError as e:
        print(f"Error writing to changelog: {e}")

def main():
    log = get_git_log()
    if log:
        write_changelog(log)

if __name__ == "__main__":
    main()
