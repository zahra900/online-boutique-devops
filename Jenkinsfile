pipeline {
    agent {
        label 'docker-python-node'
    }
    stages {
            stage('Diagnose Docker Permissions') {
        steps {
            sh '''
                echo "=== NODE ==="
                echo "NODE_NAME=$NODE_NAME"
                hostname
                id

                echo "=== CONTAINER IDENTITY ==="
cat /etc/hostname
cat /proc/self/cgroup
readlink /proc/1/ns/mnt
readlink /proc/self/ns/mnt

echo "=== SOCKET ==="
stat -c 'GID=%g Permissions=%a Inode=%i' /var/run/docker.sock

                echo "=== Current user ==="
                whoami
                id

                echo "=== Docker socket ==="
                ls -ln /var/run/docker.sock
                stat -c "Owner=%u Group=%g Permissions=%a" /var/run/docker.sock

                echo "=== Docker connection ==="
                docker ps
            '''
        }
    }
        stage('Verify Build Environment') {
            steps {
                sh '''
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
                         dir('src/backend') {
                            sh '.venv/bin/python -m pytest -v'
                        }
                    }

                 }
                 stage('frontend') {
                    steps {
                        dir('src/frontend') {
                          sh 'npm test -- --runInBand'
                        }
                    }
                 }
                 stage('catalog') {
                     steps {
                         dir('src/catalog') {
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
                 echo "Build number $BUILD_NUMBER"
                 echo "GIT commit SHA: $GIT_COMMIT"
                 echo "Job name: $JOB_NAME"
                 echo "Workspace: $WORKSPACE"
                 echo "Build URL: $BUILD_URL"
                '''
            }
        }
    }
}