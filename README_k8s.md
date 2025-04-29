

## k8s

A run-through of the k8s setup steps of kubernetes manifests.

```sh
PROJECT_ID=poc-data-platform-289915
CLUSTER_SERVICE_ACCOUNT=node-sa@$PROJECT_ID.iam.gserviceaccount.com
KSA_NAME=cross-encoder-sa
KSA_NAMESPACE=cross-encoder


# check gcloud project
gcloud config set project $PROJECT_ID
gcloud info
gcloud container clusters list

# Run this BEFORE creating the k8s service account (KSA) in manifest file
# Create IAM binding between K8s ServiceAccount and GCP ServiceAccount
gcloud iam service-accounts add-iam-policy-binding $CLUSTER_SERVICE_ACCOUNT \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:$PROJECT_ID.svc.id.goog[$KSA_NAMESPACE/$KSA_NAME]"

# check roles for the GCP service account, which should include the 
# workloadIdentityUser role binding member of the KSA
# check the workload identity user role binding referencing the iam service account
gcloud iam service-accounts get-iam-policy node-sa@poc-data-platform-289915.iam.gserviceaccount.com
```

This allows the Kubernetes ServiceAccount `cross-encoder-sa` in namespace 
`cross-encoder` to act as the GCP service account node-sa.

This IAM binding **MUST** be done before deploying the KSA in the k8s
manifest (`k8s/service-account.yaml`).

## Deploy k8s resources

```sh
# check or select the target k8s context
kubectx

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/service-account.yaml
kubectl apply -f k8s/configmap.yaml

kubectl apply -f k8s/deployment.yaml

# check, refresh or delete the deployment with the latest image
kubectl describe deployment cross-encoder -n cross-encoder
kubectl delete deployment cross-encoder -n cross-encoder
kubectl rollout restart deployment cross-encoder -n cross-encoder

kubectl apply -f k8s/service.yaml
kubectl get services -n cross-encoder

kubectl apply -f k8s/ingress.yaml
# check the created ingress
kubectl get ingress -n cross-encoder

kubectl apply -f k8s/hpa.yaml
kubectl get hpa -n cross-encoder
```
