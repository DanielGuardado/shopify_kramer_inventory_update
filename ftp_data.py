import pandas as pd
from ftplib import FTP
import io


class FTPDataLoader:
    def __init__(self, config):
        self.host = config["host"]
        self.username = config["username"]
        self.password = config["password"]
        self.file_path = config["file_path"]
        self.port = config.get("port", 21)  # Use default port 21 if not provided

    def get_ftp_file_as_dataframe(self):
        """
        Connect to the FTP server, retrieve the file, and store it in memory as a pandas DataFrame.

        Returns:
        - DataFrame: Pandas DataFrame containing the CSV data.
        """
        with FTP() as ftp:
            # Connect to the server
            ftp.connect(host=self.host, port=self.port)
            ftp.login(user=self.username, passwd=self.password)

            # Create an in-memory bytes stream
            buffer = io.BytesIO()

            # Retrieve the file and write it to the buffer
            ftp.retrbinary(f"RETR {self.file_path}", buffer.write)

            # Reset buffer's position
            buffer.seek(0)

            # Read CSV from buffer into DataFrame
            df = pd.read_csv(buffer)

        return df
