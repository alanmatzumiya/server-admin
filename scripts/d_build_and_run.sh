docker build -t jupyter -f Dockerfile .

docker run --env PORT=8888 -it -p 8888:8888 jupyter
