"""GPT コンポーネントの先頭行を確認"""
import os, sys
_this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_this_dir, "..", "..", "standard", "scripts"))
from auth_helper import get_session

s = get_session()
url = os.getenv("DATAVERSE_URL").rstrip("/")
component_id = os.environ.get("BOTCOMPONENT_ID", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
r = s.get(f"{url}/api/data/v9.2/botcomponents({component_id})?$select=data")
data = r.json().get("data", "")
lines = data.split("\n")
print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines[:8]):
    print(f"  {i}: {line}")
