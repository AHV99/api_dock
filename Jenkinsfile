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

          # 1) Descargar kubectl (sin instalar nada en el sistema)
          KVER="v1.29.8"
          curl -L -o kubectl "https://dl.k8s.io/release/${KVER}/bin/linux/amd64/kubectl"
          chmod +x kubectl

          # 2) Crear kubeconfig usando el ServiceAccount del pod (in-cluster)
          APISERVER="https://kubernetes.default.svc"
          TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
          CACERT="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
          NAMESPACE="$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)"

          ./kubectl config set-cluster in-cluster --server="${APISERVER}" --certificate-authority="${CACERT}" --embed-certs=true
          ./kubectl config set-credentials sa --token="${TOKEN}"
          ./kubectl config set-context ctx --cluster=in-cluster --user=sa --namespace="${NAMESPACE}"
          ./kubectl config use-context ctx

          # 3) Deploy (usa el yaml del repo)
          ./kubectl apply -f k8s.yaml

          # 4) Esperar rollout (si tu k8s.yaml tiene Deployment llamado "demo-app" cambia el nombre abajo)
          ./kubectl get deploy
        '''
      }
    }
  }
}
