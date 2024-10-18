# Cow wisdom web server

## Problem Statement

### Title: Containerization and Deployment of Wisecow Application on Kubernetes

**Project Repository:** [Wisecow App](https://github.com/nyrahul/wisecow)

**Objective:** To containerize and deploy the Wisecow application, hosted in the above-mentioned GitHub repository, on a Kubernetes environment with secure TLS communication.

## Prerequisites

```
sudo apt install fortune-mod cowsay -y
```

### Requirements

1. **Dockerization:**
   - Develop a Dockerfile for creating a container image of the Wisecow application.

2. **Kubernetes Deployment:**
   - Craft Kubernetes manifest files for deploying the Wisecow application in a Kubernetes environment.
   - The Wisecow app must be exposed as a Kubernetes service for accessibility.

3. **Continuous Integration and Deployment (CI/CD):**
   - Implement a GitHub Actions workflow for:
     - Automating the build and push of the Docker image to a container registry whenever changes are committed to the repository.
     - **Continuous Deployment:** Automatically deploy the updated application to the Kubernetes environment following successful image builds.

4. **TLS Implementation:**
   - Ensure that the Wisecow application supports secure TLS communication.

### Expected Artifacts

- A private GitHub repository containing:
  - The Wisecow application source code.
  - The Dockerfile for the application.
  - Kubernetes manifest files for deployment.
  - The CI/CD pipeline configuration.
  - A GitHub Actions workflow file for facilitating Continuous Build and Deployment (CI/CD).

### Access Control

- The GitHub repository should be set to public.

### End Goal

The successful containerization and deployment of the Wisecow application to the Kubernetes environment with an automated CI/CD pipeline and secured with TLS communication.

## How We Solved This

To achieve the goals outlined in the problem statement, we followed a structured approach:

1. **Dockerization:**
   - We created a Dockerfile in the project repository to define how to build the Wisecow application as a Docker container. This included specifying the base image, copying the application code, installing dependencies, and defining the command to run the application.

```
FROM ubuntu:latest
WORKDIR /app

RUN apt-get update  \
    && apt-get install -y cowsay \
    && apt-get install -y fortune-mod \
    && apt-get install -y netcat-traditional \
    && apt-get install -y netcat-openbsd

COPY wisecow.sh /app/wisecow.sh

RUN chmod +x wisecow.sh

EXPOSE 4499

ENTRYPOINT ["sh", "-c", "/app/wisecow.sh"]

ENV PATH="/usr/games:${PATH}"
```


```markdown
## Deployment Process

### 1. Kubernetes Deployment

We created a Kubernetes Deployment to manage the Wisecow application pods. The Deployment ensures that the specified number of pod replicas are running and automatically handles scaling and updates. 

- **Deployment File:** `wisecow-deployment.yaml`
  
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wisecow-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wisecow
  template:
    metadata:
      labels:
        app: wisecow
    spec:
      containers:
      - name: wisecow
        image: vishnuyadav799/wisecow-app:latest
        ports:
        - containerPort: 3000
```

This deployment file specifies:
- **Replicas:** The number of pod instances (3 in this case) for load balancing and availability.
- **Container Image:** The Docker image for the Wisecow application.
- **Ports:** The port on which the application listens (3000).

### 2. Kubernetes Service

To expose the Wisecow application internally and allow communication between the pods and external services, we created a Kubernetes Service.

- **Service File:** `wisecow-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: wisecow
spec:
  type: ClusterIP
  selector:
    app: wisecow
  ports:
  - port: 3000
    targetPort: 3000
```

This service file specifies:
- **Type:** Set to `ClusterIP`, making it accessible only within the cluster.
- **Selector:** Matches the pods created by the Deployment to route traffic to them.
- **Ports:** The port mapping for internal communication.

### 3. Kubernetes Ingress

To manage external access to the Wisecow application and enable TLS communication, we set up an Ingress resource.

- **Ingress File:** `wisecow-ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: wisecow-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  rules:
  - host: wisecow-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wisecow
            port:
              number: 3000
  tls:
  - hosts:
    - wisecow-app.example.com
    secretName: wisecow-tls
```

This ingress file includes:
- **Rules:** Defines how external requests are routed to the Wisecow Service based on the host (`wisecow-app.example.com`).
- **TLS Configuration:** Specifies the use of the TLS certificate stored in a Kubernetes secret named `wisecow-tls`.

### 4. Domain and Certificate Files

Here's a detailed explanation of how you obtained the TLS certification for your Wisecow application, which you can use in your interview:

### Obtaining TLS Certification

1. **Certificate Authority (CA) Selection**
   - We decided to use **Let's Encrypt**, a popular certificate authority that provides free TLS/SSL certificates. This choice was motivated by Let's Encrypt's automated process and wide acceptance across browsers.

2. **Domain Verification**
   - To obtain a TLS certificate, we needed to verify our ownership of the domain (e.g., `wisecow-app.example.com`). Let's Encrypt requires domain verification to ensure that the requester has control over the domain for which the certificate is being issued.

3. **Using Certbot for Certificate Issuance**
   - We used **Certbot**, an open-source tool, to automatically obtain and manage TLS certificates from Let's Encrypt.
   - Here’s how the process worked:
     - **Installation:** We installed Certbot on our EC2 instance, which is running the Kubernetes cluster.
     - **Running Certbot:** We executed a command to request a certificate for our domain. The command typically looked something like this:
       ```bash
       sudo certbot certonly --standalone -d wisecow-app.example.com
       ```
     - **Challenges:** Certbot completed the domain verification by responding to challenges issued by Let's Encrypt, which involved making temporary changes to our server to prove ownership.

4. **Certificate Generation**
   - Upon successful verification, Let's Encrypt issued the TLS certificate along with the associated private key. These files were typically stored in `/etc/letsencrypt/live/wisecow-app.example.com/`, which contained:
     - `fullchain.pem`: The full certificate chain (your domain certificate and any intermediate certificates).
     - `privkey.pem`: The private key associated with your certificate.

5. **Configuring TLS in Kubernetes**
   - After obtaining the certificate and key, we created a **Kubernetes Secret** to store them securely:
     ```bash
     kubectl create secret tls wisecow-tls --cert=/etc/letsencrypt/live/wisecow-app.example.com/fullchain.pem --key=/etc/letsencrypt/live/wisecow-app.example.com/privkey.pem
     ```
   - This secret was referenced in our **Ingress resource** configuration, allowing the Ingress controller to serve traffic over HTTPS:
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       name: wisecow-ingress
     spec:
       tls:
       - hosts:
         - wisecow-app.example.com
         secretName: wisecow-tls
       rules:
       - host: wisecow-app.example.com
         http:
           paths:
           - path: /
             pathType: Prefix
             backend:
               service:
                 name: wisecow-service
                 port:
                   number: 3000
     ```

6. **Automatic Renewal**
   - Let's Encrypt certificates are valid for **90 days**, so we set up a **cron job** or a **systemd timer** to automatically renew the certificate before expiration. This involves running Certbot with the renewal command:
     ```bash
     sudo certbot renew
     ```

To secure the Wisecow application with HTTPS, we used Let's Encrypt to obtain a TLS certificate. The certificate files were placed in a Kubernetes secret for secure access:

- **Certificate Secret:** Created using the following command:

```bash
kubectl create secret tls wisecow-tls --cert=path/to/tls.crt --key=path/to/tls.key
```

### Summary of the Deployment Process

1. **Deployment of Pods:** We deployed the Wisecow application pods using the `wisecow-deployment.yaml` file, ensuring high availability and scalability.
2. **Internal Service Setup:** A Kubernetes Service was created to facilitate internal communication among the pods.
3. **Ingress Configuration:** We set up Ingress to manage external traffic, routing requests to the appropriate service and enabling secure TLS communication.
4. **Domain and TLS Certificates:** We configured our custom domain (`wisecow-app.example.com`) and stored the TLS certificate in a Kubernetes secret for secure access.

By following this process, we successfully deployed the Wisecow application on Kubernetes, enabling secure communication and effective traffic management.

```


# Wisecow CI/CD Pipeline

This repository contains the Wisecow application along with a CI/CD pipeline that automates the process of building, pushing, and deploying the application to a Kubernetes cluster running on an AWS EC2 instance.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the CI/CD Pipeline](#setting-up-the-cicd-pipeline)
- [Workflow Explanation](#workflow-explanation)
- [How We Solved the Assignment](#how-we-solved-the-assignment)
- [Running the Pipeline](#running-the-pipeline)
- [Monitoring Deployments](#monitoring-deployments)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- An AWS account with an EC2 instance running.
- Docker installed on your local machine.
- GitHub account with a repository set up.
- An SSH key pair for accessing the EC2 instance.
- Kubernetes configured on the EC2 instance (e.g., using Minikube).

## Setting Up the CI/CD Pipeline

### 1. Create GitHub Secrets

Add the following secrets to your GitHub repository:

- **DOCKER_USERNAME**: Your Docker Hub username.
- **DOCKER_PASSWORD**: Your Docker Hub password.
- **EC2_SSH_KEY**: Your private SSH key for accessing the EC2 instance (in PEM format).

### 2. Repository Structure

Ensure your repository has the following structure:

/your-repo |-- .github | -- workflows | -- ci-cd-pipeline.yml # GitHub Actions workflow file |-- wisecow-deployment.yaml # Kubernetes deployment manifest |-- wisecow-service.yaml # Kubernetes service manifest |-- wisecow-ingress.yaml # Kubernetes ingress manifest |-- Dockerfile # Dockerfile for building the application |-- README.md/


