"""Rank three business models for a low-cost 30-day experiment.

Transparent decision aid; not market research, live sales data, or a revenue forecast.
No paid APIs, scraping, messages, financial transactions or external actions.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
WEIGHTS = {
    "upfront_cost": .25,
    "automation_fit": .20,
    "launch_speed": .15,
    "maintenance_ease": .10,
    "observed_demand": .30,
}
SIGNAL_SCORES = {
    "customer_interview": .5,
    "waitlist_signup": 1.,
    "qualified_inquiry": 1.5,
    "paid_order": 5.,
}
MODEL_IDS = {"digital_products", "ai_services", "software_saas"}


def parse_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(config.get("models"), list):
        raise ValueError("Config must contain a models list")
    models = config["models"]
    if len(models) != 3 or {m["id"] for m in models} != MODEL_IDS:
        raise ValueError("All three designated business models required")
    for model in models:
        for key in ("upfront_cost", "automation_fit", "launch_speed", "maintenance_ease"):
            value = model["assumptions"].get(key)
            if type(value) not in (int, float) or not 0 <= value <= 5:
                raise ValueError("Assumption scores must be between 0 and 5")
        if not model.get("pricing_sources"):
            raise ValueError("Official pricing references required")
    return config


def parse_signals(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []  # No data is not proof of zero sales.
    signals = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(signals, list):
        raise ValueError("Signals must be a JSON array")
    for s in signals:
        if not isinstance(s, dict) or s.get("model") not in MODEL_IDS:
            raise ValueError("Unknown model in signal")
        if s.get("kind") not in SIGNAL_SCORES:
            raise ValueError("Unknown signal type")
        if not isinstance(s.get("source"), str) or not s["source"].strip():
            raise ValueError("Traceable source or internal record ID required")
        if not isinstance(s.get("observed_at"), str):
            raise ValueError("Signal date required")
        date.fromisoformat(s["observed_at"])
    return signals


def evaluate(config: dict[str, Any], signals: list[dict[str, Any]]) -> dict[str, Any]:
    ranking = []
    for model in config["models"]:
        observed = [s for s in signals if s["model"] == model["id"]]
        demand = min(5., sum(SIGNAL_SCORES[s["kind"]] for s in observed))
        factors = {**model["assumptions"], "observed_demand": demand}
        score = round(20 * sum(WEIGHTS[k] * factors[k] for k in WEIGHTS), 1)
        ranking.append({
            "id": model["id"],
            "name": model["name"],
            "heuristic_score_out_of_100": score,
            "assumptions": model["assumptions"],
            "user_reported_demand_signals": len(observed),
            "user_reported_demand_score": demand,
            "pricing_sources": model["pricing_sources"],
            "main_risk": model["main_risk"],
            "first_test": model["first_test"],
        })
    ranking.sort(key=lambda r: (-r["heuristic_score_out_of_100"], r["id"]))
    first = ranking[0]
    return {
        "generated_on": date.today().isoformat(),
        "selection": first["id"],
        "selection_name": first["name"],
        "selection_status": "provisional_experiment_choice",
        "verified_revenue": None,
        "not_a_sales_forecast": True,
        "scores": ranking,
        "method": "Judgment-based heuristic: upfront cost 25%, automation fit 20%, speed 15%, maintenance 10%, manually entered demand 30%. Not an empirical market model.",
        "limitations": [
            "No verified customer demand or revenue is available automatically.",
            "Manually entered signals are not independently authenticated.",
            "No posting, customer contact, spending, checkout setup or payment access.",
            "A provisional selection is not proof anything will sell.",
        ],
        "next_action": first["first_test"],
    }


def report_md(r: dict[str, Any]) -> str:
    lines = [
        "# 30-day business-model evaluation",
        "",
        f"Generated: {r['generated_on']}",
        "",
        f"**Provisional test choice: {r['selection_name']}**",
        "",
        "This ranks models for a cheap pilot, NOT validated product demand or guaranteed income.",
        "",
        "| Model | Heuristic score | User-entered signals | Biggest risk |",
        "|---|---:|---:|---|",
    ]
    for item in r["scores"]:
        lines.append(f"| {item['name']} | {item['heuristic_score_out_of_100']}/100 | {item['user_reported_demand_signals']} | {item['main_risk']} |")
    lines += ["", f"**First test:** {r['next_action']}", "", "**Method:** " + r["method"], "", "**Limits:**"]
    lines += ["- " + item for item in r["limitations"]]
    lines += ["", "**Official pricing references:**"]
    for item in r["scores"]:
        for source in item["pricing_sources"]:
            lines.append(f"- {item['name']}: [{source['label']}]({source['url']})")
    lines += ["", "**Sales and profit: unavailable until a payment provider is connected and real transactions are reconciled.**", ""]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=HERE / "models.json")
    p.add_argument("--signals", type=Path, default=HERE.parent / "data" / "opportunity_signals.json")
    p.add_argument("--out-json", type=Path, default=HERE.parent / "data" / "opportunity_decision.json")
    p.add_argument("--out-md", type=Path, default=HERE.parent / "data" / "opportunity_report.md")
    a = p.parse_args()
    result = evaluate(parse_config(a.config), parse_signals(a.signals))
    for file in (a.out_json, a.out_md):
        file.parent.mkdir(parents=True, exist_ok=True)
    a.out_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    a.out_md.write_text(report_md(result), encoding="utf-8")
    print(f"Provisional pilot: {result['selection_name']}")
    print(f"Report: {a.out_md}")


if __name__ == "__main__":
    main()
