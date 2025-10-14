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
                sh '''
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                '''
            }
        }

    //     stage('Install Requirements') {
    //         steps {
    //             echo '=== Installing dependencies from requirements.txt ==='
    //             sh '''
    //             source ${VENV_DIR}/bin/activate
    //             pip install -r requirements.txt
    //             '''
    //         }
    //     }

    //     stage('Test') {
    //         steps {
    //             echo '=== Running tests (if any) ==='
    //             sh '''
    //             source ${VENV_DIR}/bin/activate
    //             if [ -d "tests" ]; then
    //                 pytest --maxfail=1 --disable-warnings -q
    //             else
    //                 echo "No tests directory found — skipping tests."
    //             fi
    //             '''
    //         }
    //     }

    //     stage('Run Flask App') {
    //         steps {
    //             echo '=== Running Flask app ==='
    //             sh '''
    //             source ${VENV_DIR}/bin/activate
    //             export FLASK_APP=${FLASK_APP}
    //             export FLASK_ENV=${FLASK_ENV}
    //             nohup flask run --host=0.0.0.0 --port=5000 &
    //             sleep 5
    //             echo "Flask app started successfully!"
    //             '''
    //         }
    //     }
    // }

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
}

