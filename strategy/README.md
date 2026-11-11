# Business-model comparison for the 30-day AI experiment

This is a **transparent, no-cost decision aid** for the existing money-making-ai project. It compares digital products, AI-assisted services, and software subscriptions. It does not open accounts, gather live customer data, create sales, publish messages, authorize spending, or guarantee profit.

## Run from the repository root

    python -m strategy.evaluate
    python -m unittest discover -s tests -p 'test_opportunity_evaluator.py'

The Python script creates:
- data/opportunity_decision.json (machine-readable choice)
- data/opportunity_report.md (human-readable reasoning with official sources)

It does **not** change the main product generator or overwrite files Copilot is currently editing. A separate GitHub Actions workflow can evaluate daily during November 11–December 10, 2026 when merged into main.

## How the decision is made

Heuristic weights: upfront cash 25%, automation suitability 20%, launch speed 15%, maintenance simplicity 10%, **documented demand signals 30%**.

Starting scores use explicit **judgment-based assumptions**, not factual demand metrics. Without demand evidence, digital products are the *provisional* cheapest and simplest test choice for the current repository. The model can change when real evidence arrives.

Default does not mean there are buyers. Do not waste a month generating low-quality repetitive templates. Test one useful product with real potential customers first.

## Feeding it actual evidence

Create data/opportunity_signals.json containing a JSON array. Example:

    [
      {
        "model": "ai_services",
        "kind": "qualified_inquiry",
        "observed_at": "2026-11-11",
        "source": "redacted-private-note-001"
      }
    ]

Allowed models: digital_products, ai_services, software_saas.
Allowed kinds: customer_interview, waitlist_signup, qualified_inquiry, paid_order.

Only add **genuine** source records (and DO NOT add private customer names, emails, payment IDs, addresses or secrets to your public GitHub repository). A record ID is not proof of an authenticated purchase. The evaluator deliberately reports verified sales and revenue as **unavailable** unless an authorized payment integration is separately implemented and reconciled.

For rigorous actual market comparison, gather two independent sources of demand for each proposed niche and log date, URL, customer problem, likely purchasing intent, competitor price and proof. These records can then guide a human or appropriately permitted agent to update this input. Model-generated guesses must never count as customer demand.

## Low-cost platform facts (checked Nov 11, 2026)

- Payhip offers a free plan with 5% platform fee per sale, plus independent payment-processing fees: https://payhip.com/pricing
- Upwork Basic starts at $0/month, but freelancer service fees are charged on earnings: https://www.upwork.com/pricing/freelancer
- Stripe standard online domestic card processing lists 2.9% + 30¢ and Payment Links without additional standard link fees: https://stripe.com/pricing
- Standard GitHub Actions hosted runners on public repositories are free: https://docs.github.com/en/billing/concepts/product-billing/github-actions

Fees can change. Free to start does not mean free to operate at higher volume.

## Before any business can earn money

1. Validate a real problem, build **one** excellent original product or service.
2. Review quality, claims, rights and functionality.
3. Set up a legitimate checkout and fulfillment flow with your explicit permission.
4. Make a truthful product page; seek **opt-in** buyers instead of spam.
5. Reconcile real purchases, fees and refunds; no fictional revenue.

The separate evaluation workflow is not a substitute for selling or marketing and does not activate the original product-creation workflow.
