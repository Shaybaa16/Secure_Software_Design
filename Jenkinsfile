pipeline {
    agent any
    
    options {
        skipDefaultCheckout(true)  // Don't use cached checkout
    }
    
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to deploy')
        choice(name: 'DEPLOY_ENV', choices: ['development', 'staging'], description: 'Deployment environment')
        booleanParam(name: 'RUN_SECURITY_SCANS', defaultValue: true, description: 'Run security scans?')
    }
    
    environment {
        VENV_DIR = 'venv'
        SCAN_HOME = "${WORKSPACE}"
    }

    stages {
        stage('Checkout Latest Code') {
            steps {
                echo "=== Fetching latest code from GitHub ==="
                cleanWs()  // Clean workspace first
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[url: 'https://github.com/Shaybaa16/Secure_Software_Design']]])
                
                // Show what commit we're on
                bat 'git log -1 --oneline'
                bat 'dir'  // Show files in workspace
            }
        }

        stage('Setup Workspace') {
            steps {
                bat 'if exist reports rmdir /s /q reports'
                bat 'mkdir reports'
            }
        }

        stage('Verify Files') {
            steps {
                script {
                    echo "=== Verifying required files exist ==="
                    
                    // List all files for debugging
                    bat 'echo Listing all files:'
                    bat 'dir /B'
                    
                    // Check if requirements.txt exists
                    if (!fileExists('requirements.txt')) {
                        error("requirements.txt file not found in repository root!")
                    }
                    echo "✅ requirements.txt found"
                }
            }
        }

        // ... rest of your stages remain the same