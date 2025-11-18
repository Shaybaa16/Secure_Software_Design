pipeline {
    agent any
    
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to deploy')
        choice(name: 'DEPLOY_ENV', choices: ['development', 'staging', 'production'], description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Execute test stage?')
        booleanParam(name: 'START_FLASK', defaultValue: true, description: 'Start Flask application?')
    }
    
    environment {
        VENV_DIR = 'venv'
        FLASK_APP = 'app.py'
        FLASK_ENV = 'development'
        APP_VERSION = "${params.VERSION}"
        DEPLOYMENT_ENV = "${params.DEPLOY_ENV}"
    }

    stages {
        stage('Setup Virtual Environment') {
            steps {
                echo "=== Creating Python virtual environment for ${APP_VERSION} ==="
                bat """
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                python -m pip install --upgrade pip
                """
            }
        }

        stage('Install Requirements') {
            steps {
                echo '=== Installing dependencies from requirements.txt ==='
                bat """
                call %VENV_DIR%\\Scripts\\activate
                pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                echo "=== Running tests for ${DEPLOYMENT_ENV} environment ==="
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if exist tests (
                    pytest --maxfail=1 --disable-warnings -q
                ) else (
                    echo No tests directory found — skipping tests.
                )
                """
            }
        }

        stage('Run Flask App') {
            when {
                expression { params.START_FLASK == true }
            }
            steps {
                echo "=== Starting Flask app for version ${APP_VERSION} ==="
                bat """
                REM Kill any previous Flask instances
                for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /F /PID %%a >nul 2>&1

                call %VENV_DIR%\\Scripts\\activate
                set FLASK_APP=%FLASK_APP%
                set FLASK_ENV=%FLASK_ENV%

                REM Start Flask app in background
                start "" python -m flask run --host=0.0.0.0 --port=5000

                timeout /t 5 >nul
                echo Flask app started successfully on ${DEPLOYMENT_ENV}.
                exit /b 0
                """
            }
        }
    }

    post {
        always {
            echo "=== Build Finished - Environment: ${DEPLOYMENT_ENV} ==="
            echo "=== Version: ${APP_VERSION} ==="
            bat 'for /f "tokens=5" %%a in (''netstat -ano ^| findstr :5000'') do taskkill /F /PID %%a >nul 2>&1'
        }
        success {
            echo '✅ Build succeeded!'
        }
        failure {
            echo '❌ Build failed!'
        }
        changed {
            echo '🔄 Build status changed from previous build'
        }
    }
}