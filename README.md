# docker-pdf-signer
A lightweight Dockerized CLI tool that adds an SVG signature to a PDF without local installations. Mount a folder, specify page, position, and scale, and the container embeds the signature as true vector graphics. Outputs a signed PDF with deterministic placement and full multi-page support.

## Usage

### Using the Pre-built Docker Image from Docker Hub

The easiest way to use docker-pdf-signer is to pull the pre-built image from Docker Hub:

```bash
docker pull jasdefer/docker-pdf-signer:latest
```

Then run the container with your PDF and signature files:

```bash
docker run --rm -v $(pwd):/work jasdefer/docker-pdf-signer:latest \
  --pdf test.pdf \
  --signature signature.svg \
  --page 1 \
  --rel-x 0.5 \
  --rel-y 0.1 \
  --scale 0.3
```

### Building Locally

If you prefer to build the Docker image yourself:

```bash
docker build -t docker-pdf-signer .
docker run --rm -v $(pwd):/work docker-pdf-signer \
  --pdf test.pdf \
  --signature signature.svg \
  --page 1 \
  --rel-x 0.5 \
  --rel-y 0.1 \
  --scale 0.3
```

## Arguments

- `--pdf`: Input PDF file (required)
- `--signature`: SVG signature file (default: signature.svg)
- `--page`: Page number to sign (1-based, required)
- `--scale`: Scale factor for the signature (required)
- `--x` / `--y`: Absolute coordinates in points
- `--rel-x` / `--rel-y`: Relative coordinates (0-1 range)
- `--output`: Custom output filename
- `--overwrite`: Overwrite the original PDF instead of creating a .signed.pdf file

## Docker Hub

Docker images are automatically published to Docker Hub when a new release is created. Available tags:
- `latest`: Latest stable release
- `x.y.z`: Specific version (e.g., 1.0.0)
- `x.y`: Minor version (e.g., 1.0)
- `x`: Major version (e.g., 1)

## Repository

https://github.com/jasdefer/docker-pdf-signer
