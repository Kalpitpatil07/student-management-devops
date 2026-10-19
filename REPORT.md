# DevOps Assignment Report
## Enterprise Student Record & Academic Management Platform

### 1. Objective
To demonstrate an end-to-end DevOps workflow by developing a Python/Flask academic management application, tracking its source with Git/GitHub, validating changes with pytest through Jenkins, packaging the application in Docker, and deploying it to Kubernetes on Minikube.

### 2. Technology stack
- Python and Flask: application and HTTP routes
- SQLite: lightweight local database
- pytest: automated tests
- Git/GitHub: source control and collaboration
- Jenkins: continuous integration pipeline
- Docker: application image and container
- Kubernetes/Minikube: local orchestration and deployment

### 3. Functional modules
1. Student records: create and list student records; enforce unique email and PRN.
2. Courses: create and list courses; enforce unique course code and valid credits.
3. Faculty: create and list faculty records.
4. Enrollments: register a student in a course; reject invalid and duplicate registrations.
5. Marks and GPA: record marks for enrolled students, validate the 0–100 range, and calculate illustrative grade points and GPA.

### 4. CI/CD workflow
1. Developer commits and pushes code to GitHub.
2. Jenkins checks out the repository.
3. Jenkins creates a Python virtual environment and installs `requirements.txt`.
4. Jenkins runs pytest; a failing test fails the pipeline.
5. On the main branch, Jenkins builds the Docker image `student-platform:v1.0.0`.
6. Kubernetes Deployment and Service manifests deploy the image to Minikube.
7. `/health`, Pod status, service access, and logs are used to verify deployment.

### 5. Test plan
- Student service: create/get student, normalize email, reject duplicate identifiers, require fields.
- Course registration: enroll a valid student, reject duplicate enrollment, reject unknown student/course.
- Marks management: calculate grade points/GPA, reject out-of-range marks, require enrollment before marks entry.

### 6. Execution evidence to capture
Add your own screenshots after running the commands:
1. Application dashboard in the browser.
2. GitHub repository with project files.
3. Terminal output of `pytest -q` showing all tests passed.
4. Jenkins pipeline with successful stages.
5. Docker image listed by `docker images`.
6. `kubectl get pods,services` showing the running workload.
7. Application opened through `minikube service student-platform-service`.

### 7. Limitations
This is an educational prototype. It does not include login/role permissions, production secrets management, enterprise database deployment, or durable Kubernetes storage. The GPA scale is an example and should be replaced if the faculty provides an official grading scheme. The Jenkins pipeline assumes a Linux agent with Python and Docker available.

### 8. Conclusion
The project demonstrates the integration of application development, version control, automated testing, containerization, and Kubernetes deployment. It illustrates how automated quality checks reduce manual errors and make application delivery repeatable.
