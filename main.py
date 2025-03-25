import paramiko
import time
import numpy as np
import pandas as pd

# EC2 instance details
EC2_HOST = "ec2-54-85-19-156.compute-1.amazonaws.com"
EC2_USER = "ec2-user"
PEM_FILE = "./EC2-far.pem"


def generate_test_files_for_upload(ssh):
    generate_files_commands = {
        "create 1mb file": "dd if=/dev/urandom of=test-1mb.file bs=1M count=1",
        "create 100mb file": "dd if=/dev/urandom of=test-10mb.file bs=1M count=10",
    }
    
    for desc, command in generate_files_commands.items():
        print(f"Executing command: {desc}")
        start_time = time.time()
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        end_time = time.time()

        print(f"Time taken; {end_time - start_time:.2f} seconds\n")

def execute_and_time_commands(ssh, commands):
    total_time = 0
    total_size_mb = 0
    for desc, command in commands.items():
        print(f"Executing command: {desc}")
        start_time = time.time()
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        end_time = time.time()

        print(f"Time taken; {end_time - start_time:.2f} seconds\n")
        total_time += (end_time - start_time)
        total_size_mb += int(desc.split()[1][:-2])
    return total_time, total_size_mb

def time_and_upload_files_to_s3_standard(ssh):
    upload_files_commands = {
        "upload 1mb file to standard storage": "aws s3 cp test-1mb.file s3://seng533-standard-storage-group15/test-upload-1mb-agent1.file",
        "upload 100mb file to standard storage": "aws s3 cp test-10mb.file s3://seng533-standard-storage-group15/test-upload-10mb-agent1.file",
    }

    print("Timing of PUT commands:")
    total_time, total_size_mb = execute_and_time_commands(ssh, upload_files_commands)
    print("Uploads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["standard", total_time, total_size_mb, tput]

def time_and_upload_files_to_s3_intelligent(ssh):
    upload_files_commands = {
        "upload 1mb file to intelligent tiering storage": "aws s3 cp test-1mb.file s3://seng533-intelligent-tiering-group15/test-upload-1mb-agent1.file --storage-class INTELLIGENT_TIERING",
        "upload 100mb file to intelligent tiering storage": "aws s3 cp test-10mb.file s3://seng533-intelligent-tiering-group15/test-upload-10mb-agent1.file --storage-class INTELLIGENT_TIERING",
    }

    print("Timing of PUT commands:")

    total_time, total_size_mb = execute_and_time_commands(ssh, upload_files_commands)
    print("Uploads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["intelligent", total_time, total_size_mb, tput]

def time_and_upload_files_to_s3_glacier(ssh):
    upload_files_commands = {
        "upload 1mb file to glacier storage": "aws s3 cp test-1mb.file s3://seng533-glacier-group15/test-upload-1mb-agent1.file --storage-class GLACIER",
        "upload 100mb file to glacier storage": "aws s3 cp test-10mb.file s3://seng533-glacier-group15/test-upload-10mb-agent1.file --storage-class GLACIER",
    }

    print("Timing of PUT commands:")

    total_time, total_size_mb = execute_and_time_commands(ssh, upload_files_commands)
    print("Uploads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["glacier", total_time, total_size_mb, tput]

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=EC2_HOST, username=EC2_USER, key_filename=PEM_FILE)
    print("Connected to EC2 instance")

    # generate_test_files_for_upload(ssh)
    s3_standard_upload_data = time_and_upload_files_to_s3_standard(ssh)
    s3_intelligent_upload_data = time_and_upload_files_to_s3_intelligent(ssh)
    s3_glacier_upload_data = time_and_upload_files_to_s3_glacier(ssh)

    data = np.array([
        ["storage type", "total time", "total size", "total tput"],
        s3_standard_upload_data, 
        s3_intelligent_upload_data, 
        s3_glacier_upload_data
    ])
    
    print("Importing the following data to CSV: ")
    print(data)

    df = pd.DataFrame(data)
    df.to_csv("upload_data.csv", index=False)
    ssh.close()

if __name__ == "__main__":
    main()