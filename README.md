# Face Blur API

A Flask-based API that detects and blurs faces in images. This guide will walk you through deploying this API on **Azure Kubernetes Service (AKS).**

---

## 🚀 Deployment Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/kaustu88/face-blur-api.git
cd face-blur-api
```
---
### 2️⃣ Set Up the Local Environment
a. Install Dependencies
```sh
pip install flask opencv-python numpy
```
b. Run the Application Locally
```sh
python face_blur_simple.py
```
c. Test the API Locally
```sh
curl -X POST "http://localhost:5000/blur" -F "image=@/path/to/your/image.jpg" --output @/path/to/your/blurred_image.jpg
```

---

## 3️⃣ Set Up Azure Resources

### a. Create a Resource Group
```sh
az group create --name face-blur-rg --location eastus
```

### b. Create an Azure Container Registry (ACR)
```sh
az acr create --resource-group face-blur-rg --name facebluracr --sku Basic
```

---

## 4️⃣ Build and Push Docker Image to ACR

### a. Log in to ACR
```sh
az acr login --name facebluracr
```

### b. Build the Docker Image
```sh
docker build -t facebluracr.azurecr.io/face-blur-api:latest .
```

### c. Push the Image to ACR
```sh
docker push facebluracr.azurecr.io/face-blur-api:latest
```

### d. Verify the Image in ACR
```sh
az acr repository list --name facebluracr --output table
```
---

## 5️⃣ Create and Configure AKS Cluster

### a. Create an AKS Cluster
```sh
az aks create \
  --resource-group face-blur-rg \
  --name face-blur-aks \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys
```

### b. Connect to the AKS Cluster
```sh
az aks get-credentials --resource-group face-blur-rg --name face-blur-aks
```
### c. Check Running Nodes
```sh
kubectl get nodes
```

---
## 6️⃣ Create a Secret to Access ACR
a. Create a Kubernetes Secret
```sh
kubectl create secret docker-registry acr-secret \
  --docker-server=facebluracr.azurecr.io \
  --docker-username=facebluracr \
  --docker-password=<YOUR-ACR-PASSWORD> \
  --docker-email=<YOUR-EMAIL>
```

---

## 7️⃣ Deploy to AKS

### a. Create a Kubernetes Deployment YAML (`deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: face-blur-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: face-blur-api
  template:
    metadata:
      labels:
        app: face-blur-api
    spec:
      imagePullSecrets:
        - name: acr-secret
      containers:
      - name: face-blur-api
        image: facebluracr.azurecr.io/face-blur-api:latest
        ports:
        - containerPort: 5000
```

### b. Apply the Deployment
```sh
kubectl apply -f deployment.yaml
```

### c. Check Running Pods
```sh
kubectl get pods
```
---
## 7️⃣ Create a Service to Expose the Deployment
### a. Create a Service YAML (`service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: face-blur-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: face-blur-api
```

### b. Apply the Service
```sh
kubectl apply -f service.yaml
```

---

## 6️⃣ Retrieve the External IP Address
```sh
kubectl get svc face-blur-service
```
🔹 **Once the `EXTERNAL-IP` is assigned**, you can access your Flask application via that IP.

---

## 🎯 Testing the API

To test the API, send a POST request with an image file to the `/blur` endpoint:

```sh
curl -X POST "http://<EXTERNAL-IP>/blur" -F "image=@/path/to/your/image.jpg" --output blurred_image.jpg
```

Replace `<EXTERNAL-IP>` with the external IP address obtained earlier and `/path/to/your/image.jpg` with the path to the image you want to process.

---

## 🗑 Cleanup Resources
To remove all created resources, run:
```sh
az group delete --name face-blur-rg --yes --no-wait
```

---

## 📚 References

- [Deploy an application to Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-application)
- [Building a CI/CD Pipeline for a Flask Application with Jenkins, Docker, and Kubernetes](https://medium.com/@kalimitalha8/building-a-ci-cd-pipeline-for-a-flask-application-with-jenkins-docker-and-kubernetes-f9c9106140bd)

---


