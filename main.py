import paramiko
import time

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

def time_and_upload_files_to_s3(ssh):
    upload_files_commands = {
        "upload 1mb file to standard storage": "aws s3 cp test-1mb.file s3://seng533-standard-storage-group15/test-upload-1mb-agent1.file",
        "upload 100mb file to standard storage": "aws s3 cp test-10mb.file s3://seng533-standard-storage-group15/test-upload-10mb-agent1.file",
    }

    print("Timing of PUT commands:")

    total_time = 0
    total_size_mb = 0
    for desc, command in upload_files_commands.items():
        print(f"Executing command: {desc}")
        start_time = time.time()
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        end_time = time.time()

        print(f"Time taken; {end_time - start_time:.2f} seconds\n")
        total_time += (end_time - start_time)
        total_size_mb += int(desc.split()[1][:-2])
    print("Uploads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=EC2_HOST, username=EC2_USER, key_filename=PEM_FILE)
    print("Connected to EC2 instance")

    generate_test_files_for_upload(ssh)

    time_and_upload_files_to_s3(ssh)

    ssh.close()

if __name__ == "__main__":
    main()