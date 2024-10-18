# Use a base image
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update  \
    && apt-get install -y cowsay \
    && apt-get install -y fortune-mod \
    && apt-get install -y netcat-traditional \
    && apt-get install -y netcat-openbsd

# Copy the script into the container
COPY wisecow.sh /app/wisecow.sh

# Make the script executable
RUN chmod +x wisecow.sh

# Expose the server port
EXPOSE 4499

# Set the startup command
ENTRYPOINT ["sh", "-c", "/app/wisecow.sh"]

# Set PATH environment variable
ENV PATH="/usr/games:${PATH}"

