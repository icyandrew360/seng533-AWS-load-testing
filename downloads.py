import time

def execute_and_time_commands(ssh, commands):
    total_time = 0
    total_size_mb = 0
    for desc, command in commands.items():
        print(f"Executing command: {desc}")
        start_time = time.time()
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        end_time = time.time()

        print(f"Time taken: {end_time - start_time:.2f} seconds\n")
        total_time += (end_time - start_time)
        total_size_mb += int(desc.split()[1][:-2])
    return total_time, total_size_mb

def time_and_download_files_from_s3_standard(ssh):
    download_files_commands = {
        "download 1mb file from standard storage": "aws s3 cp s3://seng533-standard-storage-group15/test-upload-1mb-agent1.file downloaded-1mb.file",
        "download 100mb file from standard storage": "aws s3 cp s3://seng533-standard-storage-group15/test-upload-10mb-agent1.file downloaded-10mb.file",
    }

    print("Timing of GET commands:")
    total_time, total_size_mb = execute_and_time_commands(ssh, download_files_commands)
    print("Downloads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["standard", total_time, total_size_mb, tput]

def time_and_download_files_from_s3_intelligent(ssh):
    download_files_commands = {
        "download 1mb file from intelligent tiering storage": "aws s3 cp s3://seng533-intelligent-tiering-group15/test-upload-1mb-agent1.file downloaded-1mb.file",
        "download 100mb file from intelligent tiering storage": "aws s3 cp s3://seng533-intelligent-tiering-group15/test-upload-10mb-agent1.file downloaded-10mb.file",
    }

    print("Timing of GET commands:")
    total_time, total_size_mb = execute_and_time_commands(ssh, download_files_commands)
    print("Downloads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["intelligent", total_time, total_size_mb, tput]

def time_and_download_files_from_s3_glacier_ir(ssh):
    download_files_commands = {
        "download 1mb file from glacier IR storage": "aws s3 cp s3://seng533-glacier-group15/test-upload-1mb-agent1.file downloaded-1mb.file",
        "download 100mb file from glacier IR storage": "aws s3 cp s3://seng533-glacier-group15/test-upload-10mb-agent1.file downloaded-10mb.file",
    }

    print("Timing of GET commands:")
    total_time, total_size_mb = execute_and_time_commands(ssh, download_files_commands)
    print("Downloads complete.")

    tput = total_size_mb / total_time
    print(f"total size: {total_size_mb} MB")
    print(f"total time: {total_time:.2f} seconds")
    print(f"total throughput: {tput:.2f} MB/s")
    return ["glacier_ir", total_time, total_size_mb, tput]