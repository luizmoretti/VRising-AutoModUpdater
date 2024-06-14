### VRising AutoModUpdater

**An Automatic Application for Updating Mods on VRising Servers Using FTP**

### Overview

VRising AutoModUpdater is a Python application that automates the process of updating mods on VRising servers via FTP. It periodically checks mod repositories for updates and, if any are found, automatically downloads and installs the updated mods on the server. This ensures that your mods are always up-to-date, providing the best experience for players.

### Requirements

To use VRising AutoModUpdater, you will need the following:

* Python 3.11 or higher
* pip
* FTP server

### Installation

1. Clone the VRising AutoModUpdater repository from GitHub:

    ```bash
    
    git clone https://github.com/luizmoretti/VRising-AutoModUpdater.git
    
    ```

2. Navigate to the VRising-AutoModUpdater directory:

    ```bash
    cd VRising-AutoModUpdater
    ```

3. Install the application's dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure the `.env` file with your FTP information:

    ```
    FTP_HOST= your ftp host
    FTP_USERNAME= your ftp username
    FTP_PASSWORD= your ftp password
    LOCAL_DIR= your local directory
    TARGET_DIR= your target directory
    ```

5. Run the application:

    ```bash
    python app.py
    ```

### Usage

VRising AutoModUpdater will periodically check mod repositories for updates. If it finds any, it will automatically download and install the updated mods on the server. You can configure the update check interval in the `.env` file.

### Example .env File

```
FTP_HOST=example.com
FTP_USERNAME=username
FTP_PASSWORD=password
LOCAL_DIR=your_local_directory
TARGET_DIR=your_target_directory
```

### Contributing

If you would like to contribute to VRising AutoModUpdater, feel free to fork the repository and submit pull requests.

### Support

If you have any questions or issues with VRising AutoModUpdater, please open an issue on the GitHub repository.

### License

VRising AutoModUpdater is licensed under the MIT License.