"""Bot の全コンポーネントから 'test' を含むものを検索"""
import importlib.util
import os, sys
_this_dir = os.path.dirname(os.path.abspath(__file__))

_auth_helper_path = os.path.join(_this_dir, "..", "..", "standard", "scripts", "auth_helper.py")
_auth_helper_spec = importlib.util.spec_from_file_location("copilot_studio_auth_helper", _auth_helper_path)
if _auth_helper_spec is None or _auth_helper_spec.loader is None:
    raise ImportError(f"auth_helper.py を読み込めません: {_auth_helper_path}")
_auth_helper = importlib.util.module_from_spec(_auth_helper_spec)
_auth_helper_spec.loader.exec_module(_auth_helper)
get_session = _auth_helper.get_session

s = get_session()
url = (os.getenv("DATAVERSE_URL") or "").rstrip("/")
bot_id = os.environ.get("BOT_ID", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

# 全コンポーネント
r = s.get(f"{url}/api/data/v9.2/botcomponents",
      params={"$filter": f"_parentbotid_value eq '{bot_id}'",
                  "$select": "botcomponentid,componenttype,schemaname,data,name"})
comps = r.json().get("value", [])
print(f"Total components: {len(comps)}")

for c in comps:
    data = c.get("data", "") or ""
    name = c.get("name", "") or ""
    has_test = "test" in data.lower() or "test" in name.lower()
    print(f"\nType={c['componenttype']} schema={c.get('schemaname','')} name={name[:60]}")
    if has_test:
        print("  *** CONTAINS 'test' ***")
    if data:
        print(f"  data[:200]: {data[:200]}")

# Also check bot record itself
print("\n--- Bot record ---")
r2 = s.get(f"{url}/api/data/v9.2/bots({bot_id})")
bot = r2.json()
for k, v in sorted(bot.items()):
    sv = str(v)
    if v is not None and not k.startswith("@") and not k.startswith("_"):
        if "test" in sv.lower():
            print(f"  {k}: {sv[:200]}")

# Check applicationmanifestinformation
ami = bot.get("applicationmanifestinformation", "")
if ami:
    print(f"\napplicationmanifestinformation:\n{ami[:500]}")
