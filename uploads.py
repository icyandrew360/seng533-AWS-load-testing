import time

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
        "upload 1mb file to glacier IR storage": "aws s3 cp test-1mb.file s3://seng533-glacier-group15/test-upload-1mb-agent1.file --storage-class GLACIER_IR",
        "upload 100mb file to glacier IR storage": "aws s3 cp test-10mb.file s3://seng533-glacier-group15/test-upload-10mb-agent1.file --storage-class GLACIER_IR",
    }

    print("Timing of PUT commands (Glacier IR):")

    total_time, total_size_mb = execute_and_time_commands(ssh, upload_files_commands)
    print("Uploads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["glacier_ir", total_time, total_size_mb, tput]
