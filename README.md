# Cross Encoder FastAPI

This is a simple cross encoder FastAPI service for ranking passages based on a
query. It uses the sentence-transformers library to load a pre-trained cross
encoder model.

This is a naive implementation of a cross encoder service.
For production use, consider using vLLM deployment with rerank API.

See:
https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html#rerank-api

## run locally

```sh
pyenv shell 3.11
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run FastAPI app
uvicorn cross_encoder_service:app --host 0.0.0.0 --port 8000 --reload

# check app is running
curl http://localhost:9000/health

# test with curl
curl -X POST "http://localhost:9000/rank" \
-H "accept: application/json" -H "Content-Type: application/json" \
-d '{
    "query": "What is the capital of France?",
    "passages": [
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
        "Madrid is the capital of Spain.",
        "Rome is the capital of Italy."
    ],
    "top_k": 2
}' | jq
```

## build and run the cross encoder FastAPI app

```sh
docker build -t cross-encoder-fastapi .

# use -e to set PORT 9000 to avoid conflict with other services
# Use -v to mount host volume to cache huggingface model to save loading time.
docker run --rm --name cross-encoder-fastapi-local -e PORT=9000 -p 9000:9000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    cross-encoder-fastapi:latest
```

## build and push to docker hub

Use latest version tag for the image to push to dockerhub.

```sh
# check docker buildx builder instances
docker buildx ls
# if there's only one builder instance, need to create another builder
# instance to support parallel multi-platform builds
docker buildx create --name mybuilder
# use the builder instance
docker buildx use mybuilder

# dockerhub login with access token in shell env var
# docker login --username=ikalidocker --password=$DOCKERHUB_TOKEN
# recommended, more secure to use stdin pipe to pass token
echo $DOCKERHUB_TOKEN | docker login --username=ikalidocker --password-stdin

# if there are multiple builders active, run multi-platform builds and push in one cli
docker buildx build --platform linux/amd64,linux/arm64 \
    -t ikalidocker/cross-encoder-fastapi:latest \
    --push .

docker buildx build --platform linux/amd64,linux/arm64 \
    -t ikalidocker/cross-encoder-fastapi:gpu \
    --push .
```

Pull image from docker hub and run:

```sh
docker pull ikalidocker/cross-encoder-fastapi:latest && \
docker run --rm --name cross-encoder-fastapi -p 8000:8000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    ikalidocker/cross-encoder-fastapi:latest

# check app is running
curl http://localhost:8000/health
```

## deploy to GKE

See [README_k8s.md](README_k8s.md) for the k8s setup steps.

Test from public IP endpoint:

```sh
PUBLIC_IP="34.86.129.157"

curl http://$PUBLIC_IP/cross-encoder/health

curl -X POST "http://$PUBLIC_IP/cross-encoder/rank" \
-H "accept: application/json" -H "Content-Type: application/json" \
-d '{
    "query": "What is the capital of France?",
    "passages": [
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
        "Madrid is the capital of Spain.",
        "Rome is the capital of Italy."
    ],
    "top_k": 2
}' | jq
```
