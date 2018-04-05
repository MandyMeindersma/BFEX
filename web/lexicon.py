import sys
import json
lines = [line.strip('\r\n').lower().strip() for line in sys.stdin]

obj = {
    "data": lines
}

print(json.dumps(obj))
