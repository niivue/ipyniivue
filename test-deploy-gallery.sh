#!/usr/bin/env bash
set -euo pipefail

echo "=== 0. sanity: node/npm available? ==="
if ! command -v node >/dev/null 2>&1; then
  echo "node not found — please install node/npm"
  exit 1
fi

echo "=== 1. install node deps (Playwright, cross-env, etc.) ==="
# prefer CI-style reproducible install if you commit lockfile
if [ -f package-lock.json ] || [ -f pnpm-lock.yaml ] || [ -f yarn.lock ]; then
  echo "Installing node deps (using npm ci)..."
  npm ci
else
  echo "No lockfile found — running npm install"
  npm install
fi

# If your gallery generator uses Playwright: ensure browsers installed.
if [ -d node_modules/playwright ] || [ -f node_modules/playwright/package.json ]; then
  echo "Installing Playwright browsers (if not present)..."
  # try with deps first (helpful on CI), fallback if not supported
  npx playwright install --with-deps || npx playwright install || true
fi

echo "=== 2. ensure python tooling and Hatch are available (system) ==="
python -m pip install --upgrade pip
python -m pip install --upgrade hatch || true

echo "=== 3. create Hatch env (or ensure it exists) ==="
# hatch env create will not clobber an existing env
hatch env create

echo "=== 4. ensure nbconvert exists inside the Hatch env ==="
# prefer the hatch-provided python so nbconvert is used inside that env
HATCH_PYTHON="$(hatch run python -c 'import sys;print(sys.executable)')"
echo "Resolved Hatch python: $HATCH_PYTHON"

# If nbconvert is missing inside the hatch env, install it there
if ! "$HATCH_PYTHON" -m pip show nbconvert >/dev/null 2>&1; then
  echo "Installing nbconvert into Hatch env..."
  "$HATCH_PYTHON" -m pip install nbconvert
fi

# optionally ensure pandoc (some nbconvert conversions can use it)
if ! command -v pandoc >/dev/null 2>&1; then
  echo "Warning: pandoc not found on system. Some nbconvert features may require pandoc."
  echo "If you want to install pandoc, run (mac): brew install pandoc  or (ubuntu): sudo apt-get install -y pandoc"
fi

echo "=== 5. Generate docs/gallery (HTML outputs) using Hatch python ==="
# Ensure gallery generator sees the Hatch python. Your package.json script reads process.env.PYTHON.
# NOTE: npm run will use local node; we already ran npm ci above.
PYTHON="$HATCH_PYTHON" npm run gallery:html

echo "=== 6. Build Sphinx docs with Hatch (same as CI) ==="
hatch run docs

echo "=== 7. mirror the generated gallery into the built docs ==="
SRC="docs/gallery"                    # where generator wrote files
DEST="docs/build/html/gallery"
mkdir -p "$DEST"

if [ -d "$SRC" ]; then
  # By default preserve Sphinx's gallery/index.html (the iframe wrapper). Remove --exclude 'index.html' if you want to overwrite it.
  rsync -av --delete --exclude 'index.html' "$SRC"/ "$DEST"/

  # Move any stray generated html accidentally placed at docs/build/html root into the gallery folder
  for f in "$SRC"/*.html; do
    [ -e "$f" ] || continue
    bn=$(basename "$f")
    if [ -f "docs/build/html/$bn" ] && [ ! -f "$DEST/$bn" ]; then
      echo "Moving stray $bn into gallery folder"
      mv -v "docs/build/html/$bn" "$DEST/$bn"
    fi
  done
else
  echo "Gallery source ($SRC) not found — skipping mirror."
fi

echo "=== 8. inject the Gallery link into docs/build/html/index.html if missing ==="
INDEX="docs/build/html/index.html"
if [ -f "$INDEX" ]; then
  if ! grep -q 'href="gallery/' "$INDEX"; then
    echo "Injecting Gallery link into $INDEX"
    awk '
      BEGIN { inserted = 0 }
      {
        print
        if (!inserted && $0 ~ /<body[^>]*>/) {
          print "  <p style=\"margin: 1em 0;\"><a href=\"gallery/\">📷 Notebook Gallery</a></p>"
          inserted = 1
        }
      }
    ' "$INDEX" > "${INDEX}.tmp" && mv "${INDEX}.tmp" "$INDEX"
  else
    echo "Gallery link already present."
  fi
else
  echo "Index file missing at $INDEX — build probably failed"
  exit 1
fi

echo "=== 9. Serve locally at http://localhost:8000 ==="
echo "Open http://localhost:8000 to inspect the homepage and /gallery/."
python -m http.server --directory docs/build/html 8000
