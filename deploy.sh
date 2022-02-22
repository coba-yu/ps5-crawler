poetry export -f requirements.txt --output src/requirements.txt --without-hashes

cd src || exit

set -eu
function finally {
  cd ..
}
trap finally EXIT

zip -r ../ps5-crawler-src.zip . -x \*/__pycache__/\*
