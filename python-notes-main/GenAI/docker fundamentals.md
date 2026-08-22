# 🐳 The Docker Master Document: From Zero to Senior

## Table of Contents
1. **The Absolute Basics:** What is Docker and why do we need it?
2. **Beginner Level:** Running your first containers and writing Dockerfiles
3. **Mid-Level (Under the Hood):** How Docker actually works (Linux Internals)
4. **Senior Level (Image Building):** Multi-stage builds, the PID 1 problem, and Distroless
5. **Senior Level (Security):** Locking down your containers
6. **Senior Level (Networking & Storage):** Managing traffic and data
7. **Senior Level (Observability & Automation):** Healthchecks and Docker Compose
8. **Beyond Docker:** Where this fits into the real world

---

## Part 1: The Absolute Basics 

### What is Docker?
Imagine you write a piece of software on your laptop. It works perfectly. You send it to your friend, and it crashes on their laptop because they have a different version of Python, missing files, or a different operating system. 

Historically, we solved this with **Virtual Machines (VMs)**. A VM is like building a fully functioning house (an entire Guest Operating System) inside your computer just to run one application. It takes up gigabytes of space and minutes to start.

**Docker** solves this using **Containers**. 
* Think of a VM as an isolated **house** with its own plumbing, electricity, and foundation.
* Think of a Container as an **apartment** in a high-rise building. It shares the building's plumbing and foundation (the Host Operating System) but has its own locked door. 

Because containers share the host's operating system, they start in milliseconds, use barely any memory, and guarantee that **"if it works on my machine, it works everywhere."**

### Core Terminology
* **Image:** A read-only blueprint. It contains your code, libraries, and the exact tools needed to run your app. (Like a recipe).
* **Container:** A running instance of an Image. (Like the cake you baked from the recipe).
* **Dockerfile:** The text file containing the instructions to build an Image.
* **Registry:** A place to store and share images (e.g., Docker Hub, exactly like GitHub but for Docker images).

---

## Part 2: Beginner Level (Getting Your Hands Dirty)

### The Essential Commands
Once you install Docker on your computer, you interact with it via the terminal.

**1. Running a container:**
```bash
docker run -d -p 8080:80 --name my-website nginx
```
* `docker run`: Starts a container.
* `-d`: Detached mode (runs in the background so you can keep using your terminal).
* `-p 8080:80`: Port mapping. Maps port 8080 on your laptop to port 80 inside the container.
* `--name my-website`: Gives the container a friendly name.
* `nginx`: The name of the image to use (a popular web server). Docker will download it automatically if you don't have it.

**2. Viewing running containers:**
```bash
docker ps
```

**3. Stopping and removing a container:**
```bash
docker stop my-website
docker rm my-website
```

### Writing Your First Dockerfile
Let’s say you have a simple Python web app. Here is how you containerize it.

Create a file named `Dockerfile` (no extension):
```dockerfile
# 1. Start with a base image that already has Python installed
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your application code from your laptop into the container
COPY . /app

# 4. Run a command to install dependencies
RUN pip install -r requirements.txt

# 5. Tell Docker what to do when the container starts
CMD ["python", "app.py"]
```
To build this into an image, run:
```bash
docker build -t my-python-app:v1 .
```
*(The `-t` tags it with a name, and the `.` tells Docker to look in the current folder for the Dockerfile).*

---

## Part 3: Mid-Level (Under the Hood)
*How does a container actually isolate itself?* A senior engineer knows that **Docker is not magic; it’s just a wrapper around Linux kernel features.**

### 1. Namespaces (Isolation)
Namespaces act like blinders on a horse. They trick a process into thinking it is the only process running on the computer.
* **PID Namespace:** Isolates Process IDs. Inside the container, your app thinks it is process #1. On your host machine, it might actually be process #14593.
* **NET Namespace:** Gives the container its own isolated network, IP address, and ports.
* **MNT Namespace:** Isolates the file system. The container cannot see your laptop's files.

### 2. Control Groups (cgroups) (Resource Limits)
If namespaces dictate what a container can *see*, cgroups dictate what a container can *use*. cgroups prevent one container from eating up all your computer's RAM and crashing everything else.
```bash
# Example: Limiting a container to use only 512 Megabytes of RAM and half a CPU core
docker run -d --memory="512m" --cpus="0.5" nginx
```

### 3. Union File Systems (UFS / Overlay2)
Docker images are built in **layers**. Every command in a Dockerfile (`FROM`, `COPY`, `RUN`) creates a new layer. 
Imagine layers like sheets of transparent glass stacked on top of each other. 
* If you change one line of code and rebuild, Docker doesn't rebuild the whole OS; it only replaces the glass sheet (layer) that changed. This makes building incredibly fast.
* **Copy-on-Write (CoW):** When a container runs, it gets a thin "read-write" layer on top of the read-only image layers. If the container deletes a file, it doesn't actually delete it from the image; it just hides it in the read-write layer.

### 4. The Architecture (OCI)
When you type `docker run`, you are using the **Docker Client (CLI)**. 
1. The CLI talks to the **Docker Daemon (`dockerd`)** (a background service).
2. `dockerd` talks to a tool called **`containerd`** (which manages downloading images and networking).
3. `containerd` hands the actual creation of the container to a tiny tool called **`runc`**.
*(Senior note: Modern orchestration tools like Kubernetes completely bypassed `dockerd` and just use `containerd` directly).*

---

## Part 4: Senior Level (Advanced Image Building)
Seniors don't just make images that work; they make images that are tiny, secure, and fast.

### 1. Multi-Stage Builds
Compiling code requires heavy tools (like compilers and massive libraries). But running the compiled code doesn't. Multi-stage builds let you use one image to build the code, and a tiny, separate image to run it.

```dockerfile
# Stage 1: The Builder (Heavy, has all the tools)
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp main.go

# Stage 2: The Final Image (Tiny, only has what is needed to run)
FROM alpine:latest
WORKDIR /app
# Copy ONLY the compiled binary from Stage 1
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```
*Result:* Your image shrinks from 800MB to 15MB.

### 2. Distroless and Scratch Images
Even `alpine` linux has a shell (`/bin/sh`) and package managers. If a hacker gets into your container, they can use that shell to download malware.
Seniors use **Distroless** images (created by Google) or **Scratch** (an empty image). These contain *literally nothing* except your app. No shell, no terminal. You can't even "log into" them. This drastically improves security.

### 3. The PID 1 Problem & Graceful Shutdowns
When you stop a container (`docker stop`), Docker sends a polite signal (`SIGTERM`) to the main process (PID 1) saying, "Please finish what you are doing and shut down." If the app doesn't shut down in 10 seconds, Docker violently kills it (`SIGKILL`), causing data corruption.
Many apps (like Node.js or Java) do not know how to handle `SIGTERM` properly when running as PID 1.
**The Fix:** Use a tiny init manager like `tini`.
```dockerfile
# Add tini to handle signals
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]
```

---

## Part 5: Senior Level (Security)
By default, Docker runs your applications as the **Root user** inside the container. If a hacker breaks out of the container, they might have Root access to your actual host server!

### 1. Running as Non-Root
Always create a dedicated, low-privilege user in your Dockerfile.
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
# Create a user called 'appuser'
RUN useradd -m appuser
# Switch to that user
USER appuser
CMD ["node", "app.js"]
```

### 2. Dropping Linux Capabilities
Even as root, you can strip the container of dangerous kernel powers using the `--cap-drop` flag.
```bash
# Drops all super-powers, only adds back the ability to bind to a network port
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

---

## Part 6: Senior Level (Networking & Storage)

### Advanced Networking
* **Bridge (Default):** Containers are on a private network and can talk to each other if on the same bridge.
* **Host:** The container completely bypasses network isolation and shares the host's IP and ports. (High performance, low security).
* **None:** The container has no internet or network access at all. Great for highly secure, localized data processing.

### Managing State (Storage)
Containers are ephemeral (temporary). If a container is deleted, all its data is deleted. To save data (like a database), we use volumes.
1. **Bind Mounts:** Maps a specific folder on your laptop to a folder in the container. Great for local development.
   ```bash
   docker run -v /Users/me/mycode:/app nginx
   ```
2. **Docker Volumes:** Docker manages the storage somewhere on the host. Much safer for production.
   ```bash
   docker volume create my-db-data
   docker run -v my-db-data:/var/lib/mysql mysql
   ```
3. **tmpfs:** Stores data strictly in RAM. Never written to a hard drive. Perfect for highly sensitive things like passwords or temporary cache.

---

## Part 7: Senior Level (Observability & Automation)

### 1. Healthchecks
Just because a container is "running" doesn't mean the app is working. The app might have frozen or run out of database connections. A `HEALTHCHECK` tells Docker how to test if the app is actually healthy.
```dockerfile
# Ping the web server every 30 seconds. If it fails, mark container as 'Unhealthy'
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

### 2. Docker Compose (Advanced Automation)
Typing long `docker run` commands with 15 flags is annoying. **Docker Compose** lets you define your entire environment in a simple YAML file (`docker-compose.yml`).

```yaml
version: '3.8'
services:
  web:
    image: my-web-app:v1
    ports:
      - "80:80"
    depends_on:
      - database

  database:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: supersecret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```
Now, you just type `docker compose up -d` and Docker creates the network, starts the database, waits for it, and then starts your web app.

---

## Part 8: Beyond Docker (The Ecosystem)

A senior engineer knows that in massive companies (like Netflix or Spotify), you don't run containers manually using Docker commands. If you have 5,000 containers across 100 servers, and one server catches fire, who restarts those containers on a new server?

This is where **Kubernetes (K8s)** comes in. 
* Docker is the tool used to **build** and **package** the container.
* Kubernetes is the tool used to **orchestrate** (manage, scale, and heal) thousands of containers across many servers.
