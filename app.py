import os
import ftplib
from dotenv import load_dotenv
from init_ import callHelpers

class AutoUpdater:
    def __init__(self):
        self.load_env_variables()

    def load_env_variables(self):
        load_dotenv()
        self.host = os.getenv('HOST')
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.local_dir = os.getenv('LOCAL_DIR')
        self.target_dir = os.getenv('TARGET_DIR')

    def connect_ftp(self):
        try:
            ftp = ftplib.FTP(self.host)
            ftp.login(self.username, self.password)
            print(f"Connected to FTP server {self.host}")
            return ftp
        except ftplib.Error as e:
            print(f"Failed to connect to FTP server: {e}")
            return None

    def list_files_ftp(self, ftp):
        print("Listing files in the current directory:")
        for file in ftp.nlst():
            print(file)

    def transfer_files(self, ftp):
        print("\n------- Transferring files -------\n")
        files_transferred = []

        local_files = os.listdir(self.local_dir)
        ftp_files = ftp.nlst()

        for local_file in local_files:
            if local_file in ftp_files:
                with open(os.path.join(self.local_dir, local_file), 'rb') as file:
                    ftp.storbinary(f"STOR {local_file}", file)
                files_transferred.append(local_file)
                print(f"Transferred {local_file}")

        print(f'\n{len(files_transferred)} files updated')
        for file in files_transferred:
            print(f"Transferred file: {file}")

    def change_and_transfer(self, ftp):
        current_ftp_dir = ftp.pwd()
        if current_ftp_dir != self.target_dir:
            print(f"Changing directory to {self.target_dir}")
            ftp.cwd(self.target_dir)
        
        print(f"You are now in directory {ftp.pwd()}")
        self.list_files_ftp(ftp)
        self.transfer_files(ftp)

    def update(self):
        ftp = self.connect_ftp()
        if ftp:
            self.change_and_transfer(ftp)
            ftp.quit()
            print("\nFiles transferred, ending the program")
        else:
            print("Failed to connect to FTP server")

if __name__ == "__main__":
    callHelpers()
    updater = AutoUpdater()
    updater.update()
