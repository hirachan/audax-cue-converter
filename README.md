# audax-cue-converter

## What's this for?

This will help to create Audax Brevet cue sheet for each club format from Ride with GPS route data.
Now only have AR Nihonbashi format of cue sheet.

## How to use (CLI)

```console
usage: cue-convert [-h] [-o OUTPUT] ROUTE_ID [PRIVACY_CODE]
```

Example.
```console
cue-convert -o BRM523-2020.xlsx 30477783
```

## How to use (Docker)

Build container image.
```console
docker build -t audax-cue-converter .
```

Invoke in container.
Example.
```console
docker run -it --rm -v $(pwd)/output:/output audax-cue-converter -o /output/BRM523-2020.xlsx 30477783
```


## Deploy to AWS Lambda

Prepare for serverless framework and its plugins.
```
npm install -g serverless
npm install serverless-python-requirements
npm install serverless-apigw-binary
```

Deploy
```
cd src/audax_cue_converter
sls deploy
```
