pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'No Build Step Required!'
      }
    }

    stage('Login Tests') {
      parallel {
        stage('Login Tests') {
          agent {
            node {
              label 'master'
            }

          }
          steps {
            bat 'pytest -vs testCases/test_login.py'
          }
        }

        stage('Add Customer Tests') {
          agent {
            node {
              label 'windows_node'
            }

          }
          steps {
            bat 'pytest -vs testCases/test_addcustomer.py'
          }
        }

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
}