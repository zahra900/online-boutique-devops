pipeline {
    agent {
        label 'docker-python-node'
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(
            numToKeepStr: '5',
            artifactNumToKeepStr: '10'
        ))
        skipDefaultCheckout(true)
    }

    environment {
        BACKEND_IMAGE = "mini-shop-backend"
        CATALOG_IMAGE = "mini-shop-catalog"
        FRONTEND_IMAGE = "mini-shop-frontend"
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                script {
                    env.GIT_COMMIT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    echo "Branch: ${env.BRANCH_NAME ?: 'unknown'}"
                    echo "Commit: ${env.GIT_COMMIT}"
                    echo "Build: ${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Verify Build Environment') {
            steps {
                sh '''
                    set -eu

                    echo "=== Python ==="
                    python3 --version

                    echo "=== Node.js ==="
                    node --version

                    echo "=== npm ==="
                    npm --version

                    echo "=== Docker ==="
                    docker version

                    echo "=== Git ==="
                    git --version
                '''
            }
        }

        stage('Install Dependencies') {
            parallel {

                stage('Backend Dependencies') {
                    steps {
                        dir('src/backend') {
                            sh '''
                                set -eu
                                python3 -m venv .venv
                                .venv/bin/pip install --upgrade pip
                                .venv/bin/pip install -r requirements-dev.txt
                            '''
                        }
                    }
                }

                stage('Catalog Dependencies') {
                    steps {
                        dir('src/catalog') {
                            sh '''
                                set -eu
                                python3 -m venv .venv
                                .venv/bin/pip install --upgrade pip
                                .venv/bin/pip install -r requirements-dev.txt
                            '''
                        }
                    }
                }

                stage('Frontend Dependencies') {
                    steps {
                        dir('src/frontend') {
                            sh 'npm ci'
                        }
                    }
                }
            }
        }

        stage('Code Quality') {
            parallel {

                stage('Backend Quality') {
                    steps {
                        dir('src/backend') {
                            sh '''
                                set -eu
                                .venv/bin/black --check ./app ./tests
                                .venv/bin/isort --check-only ./app ./tests
                                .venv/bin/flake8 ./app ./tests
                            '''
                        }
                    }
                }

                stage('Catalog Quality') {
                    steps {
                        dir('src/catalog') {
                            sh '''
                                set -eu
                                .venv/bin/black --check ./app ./tests
                                .venv/bin/isort --check-only ./app ./tests
                                .venv/bin/flake8 ./app ./tests
                            '''
                        }
                    }
                }
            }
        }

        stage('Unit Tests') {
            parallel {

                stage('Backend Tests') {
                    steps {
                        dir('src/backend') {
                            sh '''
                                set -eu
                                mkdir -p reports
                                .venv/bin/python -m pytest -v \
                                    --junitxml=reports/backend-results.xml
                            '''
                        }
                    }
                }

                stage('Catalog Tests') {
                    steps {
                        dir('src/catalog') {
                            sh '''
                                set -eu
                                mkdir -p reports
                                .venv/bin/python -m pytest -v \
                                    --junitxml=reports/catalog-results.xml
                            '''
                        }
                    }
                }

                stage('Frontend Tests') {
                    steps {
                        dir('src/frontend') {
                            sh '''
                                set -eu
                                npm test -- --ci \
                                    --reporters=default \
                                    --reporters=jest-junit
                            '''
                        }
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit allowEmptyResults: false,
                    testResults: '''
                        src/backend/reports/*.xml,
                        src/catalog/reports/*.xml,
                        src/frontend/junit.xml
                    '''
            }
        }

        stage('Build Docker Images') {
            parallel {

                stage('Backend Image') {
                    steps {
                        sh '''
                            set -eu
                            docker build \
                                -t ${BACKEND_IMAGE}:${IMAGE_TAG} \
                                -t ${BACKEND_IMAGE}:${BUILD_NUMBER} \
                                -f src/backend/Dockerfile src/backend
                        '''
                    }
                }

                stage('Catalog Image') {
                    steps {
                        sh '''
                            set -eu
                            docker build \
                                -t ${CATALOG_IMAGE}:${IMAGE_TAG} \
                                -t ${CATALOG_IMAGE}:${BUILD_NUMBER} \
                                -f src/catalog/Dockerfile src/catalog
                        '''
                    }
                }

                stage('Frontend Image') {
                    steps {
                        sh '''
                            set -eu
                            docker build \
                                -t ${FRONTEND_IMAGE}:${IMAGE_TAG} \
                                -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                                -f src/frontend/Dockerfile src/frontend
                        '''
                    }
                }
            }
        }

        stage('Verify Docker Images') {
            steps {
                sh '''
                    set -eu

                    docker image inspect ${BACKEND_IMAGE}:${IMAGE_TAG}
                    docker image inspect ${CATALOG_IMAGE}:${IMAGE_TAG}
                    docker image inspect ${FRONTEND_IMAGE}:${IMAGE_TAG}

                    echo "All three Docker images were built successfully."
                '''
            }
        }
    }

    post {
        always {
            echo "Build ${BUILD_NUMBER} finished: ${currentBuild.currentResult}"
            echo "Job: ${JOB_NAME}"
            echo "Build URL: ${BUILD_URL}"
        }

        success {
            echo "CI pipeline passed successfully."
        }

        failure {
            echo "CI pipeline failed. Review the failed stage and test reports."
        }
    }
}
