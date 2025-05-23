import paramiko
import numpy as np
import pandas as pd
from uploads import *
from downloads import *
# EC2 instance details
EC2_HOST = "ec2-54-85-19-156.compute-1.amazonaws.com"
EC2_USER = "ec2-user"
PEM_FILE = "./EC2-far.pem"


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=EC2_HOST, username=EC2_USER, key_filename=PEM_FILE)
    print("Connected to EC2 instance")

    # generate_test_files_for_upload(ssh)
    s3_standard_upload_data = time_and_upload_files_to_s3_standard(ssh)
    s3_intelligent_upload_data = time_and_upload_files_to_s3_intelligent(ssh)
    s3_glacier_upload_data = time_and_upload_files_to_s3_glacier(ssh)

    upload_data = np.array([
        ["storage type", "total time (s)", "total size (MB)", "total tput (MB/s)"],
        s3_standard_upload_data, 
        s3_intelligent_upload_data, 
        s3_glacier_upload_data
    ])
    
    s3_standard_download_data = time_and_download_files_from_s3_standard(ssh)
    s3_intelligent_download_data = time_and_download_files_from_s3_intelligent(ssh)
    s3_glacier_download_data = time_and_download_files_from_s3_glacier_ir(ssh)

    download_data = np.array([
        ["storage type", "total time (s)", "total size (MB)", "total tput (MB/s)"],
        s3_standard_download_data, 
        s3_intelligent_download_data, 
        s3_glacier_download_data
    ])

    print("Importing the following upload_data to CSV: ")
    print(upload_data)
    print("Importing the following download_data to CSV: ")
    print(download_data)

    upload_df = pd.DataFrame(upload_data)
    upload_df.to_csv("upload_data.csv", index=False)

    download_df = pd.DataFrame(download_data)
    download_df.to_csv("download_data.csv", index=False)
    ssh.close()

if __name__ == "__main__":
    main()