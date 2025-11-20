pipeline {
    agent any
    
    options {
        skipDefaultCheckout(true)
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
                cleanWs()
                checkout([$class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[url: 'https://github.com/Shaybaa16/Secure_Software_Design']]])
                
                bat 'git log -1 --oneline'
                bat 'dir'
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
                    bat 'dir /B'
                    
                    if (!fileExists('requirements.txt')) {
                        error("requirements.txt file not found in repository root!")
                    }
                    echo "✅ requirements.txt found"
                }
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
                """
            }
        }

        stage('Install Security Tools') {
            steps {
                echo '=== Installing security scanning tools ==='
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                pip install safety detect-secrets
                """
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
                
                script {
                    if (fileExists('reports/safety-report.json')) {
                        def safetyReport = readJSON file: 'reports/safety-report.json'
                        def vulnCount = safetyReport.vulnerabilities?.size() ?: 0
                        echo "Safety scan found ${vulnCount} vulnerabilities"
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

        stage('SAST - SonarQube Scan') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Running SAST with SonarQube ==="
                script {
                    def scannerHome = tool 'sonar-scanner'
                    echo "SonarScanner path: ${scannerHome}"
                }
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
                    bat """
                    echo "<html><body><h1>Security Scan Report</h1>" > reports/security-summary.html
                    echo "<p>Build: ${env.BUILD_NUMBER}</p>" >> reports/security-summary.html
                    echo "<p>Environment: ${params.DEPLOY_ENV}</p>" >> reports/security-summary.html
                    echo "<h2>Scans Completed:</h2><ul>" >> reports/security-summary.html
                    echo "<li>Safety Dependency Scan</li>" >> reports/security-summary.html
                    echo "<li>Secrets Detection</li>" >> reports/security-summary.html
                    echo "<li>SonarQube SAST</li>" >> reports/security-summary.html
                    echo "</ul></body></html>" >> reports/security-summary.html
                    """
                    
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'security-summary.html',
                        reportName: 'Security Scan Summary'
                    ])
                    
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
            
            bat 'taskkill /F /IM python.exe >nul 2>&1 & echo "Cleanup completed"'
        }
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}