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
    - name: docker-sock
      mountPath: /var/run/docker.sock
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
    }
  }

  stages {
    stage('Build') {
      steps {
        container('builder') {
          sh '''
            set -e
            docker version
            docker build -t api-devops:latest .
          '''
        }
      }
    }

    stage('Deploy') {
      steps {
        container('builder') {
          sh '''
            set -e

            # 1) bajar kubectl para la arquitectura del pod (arm64 vs amd64)
            ARCH="$(uname -m)"
            if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
              KARCH="arm64"
            else
              KARCH="amd64"
            fi

            KVER="v1.29.8"
            wget -qO kubectl "https://dl.k8s.io/release/${KVER}/bin/linux/${KARCH}/kubectl"
            chmod +x kubectl

            # 2) armar kubeconfig in-cluster con serviceaccount del pod
            APISERVER="https://kubernetes.default.svc"
            TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
            CACERT="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
            NAMESPACE="$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)"

            ./kubectl config set-cluster in-cluster --server="${APISERVER}" --certificate-authority="${CACERT}" --embed-certs=true
            ./kubectl config set-credentials sa --token="${TOKEN}"
            ./kubectl config set-context ctx --cluster=in-cluster --user=sa --namespace="${NAMESPACE}"
            ./kubectl config use-context ctx

            # 3) deploy
            ./kubectl apply -f k8s.yaml
            ./kubectl get pods
          '''
        }
      }
    }
  }
}
