pipeline {
  agent any
  stages {
    stage('Start Docker-Grid') {
      steps {
        bat 'docker-compose up -d'
      }
    }

    stage('Tests') {
      parallel {
        stage('Login Tests') {
          agent {
            node {
              label 'master'
            }

          }
          steps {
            bat 'pytest -vs --browser grid-chrome testCases/test_login.py'
          }
        }

        stage('Add Customer Tests') {
          agent {
            node {
              label 'windows_node'
            }

          }
          steps {
            bat 'pytest -vs --browser grid-ff -n 2 testCases/test_addcustomer.py'
          }
        }

      }
    }

    stage('Shutdown Docker-Grid') {
      steps {
        bat 'docker-compose down'
      }
    }

    stage('Deploy to Staging') {
      steps {
        echo 'Deploy to Staging'
      }
    }

    stage('Deploy to Production') {
      steps {
        input 'Deploy to Production?'
      }
    }

  }
  post {
    always {
      echo 'One way or another, I have finished'
    }

    success {
      echo 'I succeeded!'
    }

    unstable {
      echo 'I am unstable :/'
    }

    failure {
      echo 'I failed :('
      mail(to: 'siddharth2k007@gmail.com', subject: "Failed Pipeline ${currentBuild.fullDisplayName}", body: " For details about the failure, see ${env.BUILD_URL}")
    }

    changed {
      echo 'Things were different before...'
    }

  }
}