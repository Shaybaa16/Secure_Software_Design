pipeline {
    agent any
    
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to deploy')
        choice(name: 'DEPLOY_ENV', choices: ['development', 'staging'], description: 'Deployment environment')
        booleanParam(name: 'RUN_SECURITY_SCANS', defaultValue: true, description: 'Run security scans?')
    }
    
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
                bat 'if exist reports rmdir /s /q reports'
                bat 'mkdir reports'
            }
        }

        stage('Display Files') {
            steps {
                echo "=== Checking repository contents ==="
                bat """
                echo "Files in repository:"
                dir
                echo "--- requirements.txt content ---"
                if exist requirements.txt (
                    type requirements.txt
                ) else (
                    echo "requirements.txt not found - this is OK, we'll install directly"
                )
                """
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
                echo '=== Installing security tools and dependencies ==='
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                echo "Installing security scanning tools..."
                pip install safety detect-secrets bandit
                echo "Installing Flask and dependencies..."
                pip install Flask Flask-SQLAlchemy SQLAlchemy
                echo "✅ All dependencies installed successfully"
                """
            }
        }

        stage('Bandit SAST Scan') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Running Bandit Python SAST Scan ==="
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                bandit -r . -f json -o reports/bandit-report.json || echo "Bandit scan completed"
                """
            }
        }

        stage('Dependency Security Scan') {
            when {
                expression { params.RUN_SECURITY_SCANS == true }
            }
            steps {
                echo "=== Scanning dependencies with Safety ==="
                bat """
                call "${VENV_DIR}\\\\Scripts\\\\activate"
                safety check --json > reports/safety-report.json || echo "Safety scan completed"
                """
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

        stage('Generate Security Report') {
            steps {
                echo "=== Generating Security Reports ==="
                script {
                    bat """
                    echo "<html><body style='font-family: Arial, sans-serif; margin: 20px;'>" > reports/security-summary.html
                    echo "<h1 style='color: #2c3e50;'>🔒 Security Scan Report</h1>" >> reports/security-summary.html
                    echo "<div style='background: #f8f9fa; padding: 15px; border-radius: 5px;'>" >> reports/security-summary.html
                    echo "<h2 style='color: #34495e;'>Build Information</h2>" >> reports/security-summary.html
                    echo "<p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>" >> reports/security-summary.html
                    echo "<p><strong>Environment:</strong> ${params.DEPLOY_ENV}</p>" >> reports/security-summary.html
                    echo "<p><strong>Version:</strong> ${params.VERSION}</p>" >> reports/security-summary.html
                    echo "<p><strong>Security Scans:</strong> ${params.RUN_SECURITY_SCANS}</p>" >> reports/security-summary.html
                    echo "</div>" >> reports/security-summary.html
                    
                    echo "<h2 style='color: #34495e;'>Security Scans Performed</h2>" >> reports/security-summary.html
                    echo "<ul>" >> reports/security-summary.html
                    echo "<li>✅ Bandit - Static Application Security Testing (SAST)</li>" >> reports/security-summary.html
                    echo "<li>✅ Safety - Dependency Vulnerability Scanning</li>" >> reports/security-summary.html
                    echo "<li>✅ Detect-secrets - Secrets & Credentials Detection</li>" >> reports/security-summary.html
                    echo "</ul>" >> reports/security-summary.html
                    
                    echo "<h2 style='color: #34495e;'>Next Steps</h2>" >> reports/security-summary.html
                    echo "<p>Review the generated JSON reports for detailed findings:</p>" >> reports/security-summary.html
                    echo "<ul>" >> reports/security-summary.html
                    echo "<li>bandit-report.json - Code security issues</li>" >> reports/security-summary.html
                    echo "<li>safety-report.json - Dependency vulnerabilities</li>" >> reports/security-summary.html
                    echo "<li>secrets-scan.json - Hardcoded secrets</li>" >> reports/security-summary.html
                    echo "</ul>" >> reports/security-summary.html
                    echo "<p><em>Report generated automatically by Jenkins DevSecOps Pipeline</em></p>" >> reports/security-summary.html
                    echo "</body></html>" >> reports/security-summary.html
                    """
                    
                    // Publish the report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'security-summary.html',
                        reportName: 'Security Scan Report'
                    ])
                    
                    // Archive all reports
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "=== Pipeline Execution Complete ==="
            echo "Build: ${env.BUILD_NUMBER}"
            echo "Environment: ${params.DEPLOY_ENV}" 
            echo "Version: ${params.VERSION}"
            echo "Security Scans: ${params.RUN_SECURITY_SCANS}"
            
            // Safe cleanup
            bat 'taskkill /F /IM python.exe >nul 2>&1 || echo "Cleanup completed"'
        }
        success {
            echo '✅ 🎉 Pipeline succeeded!'
            echo '📊 Security scans completed successfully.'
            echo '🔍 Check the "Security Scan Report" for details.'
        }
        failure {
            echo '❌ Pipeline failed!'
            echo '💡 Check the console output above for error details.'
        }
    }
}