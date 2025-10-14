pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        FLASK_APP = 'app.py'
        FLASK_ENV = 'development'
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         echo '=== Checking out source code ==='
        //         git 'https://github.com/Shaybaa16/Secure_Software_Design.git'
        //     }
        // }

        stage('Setup Virtual Environment') {
            steps {
                echo '=== Creating Python virtual environment ==='
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
            steps {
                echo '=== Running tests (if any) ==='
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
            steps {
                echo '=== Running Flask app ==='
                bat """
                python app.py
                echo Flask app started successfully!
                """
            }
        }

    }

    post {
        always {
            echo '=== Build Finished ==='
        }
        success {
            echo '✅ Build succeeded!'
        }
        failure {
            echo '❌ Build failed!'
        }
    }
}
