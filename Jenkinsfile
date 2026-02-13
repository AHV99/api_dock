pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: creator-pipeline
spec:
  containers:

  - name: builder
    image: docker:24.0.7-cli
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock

  - name: kubectl
    image: bitnami/kubectl:1.29.8
    command:
    - cat
    tty: true

  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
    }
  }

  stages {

    stage('Build Image') {
      steps {
        container('builder') {
          sh '''
          docker version
          docker build -t api-devops:latest .
          docker images
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh '''
          kubectl version --client
          kubectl apply -f k8s.yaml
          kubectl get pods
          '''
        }
      }
    }

  }
}
