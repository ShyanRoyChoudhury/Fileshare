# 📂 Fileshare

A secure, full-stack file-sharing platform built with **React (frontend) + Django/Flask (backend)**, running on **Docker** with **self-signed SSL certificates**.

---

## 🚀 Features

- ✅ Secure file sharing over HTTPS  
- ✅ Backend powered by Gunicorn & Django/Flask  
- ✅ Frontend served with Nginx  
- ✅ Self-signed SSL certificates for encryption  
- ✅ Dockerized for easy deployment  

---

## 📌 Setup & Installation

### Clone the Repository
```sh
git clone https://github.com/ShyanRoyChoudhury/Fileshare.git
cd Fileshare
```

### 2️⃣ Configure Firebase Authentication
This project uses Firebase for authentication. Follow these steps to set it up:
* Go to Firebase Console
* Navigate to Project Settings > Service Accounts
* Click Generate new private key
Download the file and place it in:
```sh
backend/api/service-account.json
```
* Update the Firebase config in the frontend

* Open the file:
```sh
frontend/config/firebase-config.ts

```

### 2️⃣ Generate Self-Signed SSL Certificates
Run the following command to create SSL certificates locally:
```sh
mkdir -p certs 
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
   -keyout certs/server.key -out certs/server.crt \
   -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

```

### 3️⃣ Build and Start the Containers
```sh
docker-compose up --build -d

```

### 4️⃣ Ready to Roll 🎸

### 

