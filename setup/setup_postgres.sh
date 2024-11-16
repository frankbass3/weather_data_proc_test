#!/bin/bash

# Script to install the latest stable PostgreSQL on Ubuntu

# Update the system package list
echo "Updating package list..."
sudo apt update -y

# Install prerequisite packages
echo "Installing prerequisites..."
sudo apt install -y wget gnupg lsb-release

# Add PostgreSQL repository
echo "Adding PostgreSQL APT repository..."
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Update the package list again to include PostgreSQL repository
echo "Updating package list with PostgreSQL repository..."
sudo apt update -y

# Install PostgreSQL
echo "Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Enable and start PostgreSQL service
echo "Starting and enabling PostgreSQL service..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Verify the installation
echo "Verifying PostgreSQL installation..."
psql --version

# MULTIPOLYGON in PostgreSQL
sudo apt install postgis

echo "PostgreSQL installation completed successfully!"