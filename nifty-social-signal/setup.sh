#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
import nltk, ssl
try:
    _create=ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.download('vader_lexicon')
finally:
    ssl._create_default_https_context = _create
PY
echo "Setup complete."
