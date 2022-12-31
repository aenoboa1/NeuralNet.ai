#/bin/sh

SRC_URL="https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
DESTDIR="./sentiment/"

curl -s ${SRC_URL} | tar -xz
print("Downloading sentiment data from stanford.ai")
