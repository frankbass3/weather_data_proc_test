provider "aws" {
  region = "us-east-1"  # Specify your AWS region here
}

# Create a security group for the EC2 instance
resource "aws_security_group" "allow_ports" {
  name_prefix = "allow_ports"
  description = "Allow SSH, HTTP, and PostgreSQL inbound traffic"

  # Allow inbound SSH traffic on port 22
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows access from anywhere
  }

  # Allow inbound HTTP traffic on port 8080
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows access from anywhere
  }

  # Allow inbound PostgreSQL traffic on port 5432
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows access from anywhere
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 key pair (replace with your existing key pair or create a new one)
resource "aws_key_pair" "my_key" {
  key_name   = "my-key-pair"  # Name of the key pair (this will not create a new private key, just associate it)
  public_key = file("~/.ssh/id_rsa.pub")  # Path to your public key (use an existing key or generate one)
}

# Provision the EC2 instance
resource "aws_instance" "my_vm" {
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "t2.medium"  # Use t2.medium instance type
  key_name      = aws_key_pair.my_key.key_name

  security_groups = [aws_security_group.allow_ports.name]

  tags = {
    Name = "MyTerraformEC2"
  }
}

# Output the public IP of the instance
output "instance_public_ip" {
  value = aws_instance.my_vm.public_ip
}
