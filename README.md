# docker-pdf-signer

<p align="center">
  <img src="logo.svg" width="160" alt="Project Logo">
</p>

A lightweight Dockerized CLI tool that adds an SVG signature to a PDF without local installations. Mount a folder, specify page, position, and scale, and the container embeds the signature as true vector graphics. Outputs a signed PDF with deterministic placement and full multi-page support.

## Usage

Pull the pre-built image from Docker Hub or build it locally:

```bash
# Option 1: Pull from Docker Hub
docker pull jasdefer/docker-pdf-signer:latest

# Option 2: Build locally
docker build -t jasdefer/docker-pdf-signer .
```

Run the container with your PDF and signature files:

```bash
docker run --rm -v $(pwd):/work jasdefer/docker-pdf-signer:latest \
  --pdf test.pdf \
  --signature signature.svg \
  --page 1 \
  --rel-x 0.5 \
  --rel-y 0.1 \
  --scale 0.3
```

## Example

![Usage example](docker-pdf-signer.gif)

## Arguments

- `--pdf`: Input PDF file (required)
- `--signature`: SVG signature file (default: signature.svg)
- `--page`: Page number to sign (1-based, required)
- `--scale`: Scale factor for the signature size (required). Values <1 shrink the signature, values >1 increase its size
- `--x` / `--y`: Absolute coordinates in points for signature placement. `--x` controls horizontal position (left to right), `--y` controls vertical position (bottom to top). Larger values move the signature right and up
- `--rel-x` / `--rel-y`: Relative coordinates in the range 0-1 for signature placement. `--rel-x` controls horizontal position (0=left edge, 1=right edge), `--rel-y` controls vertical position (0=bottom edge, 1=top edge). Cannot be used together with `--x`/`--y`
- `--output`: Custom output filename. If not specified, creates a file with `.signed.pdf` suffix (e.g., `document.pdf` becomes `document.signed.pdf`)
- `--overwrite`: Overwrite the original PDF instead of creating a new file

## Docker Hub

Docker images are automatically published to Docker Hub when a new release is created. Available tags:
- `latest`: Latest stable release
- `x.y.z`: Specific version (e.g., 1.0.0)
- `x.y`: Minor version (e.g., 1.0)
- `x`: Major version (e.g., 1)

## Repository

https://github.com/jasdefer/docker-pdf-signer
