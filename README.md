# AWS Security Misconfiguration Checker

This project is designed to check for common security misconfigurations in AWS services such as S3, RDS, and EC2 security groups. The script uses the `boto3` AWS SDK to interact with AWS services and generate a report of potential vulnerabilities in your AWS environment.

## Features

- **S3 Bucket Check**:
  - Verifies if S3 buckets are publicly accessible.
  - Checks if bucket logging is enabled.
  - Verifies if versioning is enabled on S3 buckets.

- **RDS Instance Check**:
  - Checks if RDS instances are publicly accessible.
  - Verifies if backups are enabled.
  - Checks if deletion protection is enabled on RDS instances.

- **EC2 Security Group Check**:
  - Scans security groups to see if any allow public access for SSH (port 22), MySQL (port 3306), or MongoDB (port 27017).

- **Timestamped Report**:
  - Generates a timestamped report and saves it as `aws_vulnerability_report.txt`.

## Requirements

- Python 3.x
- `boto3` library: Install via `pip install boto3`
- AWS credentials (access key and secret key)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Rahul-262001/deeparmour
   ```

2. Install the required dependencies:
   ```bash
   pip install boto3
   ```

3. Set up your AWS credentials (Access Key ID and Secret Access Key) in the script or via environment variables.

## Usage

1. Run the script to check your AWS environment for potential misconfigurations:
   ```bash
   python aws_security_check.py
   ```

2. The script will generate a security report and save it as `aws_vulnerability_report.txt` in the current directory.

3. Review the generated report for vulnerabilities and take necessary actions to improve your AWS security.

## Example Output

```plaintext
Timestamp: 2024-12-20 18:16:43
AWS Security Misconfiguration Report
Checking S3 Buckets...

Checking bucket: test-bucket-deeparmour
1.Bucket test-bucket-deeparmour is publicly accessible.
2.Bucket with logging disabled
3.Bucket with versioning disabled
Checking RDS instances...

Checking RDS instance:  test-deeparmour-db
1.RDS instance is publicly accessible
2.RDS instance has backup disabled
3.RDS instance has no delete protection
Checking security groups...

Checking security group named: test-deeparmour-sec
1. Security Group: test-deeparmour-sec ALLOWS public SSH access.
2. Security Group: test-deeparmour-sec ALLOWS public Mongodb access.
3. Security Group: test-deeparmour-sec ALLOWS public MySQL access.

Checking security group named: default
1. Security Group: default DOES NOT allow public SSH access.
2. Security Group: default DOES NOT allow public Mongodb access.
3. Security Group: default DOES NOT allow public MySQL access.

```

## Script Explanation

This Python script interacts with the AWS SDK `boto3` to perform security checks on AWS resources:

1. **S3 Bucket Check**: 
   - Verifies if S3 buckets are publicly accessible by checking the bucket's public access settings.
   - Checks if logging is enabled for the bucket.
   - Verifies if versioning is enabled to keep track of object changes.

2. **RDS Instance Check**: 
   - Checks if the RDS instance is publicly accessible by reviewing the instance's access settings.
   - Verifies if the RDS instance has backups enabled by reviewing the backup retention period.
   - Checks if the instance has delete protection enabled, preventing accidental deletion.

3. **EC2 Security Group Check**:
   - Reviews EC2 security groups for open access to certain ports (SSH, MySQL, MongoDB).
   - Identifies which security groups allow unrestricted access (`0.0.0.0/0`) to sensitive services.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
