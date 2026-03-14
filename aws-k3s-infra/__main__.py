import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    tags={
        "Name": "my-vpc",
    })

pulumi.export("vpcId", vpc.id)

# Create a public subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet",
    })

pulumi.export("publicSubnetId", public_subnet.id)

# Create an Internet Gateway
igw = aws.ec2.InternetGateway("internet-gateway",
    vpc_id=vpc.id,
    tags={
        "Name": "igw",
    })

pulumi.export("igwId", igw.id)

# Create a route table
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    tags={
        "Name": "rt-public",
    })

pulumi.export("publicRouteTableId", public_route_table.id)

# Create a route in the route table for the Internet Gateway
route = aws.ec2.Route("igw-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=igw.id)

# Associate the route table with the public subnet
route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id)

# Create a security group for the public instance
public_security_group = aws.ec2.SecurityGroup("public-secgrp",
    vpc_id=vpc.id,
    description="Enable HTTP and SSH access for public instance",
    ingress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]},
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]},
    ])

# Use the specified Ubuntu 24.04 LTS AMI
ami_id = "ami-060e277c0d4cce553"

# Create nginx instance
nginx_instance = aws.ec2.Instance("nginx-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={
        "Name": "nginx-lb",
    })

pulumi.export("publicInstanceId", nginx_instance.id)
pulumi.export("publicInstanceIp", nginx_instance.public_ip)

# Create master instance
master_instance = aws.ec2.Instance("master-instance",
    instance_type="t3.small",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={
        "Name": "master",
    })

pulumi.export("masterInstanceId", master_instance.id)
pulumi.export("masterInstanceIp", master_instance.public_ip)

# Create worker1 instance
worker1_instance = aws.ec2.Instance("worker1-instance",
    instance_type="t3.small",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={
        "Name": "worker1",
    })

pulumi.export("worker1InstanceId", worker1_instance.id)
pulumi.export("worker1InstanceIp", worker1_instance.public_ip)

# Create worker2 instance
worker2_instance = aws.ec2.Instance("worker2-instance",
    instance_type="t3.small",
    vpc_security_group_ids=[public_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet.id,
    key_name="MyKeyPair",
    associate_public_ip_address=True,
    tags={
        "Name": "worker2",
    })

pulumi.export("worker2InstanceId", worker2_instance.id)
pulumi.export("worker2InstanceIp", worker2_instance.public_ip)
