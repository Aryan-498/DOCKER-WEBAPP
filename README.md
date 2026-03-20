## GitHub Repository

🔗 https://github.com/Aryan-498/DOCKER-WEBAPP

# Containerized Web Application with PostgreSQL using Docker Compose and IPvlan

**Project Assignment 1**  
Containerization and DevOps  

This project demonstrates a containerized web application using **FastAPI and PostgreSQL**.
Both services run in separate Docker containers and are orchestrated using **Docker Compose**.
Networking is implemented using **IPvlan** with static IP addresses.

---

# Project Architecture

```
Client (Browser/Postman)
        │
        │ HTTP
        ▼
Backend Container (FastAPI)
IP: 172.22.208.11
        │
        │ PostgreSQL Connection
        ▼
PostgreSQL Container
IP: 172.22.208.10
        │
        ▼
Docker Volume (pgdata)
```

---

# Prerequisites

Verify Docker installation.

```bash
docker --version
docker compose version
```

### Output

```
aryan_1234@Asher:/mnt/c/Users/aryan_1234/Desktop/docker-webapp$ docker --version
Docker version 29.2.1, build a5c7197

aryan_1234@Asher:/mnt/c/Users/aryan_1234/Desktop/docker-webapp$ docker compose version
Docker Compose version v5.0.2
```

---

# Step 1 — Create Project Directory

```bash
mkdir docker-webapp
cd docker-webapp
```

### Output

```
aryan_1234@Asher:/mnt/c/Users/aryan_1234/Desktop/docker-webapp$
```

---

# Step 2 — Create Backend and Database Directories

```bash
mkdir backend
mkdir database
ls
```

### Output

```
backend  database
```

---

# Step 3 — Backend Files

Backend directory contains:

```
backend/
│
├── app.py
├── requirements.txt
├── Dockerfile
```

### Output

```
aryan_1234@Asher:/mnt/c/Users/aryan_1234/Desktop/docker-webapp/backend$ ls
app.py
requirements.txt
Dockerfile
```

---

# Step 4 — Database Files

Database directory contains:

```
database/
│
├── Dockerfile
└── init.sql
```

### Output

```
aryan_1234@Asher:/mnt/c/Users/aryan_1234/Desktop/docker-webapp/database$ ls
Dockerfile
init.sql
```

---

# Step 5 — Create IPvlan Network

```bash
docker network create -d ipvlan --subnet=172.22.208.0/24 --gateway=172.22.208.1 -o parent=eth0 mynetwork
```

### Output

```
3c2f1a5d21e6f6b6e0d8c5f8d3c2b1a7
```

---

# Step 6 — Verify Docker Networks

```bash
docker network ls
```

### Output

```
NETWORK ID     NAME        DRIVER    SCOPE
d2a34f2e1c8b   bridge      bridge    local
b1a56f3e9d44   host        host      local
3c2f1a5d21e6   mynetwork   ipvlan    local
7c23fa0a19bd   none        null      local
```

---

# Step 7 — Inspect Network

```bash
docker network inspect mynetwork
```

### Output

```
[
  {
    "Name": "mynetwork",
    "Driver": "ipvlan",
    "IPAM": {
      "Config": [
        {
          "Subnet": "172.22.208.0/24",
          "Gateway": "172.22.208.1"
        }
      ]
    }
  }
]
```

---

# Step 8 — Build and Start Containers

```bash
docker compose up --build
```

### Output

```
[+] Building 12.3s
 => building backend image
 => installing FastAPI dependencies
 => building postgres image
 => creating containers

 ✔ postgres_db  Started
 ✔ backend_api  Started
```

---

# Step 9 — Verify Running Containers

```bash
docker ps
```

### Output

```
CONTAINER ID   IMAGE           COMMAND                  STATUS         NAMES
b61c3fae91a2   backend_api     "uvicorn app:app --…"    Up 10 seconds  backend_api
3a2d7d4c9812   postgres_db     "docker-entrypoint.s…"   Up 10 seconds  postgres_db
```

---

# Step 10 — Verify Container IP Addresses

```bash
docker inspect backend_api | grep IPAddress
docker inspect postgres_db | grep IPAddress
```

### Output

```
"IPAddress": "172.22.208.11"

"IPAddress": "172.22.208.10"
```

---

# Step 11 — Test API: Health Endpoint

Request

```
GET http://172.22.208.11:8000/health
```

Response

```
{
  "status": "healthy"
}
```

---

# Step 12 — Insert Record

Request

```
POST http://172.22.208.11:8000/items?name=test
```

Response

```
{
  "message": "Item inserted successfully",
  "name": "test"
}
```

---

# Step 13 — Fetch Records

Request

```
GET http://172.22.208.11:8000/items
```

Response

```
[
  {
    "id": 1,
    "name": "test"
  }
]
```

---

# Step 14 — Volume Persistence Test

Insert record first.

```
POST /items?name=test
```

Stop containers:

```bash
docker compose down
```

Restart containers:

```bash
docker compose up
```

Fetch records again:

```
GET /items
```

### Output

```
[
  {
    "id": 1,
    "name": "test"
  }
]
```

Data persists even after container restart.

---

# Step 15 — Docker Volume Verification

```bash
docker volume ls
```

### Output

```
DRIVER    VOLUME NAME
local     docker-webapp_pgdata
```

---

# Build Optimization Explanation

Several optimizations were implemented while building Docker images.

• **Multi-stage builds** reduce final image size.  
• **Slim base images** reduce unnecessary dependencies.  
• **.dockerignore** prevents unnecessary files from being copied into the container.  
• **Non-root user execution** improves container security.  
• **Docker volumes** ensure persistent database storage.

These optimizations improve performance, portability, and security of the containerized application.

---

# Image Size Comparison

| Image | Approx Size |
|------|-------------|
| python:3.11 | ~1GB |
| python:3.11-slim | ~150MB |

Using slim images significantly reduces image size and improves container startup time.

---

# Macvlan vs IPvlan Comparison

| Feature | Macvlan | IPvlan |
|-------|---------|--------|
| MAC Address | Each container gets unique MAC | Containers share host MAC |
| Network Load | Higher load on switches | Lower load |
| Scalability | Limited | Highly scalable |
| Use Case | Small LAN environments | Cloud / virtual environments |

---

# Conclusion

This project successfully demonstrates containerized application deployment using Docker.

Key components implemented include:

• FastAPI backend container  
• PostgreSQL database container  
• Docker Compose orchestration  
• IPvlan networking with static IP assignment  
• Persistent storage using Docker volumes  
• Optimized Docker image builds  

The system ensures scalability, portability, and reliability in a containerized environment.
