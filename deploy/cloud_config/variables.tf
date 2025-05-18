variable "aws_region" {
  default = "us-east-1"
}

variable "ami_id" {
  # Amazon Linux 2 or Ubuntu AMI ID for your region (e.g., Ubuntu 22.04)
  default = "ami-0fc5d935ebf8bc3bc"  # Example for us-east-1 Ubuntu
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  description = "Name of the EC2 key pair"
}
