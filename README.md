# seng533-AWS-load-testing

ensure you restrict permissions of this key file with this command
chmod 400 "EC2-far.pem"

ssh -i "EC2-far.pem" ec2-user@ec2-54-85-19-156.compute-1.amazonaws.com

# creating test files
dd if=/dev/urandom of=test-1mb.file bs=1M count=1

# upload test files
aws s3 cp test-1mb.file s3://seng533-standard-storage-group15/test-upload-1mb-agent1.file

# download test files
aws s3 cp s3://seng533-standard-storage-group15/test-upload-1mb-agent1.file downloaded-1mb.file