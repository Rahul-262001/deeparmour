import boto3
import sys
import time
import io



aws_access_key_id = <AWS_ACCESS_KEY_ID>
aws_secret_access_key = <AWS_SECRET_ACCESS_KEY>
region_name = <region>

s3_client=boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
rds_client = boto3.client('rds', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

def s3_bucket_check():
    print("Checking S3 Buckets...\n")
    # check for publicly accessible S3 buckets
    try:
        buckets = s3_client.list_buckets()  # List all buckets
        for bucket in buckets["Buckets"]:    
            bucket_name = bucket["Name"]
            print(f"Checking bucket: {bucket_name}")
            block_public_access = s3_client.get_bucket_policy_status(Bucket=bucket_name) # Check if the bucket has public access blocked
            if block_public_access['PolicyStatus']['IsPublic'] == True:  # Check if the bucket has public access blocked
                print(f"1.Bucket {bucket_name} is publicly accessible.")
            else:
                print(f"1.Bucket {bucket_name} is NOT publicly accessible.")

            logging_response = s3_client.get_bucket_logging(Bucket=bucket_name) # Check if the bucket has logging enabled
            if not logging_response.get('LoggingEnabled'):
                print(f"2.Bucket with logging disabled")
            else:
                print(f"2.Bucket with logging enabled")

            versioning_response = s3_client.get_bucket_versioning(Bucket=bucket_name) # Check if the bucket has versioning enabled
            if versioning_response.get('Status') != 'Enabled':
                print(f"3.Bucket with versioning disabled")
            else:
                print(f"3.Bucket with versioning enabled")

    except Exception as e:
        print("Error occurred: ", e)

def check_rds_instances():
    print("Checking RDS instances...\n")

    try:
       
        instances = rds_client.describe_db_instances()
        
        for instance in instances['DBInstances']:
            print("Checking RDS instance: ",instance['DBInstanceIdentifier'])
            db_instance_id = instance['DBInstanceIdentifier']
            backup_retention = instance['BackupRetentionPeriod']
            delete_protection = instance['DeletionProtection']
            publicly_accessible = instance['PubliclyAccessible']  # Public access information
            
            # Check if the instance is publicly accessible
            if publicly_accessible:
                print("1.RDS instance is publicly accessible")
            else:
                print("1.RDS instance is NOT publicly accessible")
            
            # Check if the instance has backups disabled
            if backup_retention == 0:
                print(f"2.RDS instance has backup disabled")
            else:
                print(f"2.RDS instance has backup enabled")
            
            # Check if the instance has no delete protection
            if not delete_protection:
                print(f"3.RDS instance has no delete protection")
            else:
                print(f"3.RDS instance has delete protection enabled")
            

    except Exception as e:
        print(f"Error checking RDS instances: {e}")


def check_security_groups():
    print("Checking security groups...\n")
    try:
        # Fetch all security groups
        security_groups = ec2_client.describe_security_groups()
        
        for sg in security_groups['SecurityGroups']:
            sg_name = sg['GroupName']
            
            # Print the header for the security group
            print(f"Checking security group named: {sg_name}")
            
            # Flags to track whether public access is allowed for specific ports
            ssh_public_access = False
            mysql_public_access = False
            mongo_public_access = False
            
            # Check each permission (IP rule) in the security group
            for ip_permission in sg['IpPermissions']:
                from_port = ip_permission.get('FromPort')
                ip_ranges = ip_permission.get('IpRanges', [])
                
                # Check for public access (CidrIp = 0.0.0.0/0)
                for ip_range in ip_ranges:
                    if ip_range.get('CidrIp') == '0.0.0.0/0':  # Publicly accessible
                        if from_port == 22:  # SSH port
                            ssh_public_access = True
                        elif from_port == 3306:  # MySQL port
                            mysql_public_access = True
                        elif from_port == 27017: # Mongodb port
                            mongo_public_access = True
            
            # Output for SSH access
            if ssh_public_access:
                print(f"1. Security Group: {sg_name} ALLOWS public SSH access.")
            else:
                print(f"1. Security Group: {sg_name} DOES NOT allow public SSH access.")
            
            if mongo_public_access:
                print(f"2. Security Group: {sg_name} ALLOWS public Mongodb access.")
            else:
                print(f"2. Security Group: {sg_name} DOES NOT allow public Mongodb access.")

            # Output for MySQL access
            if mysql_public_access:
                print(f"3. Security Group: {sg_name} ALLOWS public MySQL access.")
            else:
                print(f"3. Security Group: {sg_name} DOES NOT allow public MySQL access.")
            
            print()  
    except Exception as e:
        print(f"Error checking security groups: {e}")



output_buffer = io.StringIO()
original_stdout = sys.stdout
sys.stdout = output_buffer
print("Timestamp", end=": ")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("AWS Security Misconfiguration Report")
s3_bucket_check()
check_rds_instances()
check_security_groups()

sys.stdout = original_stdout
print(output_buffer.getvalue())
with open('aws_vulnerability_report.txt', 'w') as file:
    file.write(output_buffer.getvalue())

output_buffer.close()

print("Report saved as 'aws_vulnerability_report.txt'")

# print()
# s3_bucket_check()
# print()
# check_rds_instances()
# print()
# check_security_groups()
# print()

# with open('aws_vulnerability_report.txt', 'w') as file:

#     sys.stdout = file
#     print("Timestamp",end=": ")
#     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     print("AWS Security Misconfiguration Report")
#     s3_bucket_check()
#     check_rds_instances()
#     check_security_groups()
#     sys.stdout = sys.__stdout__

# print("Report saved as 'aws_vulnerability_report.txt'")