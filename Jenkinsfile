pipeline {
    agent any
    
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
        stage('Clean Workspace') {
            steps {
                cleanWs()
                bat 'if exist reports rmdir /s /q reports'
                bat 'mkdir reports'
            }
        }

        stage('Setup Environment') {
            steps {
                echo "=== Setting up Python environment ==="
                bat """
                python -m venv "${VENV_DIR}"
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                python -m pip install --upgrade pip
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '=== Installing dependencies ==='
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                pip install -r requirements.txt
                pip install pytest safety detect-secrets
                """
            }
        }

        stage('SAST - SonarQube Scan') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Running SAST with SonarQube ==="
                withSonarQubeEnv('sonarqube') {
                    bat """
                    call "${VENV_DIR}\\\\Scripts\\\\activate"
                    sonar-scanner ^
                      -Dsonar.projectKey=flask-app-${params.VERSION} ^
                      -Dsonar.projectName="Flask App ${params.VERSION}" ^
                      -Dsonar.sources=. ^
                      -Dsonar.host.url=http://localhost:9000 ^
                      -Dsonar.python.version=3
                    """
                }
            }
        }

        stage('Dependency Security Scan') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Scanning Python dependencies for vulnerabilities ==="
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                safety check --json > reports/safety-report.json || echo "Safety scan completed"
                pip list --format=json > reports/dependencies.json
                """
                
                // Simple Python dependency check
                script {
                    if (fileExists('reports/safety-report.json')) {
                        def safetyReport = readJSON file: 'reports/safety-report.json'
                        echo "Safety scan found ${safetyReport.vulnerabilities?.size() ?: 0} vulnerabilities"
                    }
                }
            }
        }

        stage('Secrets Detection') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Scanning for hardcoded secrets ==="
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                detect-secrets scan --all-files > reports/secrets-scan.json || echo "Secrets scan completed"
                """
            }
        }

        stage('Code Quality Gate') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Waiting for SonarQube Quality Gate ==="
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }

        stage('Security Report') {
            steps {
                echo "=== Generating Security Reports ==="
                script {
                    // Publish any generated reports
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: '*.html',
                        reportName: 'Security Reports'
                    ])
                    
                    // Archive all security reports
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "=== Pipeline completed ==="
            echo "Security Scans: ${params.RUN_SECURITY_SCANS}"
            echo "Environment: ${params.DEPLOY_ENV}"
            
            // Cleanup
            bat 'taskkill /F /IM python.exe >nul 2>&1 || echo "No Python processes to kill"'
        }
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}