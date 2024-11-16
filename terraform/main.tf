provider "aws" {
  region = "us-east-1"  # Specify your AWS region here
}

# Create a security group for the EC2 instance
resource "aws_security_group" "allow_ssh" {
  name_prefix = "allow_ssh"
  description = "Allow SSH inbound traffic"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows access from anywhere
  }
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
  instance_type = "t2.micro"  # Choose your instance type
  key_name      = aws_key_pair.my_key.key_name

  security_groups = [aws_security_group.allow_ssh.name]

  tags = {
    Name = "MyTerraformEC2"
  }
}

# Output the public IP of the instance
output "instance_public_ip" {
  value = aws_instance.my_vm.public_ip
}
