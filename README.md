# AI Money-Making Experiment — 30 Days

A **working, deliberately low-risk starter**, not a guaranteed income generator. It uses GitHub Actions to run daily, generates seven original generic printable worksheets, hosts a lightweight storefront with GitHub Pages, and logs each run.

## Important limitations
- **No automatic sales or marketing:** buyers must discover the products. Checkout is only a link until you set one up.
- The seven sample products are basic templates. **Review and improve them before listing for money.** They are examples, not commercially polished finished products.
- **No live AI API is included** so there are no surprise model charges. Agent-based research, content personalization, licensed design, marketplace integrations, and analytics would need additional development and permissions.
- GitHub Actions schedules are not continuously running agents, and may occasionally be delayed. No code runs 24/7.
- **Never paste API keys into source code.** Use GitHub Secrets or Variables as appropriate.

## Set up
1. Create an empty GitHub repo named `money-making-ai`. Set **Private** if you don't want code visible; GitHub Pages availability may depend on your account. For the easiest Pages setup, use Public. Do not put sensitive information in a public repository.
2. Upload the contents of this ZIP to the repo root (not the containing directory).
3. In `Settings → Pages`, choose **Deploy from a branch**, branch `main`, folder `/docs`. The first run generates that folder; run the workflow first if `/docs` is not yet selectable.
4. Under `Settings → Actions → General`, allow workflows and the permission to create commits if needed. Under **Actions**, run **30-day business experiment** manually once to test.
5. Open `data/today.txt` to see the daily checklist.
6. Create your own checkout page on Gumroad or another supported merchant. Add its URL as `Settings → Secrets and variables → Actions → Variables → CHECKOUT_URL`. A single universal checkout link is a temporary placeholder; proper purchase and fulfillment require individual products/links.
7. Set your own experiment start date in `.github/workflows/daily.yml` (`START_DATE`).
8. Connect a traffic analytics and payment platform separately and input verified numbers in `data/metrics.csv`.

## Tracking
`data/runs.csv` tracks actual runs only, not revenue. `data/metrics.csv` is for verified entries. Do not mix simulated values with real sales.

## Security, cost, and review
Set spending caps on external providers before connecting AI APIs. Don't send unsolicited mass email, post through unauthorized accounts, scrape prohibited content, or generate fake reviews. Human approval is appropriate for payments, public posts, and final product quality checks.
