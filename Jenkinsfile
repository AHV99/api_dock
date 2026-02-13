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
    command: ["cat"]
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock

  - name: kubectl
    image: bitnami/kubectl:1.29
    command: ["cat"]
    tty: true

  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
'''
    }
  }

  stages {
    stage('Build') {
      steps {
        container('builder') {
          sh 'docker version'
          sh 'docker build -t api-devops:latest .'
        }
      }
    }

    stage('Deploy') {
      steps {
        container('kubectl') {
          sh 'kubectl apply -f k8s.yaml'
          sh 'kubectl get pods'
        }
      }
    }
  }
}
