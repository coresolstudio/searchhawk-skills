#!/usr/bin/env bash
# SearchHawk Skills — package skills as upload-ready zips (Claude.ai "Upload skill" format).
#
# Each zip contains a single top-level folder with SKILL.md inside it.
# Connector scripts referenced by a skill are bundled into the zip so it is
# self-contained on hosts without repo access.
#
# Usage:
#   ./package.sh                  # package all 25 skills into dist/
#   ./package.sh site-search-audit  # package one skill
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="${REPO_ROOT}/dist"
CONNECTORS_DIR="${REPO_ROOT}/scripts/connectors"
ONLY="${1:-}"
COUNT=0

package_skill() {
  local src="$1"
  local name
  name="$(basename "$src")"
  [[ -f "${src}/SKILL.md" ]] || return 0
  [[ -n "${ONLY}" && "${name}" != "${ONLY}" ]] && return 0

  local stage="${DIST}/.stage"
  rm -rf "${stage}"
  mkdir -p "${stage}"
  cp -R "${src}" "${stage}/${name}"

  # Bundle any connector scripts the skill references so the zip is self-contained.
  local bundled=""
  while IFS= read -r script; do
    if [[ -f "${CONNECTORS_DIR}/${script}" ]]; then
      mkdir -p "${stage}/${name}/scripts/connectors"
      cp "${CONNECTORS_DIR}/${script}" "${stage}/${name}/scripts/connectors/"
      bundled="${bundled} ${script}"
    fi
  done < <(grep -rhoE 'connectors/[a-z_]+\.py' "${src}" 2>/dev/null | sed 's|connectors/||' | sort -u)

  (cd "${stage}" && zip -rq "${DIST}/${name}.zip" "${name}" -x "*.DS_Store")
  rm -rf "${stage}"
  COUNT=$((COUNT + 1))
  if [[ -n "${bundled}" ]]; then
    echo "  ✓ ${name}.zip (+${bundled# })"
  else
    echo "  ✓ ${name}.zip"
  fi
}

echo "SearchHawk Skills — packaging upload-ready zips"
echo ""
mkdir -p "${DIST}"
if [[ -z "${ONLY}" ]]; then
  rm -f "${DIST}"/*.zip
else
  rm -f "${DIST}/${ONLY}.zip"
fi

for layer in cross-cutting discover diagnose decide improve track protocol; do
  [[ -d "${REPO_ROOT}/${layer}" ]] || continue
  for skill in "${REPO_ROOT}/${layer}"/*/; do
    package_skill "${skill%/}"
  done
done

echo ""
if [[ ${COUNT} -eq 0 ]]; then
  echo "No skill matched '${ONLY}'." >&2
  exit 1
fi
echo "Packaged ${COUNT} zip(s) → ${DIST}/"
echo "Upload any zip via Claude → Settings → Capabilities → Skills → Upload skill."
