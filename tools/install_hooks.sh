#!/bin/sh
# Install plant-dataset git hooks (.git/hooks is not tracked, so this reproduces them).
# Run from anywhere inside the repo.
set -e
ROOT="$(git rev-parse --show-toplevel)"
HOOK="$ROOT/.git/hooks/pre-commit"
cat > "$HOOK" <<'EOF'
#!/bin/sh
# plant-dataset pre-commit release-verify safety net.
# Blocks only on a regression (new gate violation on a changed crop, or a catalog
# drop). Fails open on error. Bypass with: git commit --no-verify
exec python3 "$(git rev-parse --show-toplevel)/tools/precommit_release_verify.py"
EOF
chmod +x "$HOOK"
echo "installed pre-commit hook -> $HOOK"
