# Usage

## Docker
Build the docker container.
```
docker build -t cristiangauma/nft_downloader .
```

Run the command using a docker container.
```
docker run -v YOUR_DOWNLOADS_DIR:/downloads -v PATH_TO_LIST_OF_NFTS.txt:/nft_list.txt cristiangauma/nft_downloader pipenv run python3 src/cli.py

```

## Pipenv

```
pipenv install
pipenv run python3 src/cli.py -l PATH_TO_LIST_OF_NFTS.txt -o OUTPUT_DIR
```

## Python 3

```
pip3 install -r requirements.txt
python3 src/cli.py -l PATH_TO_LIST_OF_NFTS.txt -o OUTPUT_DIR
```

# Dev

You can use `pipenv` to create the dev environment.