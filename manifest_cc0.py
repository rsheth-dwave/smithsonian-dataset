# e.g., python manifest_cc0.py metadata/edan/nasm/ > nasm_urls.txt

import json, os, sys
from urllib.parse import urlparse, parse_qs

ALLOWED = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

def iter_jsonl_paths(p):
    if os.path.isdir(p):
        for root, _, files in os.walk(p):
            for fn in files:
                if fn.endswith(".txt") and fn != "index.txt":
                    yield os.path.join(root, fn)
    else:
        yield p

def pick_urls(m):
    # prefer explicit downloadable resources (often include ext)
    out = []
    for res in (m.get("resources") or []):
        u = res.get("url")
        if u and u.lower().endswith(ALLOWED):
            out.append(u)
        elif u:
            # sometimes extension is only in ?id=
            qid = parse_qs(urlparse(u).query).get("id", [""])[0].lower()
            if qid.endswith(ALLOWED):
                out.append(u)
    return out

for inp in sys.argv[1:]:
    for fp in iter_jsonl_paths(inp):
        with open(fp, "rt", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                r = json.loads(line)
                dn = r.get("content", {}).get("descriptiveNonRepeating", {})
                rec_guid = dn.get("guid") or r.get("content", {}).get("guid") or r.get("guid") or ""
                rec_id   = dn.get("record_ID") or r.get("content", {}).get("record_id") or r.get("id") or ""
                media = (dn.get("online_media", {}) or {}).get("media", []) or []
                for m in media:
                    access = str((m.get("usage") or {}).get("access", ""))
                    if "CC0" not in access.upper(): 
                        continue
                    idsid = m.get("idsId") or ""
                    urls = pick_urls(m)
                    if urls:
                        for u in urls:
                            print(f"{rec_guid}\t{rec_id}\t{idsid}\t{access}\t{u}")
                    elif idsid:
                        print(f"{rec_guid}\t{rec_id}\t{idsid}\t{access}\thttps://ids.si.edu/ids/download?id={idsid}")

