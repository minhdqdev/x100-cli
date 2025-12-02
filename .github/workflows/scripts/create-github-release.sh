#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  .genreleases/x100-template-copilot-sh-"$VERSION".zip \
  .genreleases/x100-template-copilot-ps-"$VERSION".zip \
  .genreleases/x100-template-claude-sh-"$VERSION".zip \
  .genreleases/x100-template-claude-ps-"$VERSION".zip \
  .genreleases/x100-template-gemini-sh-"$VERSION".zip \
  .genreleases/x100-template-gemini-ps-"$VERSION".zip \
  .genreleases/x100-template-cursor-agent-sh-"$VERSION".zip \
  .genreleases/x100-template-cursor-agent-ps-"$VERSION".zip \
  .genreleases/x100-template-opencode-sh-"$VERSION".zip \
  .genreleases/x100-template-opencode-ps-"$VERSION".zip \
  .genreleases/x100-template-qwen-sh-"$VERSION".zip \
  .genreleases/x100-template-qwen-ps-"$VERSION".zip \
  .genreleases/x100-template-windsurf-sh-"$VERSION".zip \
  .genreleases/x100-template-windsurf-ps-"$VERSION".zip \
  .genreleases/x100-template-codex-sh-"$VERSION".zip \
  .genreleases/x100-template-codex-ps-"$VERSION".zip \
  .genreleases/x100-template-kilocode-sh-"$VERSION".zip \
  .genreleases/x100-template-kilocode-ps-"$VERSION".zip \
  .genreleases/x100-template-auggie-sh-"$VERSION".zip \
  .genreleases/x100-template-auggie-ps-"$VERSION".zip \
  .genreleases/x100-template-roo-sh-"$VERSION".zip \
  .genreleases/x100-template-roo-ps-"$VERSION".zip \
  .genreleases/x100-template-codebuddy-sh-"$VERSION".zip \
  .genreleases/x100-template-codebuddy-ps-"$VERSION".zip \
  .genreleases/x100-template-amp-sh-"$VERSION".zip \
  .genreleases/x100-template-amp-ps-"$VERSION".zip \
  .genreleases/x100-template-shai-sh-"$VERSION".zip \
  .genreleases/x100-template-shai-ps-"$VERSION".zip \
  .genreleases/x100-template-q-sh-"$VERSION".zip \
  .genreleases/x100-template-q-ps-"$VERSION".zip \
  .genreleases/x100-template-bob-sh-"$VERSION".zip \
  .genreleases/x100-template-bob-ps-"$VERSION".zip \
  --title "x100 Templates - $VERSION_NO_V" \
  --notes-file release_notes.md
