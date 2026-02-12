pipeline {
  agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: builder
            image: docker:latest
            command:
            - cat
            tty: true
        '''
    }
  }

  stages {
    stage('Build') {
      steps {
        container('builder') {
          sh 'docker build -t api-devops:latest .'
        }
      }
    }

    stage('Deploy') {
      steps {
        container('builder') {
          sh 'kubectl apply -f k8s.yaml'
        }
      }
    }
  }
}
