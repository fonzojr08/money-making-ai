"""Low-cost, transparent digital-product experiment. No paid API required."""
from pathlib import Path
from datetime import date, datetime
import csv, html, json, os, random

ROOT = Path(__file__).parent
DATA = ROOT / 'data'
SITE = ROOT / 'docs'
DATA.mkdir(exist_ok=True)
SITE.mkdir(exist_ok=True)
IDEAS = [
    ('Weekly Meal Planner', 'A printable weekly meal plan and shopping list', 'meal-planning'),
    ('Small Business Order Tracker', 'A straightforward printable order and payment tracker', 'small-business'),
    ('Study Planner', 'A printable study schedule and assignment checklist', 'student-planning'),
    ('Household Cleaning Checklist', 'A room-by-room cleaning schedule', 'home-organization'),
    ('Monthly Budget Worksheet', 'A simple planning worksheet, not financial advice', 'budget-planning'),
    ('Fitness Habit Log', 'A printable habit tracker, not medical advice', 'fitness-planning'),
    ('Content Planning Calendar', 'A calendar for scheduling social posts', 'marketing-planning'),
]
START = date.fromisoformat(os.getenv('START_DATE', '2026-11-11'))
TODAY = date.today()
DAY = (TODAY - START).days + 1
MAX_DAYS = 30
PRICE = os.getenv('PRODUCT_PRICE', '7')
CHECKOUT = os.getenv('CHECKOUT_URL', '').strip()
BASE_URL = os.getenv('SITE_URL', '').rstrip('/')

def write_product(title, desc, slug):
    folder = ROOT / 'products' / slug
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'product.html'
    if path.exists():
        return path
    entries = ''.join(f'<tr><td>{i}</td><td style="height:36px;border-bottom:1px solid #ddd"></td><td style="border-bottom:1px solid #ddd"></td></tr>' for i in range(1, 15))
    path.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>body{{font-family:Arial;max-width:850px;margin:45px auto;color:#222}}h1{{color:#25335c}}table{{width:100%;border-collapse:collapse}}th{{text-align:left;background:#eee;padding:12px}}@media print{{button{{display:none}}}}</style></head><body><h1>{html.escape(title)}</h1><p>{html.escape(desc)}</p><p>Month/Week: __________________ Name: __________________</p><table><thead><tr><th>#</th><th>Plan / Task</th><th>Done / Notes</th></tr></thead><tbody>{entries}</tbody></table><p>Reflection / Next steps:</p><p>____________________________________________________________________</p><button onclick="window.print()">Print / Save as PDF</button></body></html>''', encoding='utf-8')
    return path

def build_site():
    cards = []
    for title, desc, slug in IDEAS:
        path = write_product(title, desc, slug)
        # Products remain freely previewable; no false claims of paid fulfillment.
        checkout = f'<a class="button" href="{html.escape(CHECKOUT, quote=True)}" rel="noopener">Visit checkout</a>' if CHECKOUT else '<span class="notice">Checkout not connected yet</span>'
        cards.append(f'<article><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p><p>Suggested price: ${html.escape(PRICE)}</p><a href="../products/{slug}/product.html">Preview printable</a> {checkout}</article>')
    (SITE / 'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Useful Printable Tools</title><style>body{font:16px system-ui;background:#f5f6fa;color:#202538;margin:0}header{padding:45px 20px;text-align:center;background:#202c51;color:white}main{max-width:1020px;margin:28px auto;padding:0 18px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}article{padding:24px;background:white;border-radius:12px;box-shadow:0 4px 20px #141c3020}a{color:#425ec7}.button{display:inline-block;background:#202c51;color:white;padding:10px;margin:10px 0;border-radius:6px;text-decoration:none}.notice{font-size:13px;color:#854d0e}footer{text-align:center;padding:25px;color:#555}</style></head><body><header><h1>Useful Printable Tools</h1><p>Simple worksheets to make everyday planning easier.</p></header><main>''' + ''.join(cards) + '''</main><footer>Digital downloads • Review all products before charging customers</footer></body></html>''', encoding='utf-8')
    # Relative product previews must live under served site root
    for _, _, slug in IDEAS:
        source = ROOT / 'products' / slug / 'product.html'
        dest = SITE / 'products' / slug / 'product.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
    p = SITE / 'index.html'
    p.write_text(p.read_text(encoding='utf-8').replace('../products/', 'products/'), encoding='utf-8')

def daily_experiment():
    build_site()
    report_file = DATA / 'runs.csv'
    if DAY < 1 or DAY > MAX_DAYS:
        print(f'Day {DAY}: outside 30-day window; no new activity.')
        return
    exists = report_file.exists()
    with report_file.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not exists: writer.writerow(['run_utc', 'day', 'products', 'checkout_configured', 'sales_source'])
        writer.writerow([datetime.utcnow().isoformat()+'Z', DAY, len(IDEAS), bool(CHECKOUT), 'not connected'])
    prompt = f'''DAY {DAY} / 30 — TASK LIST\n1. Review one product for accuracy and usefulness.\n2. Validate demand with real people; avoid invented research claims.\n3. Share one genuinely useful post only through an authorized channel.\n4. Check storefront analytics and actual payment provider sales.\n5. Record traffic, costs, and sales in data/metrics.csv.\n6. Never claim a sale unless verified by your payment provider.\n'''
    (DATA / 'today.txt').write_text(prompt, encoding='utf-8')
    print(prompt)

if __name__ == '__main__':
    daily_experiment()
