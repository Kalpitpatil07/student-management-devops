# Enterprise Student Record & Academic Management Platform

A student-friendly DevOps assignment implementation using Python, Flask, SQLite, pytest, Git/GitHub, Jenkins, Docker, and Kubernetes with Minikube.

## Features

- Student records with unique email and PRN validation
- Course and faculty records
- Student course enrollment with duplicate-enrollment validation
- Marks entry with score validation
- Grade points and a simple example GPA calculation
- `/health` endpoint for deployment health checks
- pytest test suites for student service, course registration, and marks management
- Jenkins CI pipeline, Dockerfile, and Kubernetes Deployment/Service manifests

> The GPA scale in this sample is illustrative, not an official college grading policy. Replace it with your faculty's prescribed scheme if required. This is an educational starter project, not a production-ready ERP: authentication, authorization, privacy controls, and production database persistence are not included.

## Requirements

- Python 3.10+ (Docker image uses Python 3.12)
- Git
- For later stages: Jenkins, Docker Desktop, kubectl, and Minikube

## 1. Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again.

## 2. Run tests

```powershell
pytest -q
```

Expected: all tests pass. Tests use temporary SQLite databases and do not change your local app database.

## 3. Push to GitHub

Create an empty GitHub repository, then from this folder run:

```bash
git init
git add .
git commit -m "Build student management DevOps project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL. Do not commit passwords, tokens, or secrets.

## 4. Jenkins CI

1. Install/run Jenkins in an environment that has Python 3 and (for the Docker stage) Docker CLI/daemon access.
2. Create a Pipeline job connected to the GitHub repository.
3. Select “Pipeline script from SCM”, SCM = Git, and script path = `Jenkinsfile`.
4. Configure a GitHub webhook if your Jenkins instance is reachable by GitHub; otherwise use polling or run builds manually.
5. Build the job and inspect the Checkout, Install dependencies, and Automated tests stages.
6. The Docker image stage runs on the `main` branch. Jenkins must have Docker installed and permission to access the Docker daemon.

Note: this Jenkinsfile uses Unix shell commands (`sh`) and is intended for a Linux Jenkins agent. A Windows-only Jenkins agent needs equivalent PowerShell/batch steps or a Linux agent.

## 5. Build and run with Docker

```bash
docker build -t student-platform:v1.0.0 .
docker run --rm -p 5000:5000 student-platform:v1.0.0
```

Open `http://localhost:5000`. The container's default database is ephemeral unless you mount a persistent volume.

## 6. Deploy to Minikube

Start Minikube and point Docker CLI to its image environment so the local image is available in the cluster:

```bash
minikube start
minikube docker-env
```

For PowerShell, apply the environment command printed by Minikube as instructed by your installed version; then build the image inside that environment:

```bash
docker build -t student-platform:v1.0.0 .
kubectl apply -f k8s/
kubectl get deployments,pods,services
minikube service student-platform-service
```

If your Minikube setup uses a separate image runtime, load the image with `minikube image load student-platform:v1.0.0` instead of rebuilding in Minikube's Docker environment.

The sample Deployment uses two replicas and an `emptyDir` volume. Data is not durable across Pod replacement. For a demonstration, use one Pod or a persistent storage design if you need shared/durable SQLite data; a real multi-replica application should use a shared external database.

## 7. Useful verification commands

```bash
pytest -q
docker images
docker ps
kubectl get pods
kubectl describe deployment student-platform
kubectl logs deployment/student-platform
kubectl get service student-platform-service
```

## Project layout

```text
app.py
student_service.py
requirements.txt
tests/
  test_student_service.py
  test_course_registration.py
  test_marks_mgmt.py
Jenkinsfile
Dockerfile
k8s/
  deployment.yaml
  service.yaml
```

## Assignment mapping

- Application domain: Student, Course, Faculty, Enrollment, Marks
- Validation: duplicate PRN/email, duplicate enrollment, valid course/student, marks range
- CI test coverage areas: student service, course registration, marks management
- Docker image tag: `student-platform:v1.0.0`
- Kubernetes deployment: `k8s/` manifests, Minikube, NodePort service
