#!/usr/bin/env bash
# SearchHawk Skills v2 installer
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURSOR_SKILLS="${HOME}/.cursor/skills"
CLAUDE_SKILLS="${HOME}/.claude/skills"
TARGET="${1:---cursor-only}"
COUNT=0

install_skill() {
  local src="$1"
  local name
  name="$(basename "$src")"
  [[ -f "${src}/SKILL.md" ]] || return
  mkdir -p "${CURSOR_SKILLS}"
  ln -sfn "${src}" "${CURSOR_SKILLS}/${name}"
  COUNT=$((COUNT + 1))
  echo "  ✓ ${name}"
  if [[ "${TARGET}" == "--all" ]]; then
    mkdir -p "${CLAUDE_SKILLS}"
    ln -sfn "${src}" "${CLAUDE_SKILLS}/${name}"
  fi
}

echo "SearchHawk Skills v2.3 — SEO · AEO · GEO for AI assistants"
echo ""

for layer in cross-cutting discover diagnose decide improve track protocol; do
  [[ -d "${REPO_ROOT}/${layer}" ]] || continue
  for skill in "${REPO_ROOT}/${layer}"/*/; do
    install_skill "${skill%/}"
  done
done

echo ""
echo "Installed ${COUNT} skills to ${CURSOR_SKILLS}"
