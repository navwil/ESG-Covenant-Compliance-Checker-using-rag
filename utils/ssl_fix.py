import os
import httpx

# ---------------------------------------------------------------------------
# Tiktoken local cache setup (avoid SSL errors in TCS GenAI Lab)
# ---------------------------------------------------------------------------
TIKTOKEN_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tiktoken_cache"
)
os.environ["TIKTOKEN_CACHE_DIR"] = TIKTOKEN_CACHE_DIR

_cache_file = os.path.join(TIKTOKEN_CACHE_DIR, "9b5ad71b2ce5302211f9c61530b329a4922fc6a4")
if os.path.exists(_cache_file):
    pass  # cache is valid
else:
    print(f"WARNING: tiktoken cache not found at {_cache_file}")

# ---------------------------------------------------------------------------
# httpx client with SSL verification disabled (TCS GenAI Lab requirement)
# ---------------------------------------------------------------------------
http_client = httpx.Client(verify=False)
