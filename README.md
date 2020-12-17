# zabbix-cloudwatch
AWS CloudWatch integration for Zabbix 5.x.

Requires Python 3.7+

## Installation
### Preparations in AWS
You have two options here:
1. Create an IAM user in each account you want to monitor. Give it the required permissions, see **Covered services**
2. Create an IAM user in a **central account** and for each monitored account create a Role with the required permissions. This role needs to be assumable by the central account via a configured Trust Relationship e.g.:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::XXXXXXXXXXX:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```


### Preparations for your Zabbix node
- Clone this github repo or download the zip/tar.gz.
- Copy the contents of `externalscripts` into `/usr/lib/zabbix/externalscripts`
- [Install](http://boto3.readthedocs.io/en/latest/guide/quickstart.html) system-wide `boto3` package (`pip3 install boto3`)

### Configuration - Global
- Import `templates/cloudwatch_template.xml` into Zabbix

You can deal with your configuration in a few different ways:
1. Provide the AWS credentials of your IAM User and other configuration if required by writing to a configuration file in `~/.aws/` for the Zabbix user.
   
   Refer to the [Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.htm) for instructions on how to structure the configuration file.
2. Provide the AWS credentials to your EC2 instance / ECS Fargate task using an execution role.
3. Provide the AWS credentials via the environment variables of the `zabbix` user.

### Configuration - Host
- Create a host with `0.0.0.0` as interface and link it to the template. 
  Change the macros `AWS_ACCOUNT` and `AWS_REGION` to correspond to your case.
  
   | Macro       | Value     |
   |-------------|-----------|
   | **AWS_ACCOUNT** | `12345678`  |
   | **AWS_REGION**  | `eu-west-1` |

-  Enable/Disable all desired discovery rules/items/triggers, add new or modify existing ones.


## Covered services
The default template includes discovery and items for the following services:

| Service         | Discovery API Call           | AWS Managed Policy
| --------------- | ---------------------------- | ----------------------------------- |
| **EC2**         | `describe_instances()`       | `AmazonEC2ReadOnlyAccess`           |
| **CloudFront**  | `list_distributions()`       | `CloudFrontReadOnlyAccess`          |           
| **ElastiCache** | `describe_cache_clusters()`  | `AmazonElastiCacheReadOnlyAccess`   |
| **RDS**         | `describe_db_instances()`    | `AmazonRDSReadOnlyAccess`           |
| **ELB**         | `describe_load_balancers()`  | `ElasticLoadBalancingReadOnly`      |
| **EMR**         | `list_clusters()`            | `AmazonElastiCacheReadOnlyAccess`   |
| **ELBv2 (ALB)** | `describe_target_groups()`   | `ElasticLoadBalancingReadOnly`      |
| **S3**          | `list_buckets()`             | `AmazonS3ReadOnlyAccess`            |

Alternatively you can assign your user the AWS Managed Policy `ViewOnlyAccess` which allows `List*` and `Describe*` calls across all AWS Services.

## Todo:
- [ ] Create CloudFront template
- [ ] Create ElastiCache template
- [ ] Provide separate templates for using _without_ autodiscovery (Host per item)

## Credits
- [@wawastein](https://github.com/wawastein) for creating the initial module
- [@juhovan](https://github.com/juhovan) for Zabbix 5.x changes, various fixes and improvements, Lambda discovery  
- [@aruruka](https://github.com/aruruka) for ElastiCache Discovery
- [@Aeriqu](https://github.com/Aeriqu) for CloudFront Discovery
- [@diegosainz](https://github.com/diegosainz) for RDS Cluster support