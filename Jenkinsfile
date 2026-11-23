pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            parallel {
                    stage('Backend') {
                        steps {
                            dir('src/backend') {
                                sh '''
                                    python3 -m venv .venv
                                    .venv/bin/pip install --upgrade pip
                                    .venv/bin/pip install -r requirements-dev.txt
                                    '''
                            }
                        }
                    }
                    stage('Frontend') {
                        steps {
                            dir('src/frontend') {
                                sh 'npm ci'
                            }
                        }
                    }
                    stage('Catalog') {
                        steps {
                            dir('src/catalog') {
                               sh '''
                                python3 -m venv .venv
                                .venv/bin/pip install --upgrade pip
                                .venv/bin/pip install -r requirements-dev.txt
                               '''
                            }
                        }
                    }
                }
        }
        stage('Code Quality') {
            parallel {
                stage('Backend') {
                    steps {
                        dir('src/backend') {
                            sh '''
                                .venv/bin/black --check ./app
                                .venv/bin/flake8 ./app
                                .venv/bin/isort --check-only ./app
                            '''
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('src/frontend') {
                            sh 'npm run lint'
                        }
                    }
                }
                stage('Catalog') {
                    steps {
                        dir('src/catalog') {
                             sh '''
                                .venv/bin/black --check ./app
                                .venv/bin/flake8 ./app
                                .venv/bin/isort --check-only ./app
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Run tests') {
            parallel {
                 stage('Backend') {
                    steps {
                         dir('src/backend/tests') {
                            sh '.venv/bin/python -m pytest -v'
                        }
                    }

                 }
                 stage('frontend') {
                    sh 'npm test -- --runInBand'
                 }
                 stage('catalog') {
                     steps {
                         dir('src/catalog/tests') {
                            sh '.venv/bin/python -m pytest'
                        }
                    }
                 }
            }
        }
        stage('Build Docker images') {
           parallel {
                stage('Backend') {
                    steps {
                        sh '''
                            docker build -t mini-shop-backend:${BUILD_NUMBER} \
                                -f src/backend/Dockerfile src/backend
                        '''
                    }
                }

                stage('Frontend') {
                    steps {
                        sh '''
                            docker build -t mini-shop-frontend:${BUILD_NUMBER} \
                                -f src/frontend/Dockerfile src/frontend
                        '''
                    }
                }

                stage('Catalog') {
                    steps {
                        sh '''
                            docker build -t mini-shop-catalog:${BUILD_NUMBER} \
                                -f src/catalog/Dockerfile src/catalog
                        '''
                    }
                }
            }
        }
        stage('Show Build Information') {
            steps {
                sh '''
                 echo "Build number $BULD_NUMBER"
                 echo "GIT commit SHA: $GIT_COMMIT"
                 echo "Job name: $JOB_NAME"
                 echo "Workspace: $WORKSPACE"
                 echo "Build URL: $BUILD_URL"
                '''
            }
        }
    }
}