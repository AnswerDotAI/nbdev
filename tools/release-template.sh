#!/usr/bin/env bash
# Usage: ./tools/release-template.sh 1.1.7
set -e
cd "$(dirname "$0")/../../nbdev3-template"
git tag "$1"
git push origin "$1"
gh release create "$1" --title "v$1" --generate-notes
