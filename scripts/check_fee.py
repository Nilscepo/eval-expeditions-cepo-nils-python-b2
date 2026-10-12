import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rules import shipping_fee

print(shipping_fee(500))
print(shipping_fee(501))
print(shipping_fee(2000))