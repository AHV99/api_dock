pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          set -e

          # Detectar arquitectura del pod Jenkins
          ARCH="$(uname -m)"
          case "$ARCH" in
            x86_64|amd64) KARCH="amd64" ;;
            aarch64|arm64) KARCH="arm64" ;;
            *)
              echo "Arquitectura no soportada: $ARCH"
              exit 1
              ;;
          esac

          KVER="v1.29.8"
          curl -L -o kubectl "https://dl.k8s.io/release/${KVER}/bin/linux/${KARCH}/kubectl"
          chmod +x kubectl

          APISERVER="https://kubernetes.default.svc"
          CACERT="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
          NAMESPACE="$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)"

          # NO imprimas el token en logs
          set +x
          TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
          set -x

          ./kubectl config set-cluster in-cluster --server="${APISERVER}" --certificate-authority="${CACERT}" --embed-certs=true
          ./kubectl config set-credentials sa --token="${TOKEN}"
          ./kubectl config set-context ctx --cluster=in-cluster --user=sa --namespace="${NAMESPACE}"
          ./kubectl config use-context ctx

          ./kubectl apply -f k8s.yaml
          ./kubectl get pods
          ./kubectl get svc
        '''
      }
    }
  }
}
