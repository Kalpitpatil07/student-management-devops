pipeline {
    agent any
    options { timestamps() }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }
        stage('Automated tests') {
            steps {
                sh '. .venv/bin/activate && pytest -q'
            }
        }
        stage('Build Docker image') {
            when { branch 'main' }
            steps {
                sh 'docker build -t student-platform:v1.0.0 .'
            }
        }
    }
    post {
        always { echo 'CI pipeline finished. Review stage results above.' }
        failure { echo 'Build failed: inspect the failing stage and fix the issue before merging.' }
    }
}
