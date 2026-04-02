"""Flask web application for BASTION Cost Transparency Engine."""

from __future__ import annotations

import os

from flask import Flask, redirect, render_template, request, url_for

from .data.providers import MONITORING, EQUIPMENT, HIDDEN_FEES, PROVIDER_NAMES
from .engine.calculator import (
    true_monthly_cost,
    three_year_total,
    equipment_markup,
    equipment_cost,
    diy_total,
)
from .engine.etf import etf_timeline, optimal_exit_month
from .engine.comparison import compare_all


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "..", "static"),
    )
    app.secret_key = os.urandom(16)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            providers=MONITORING,
            provider_names=PROVIDER_NAMES,
        )

    @app.route("/builder")
    def builder():
        provider = request.args.get("provider", "")
        tier_str = request.args.get("tier", "")
        contract_str = request.args.get("contract", "")

        if not _validate_provider_tier_contract(provider, tier_str, contract_str):
            return redirect(url_for("index"))

        tier_index = int(tier_str)
        contract = int(contract_str)
        installation = request.args.get("installation", "diy")

        return render_template(
            "builder.html",
            provider=provider,
            provider_name=PROVIDER_NAMES[provider],
            tier_index=tier_index,
            tier=MONITORING[provider]["tiers"][tier_index],
            contract=contract,
            installation=installation,
            equipment=EQUIPMENT,
        )

    @app.route("/results")
    def results():
        provider = request.args.get("provider", "")
        tier_str = request.args.get("tier", "")
        contract_str = request.args.get("contract", "")

        if not _validate_provider_tier_contract(provider, tier_str, contract_str):
            return redirect(url_for("index"))

        tier_index = int(tier_str)
        contract = int(contract_str)
        installation = request.args.get("installation", "diy")
        financed = request.args.get("financed", "false") == "true"

        user_equipment = {}
        for device_key in EQUIPMENT:
            raw = request.args.get(device_key, "0")
            try:
                qty = max(0, min(99, int(raw)))
            except (ValueError, TypeError):
                qty = 0
            if qty > 0:
                user_equipment[device_key] = qty

        monthly = true_monthly_cost(provider, tier_index, user_equipment, financed=financed)
        total_3yr = three_year_total(provider, tier_index, contract, user_equipment, financed=financed)
        markup = equipment_markup(user_equipment, provider)
        diy = diy_total(user_equipment)
        comparison = compare_all(user_equipment)

        equip_total = equipment_cost(provider, user_equipment)
        timeline = etf_timeline(provider, tier_index, contract, equipment_total=equip_total)
        exit_month = optimal_exit_month(provider, tier_index, contract, equipment_total=equip_total)

        max_etf = max((t[1] for t in timeline), default=0)
        no_contract = contract == 0
        share_url = request.url

        return render_template(
            "results.html",
            provider=provider,
            provider_name=PROVIDER_NAMES[provider],
            tier_index=tier_index,
            tier=MONITORING[provider]["tiers"][tier_index],
            contract=contract,
            installation=installation,
            monthly=monthly,
            total_3yr=total_3yr,
            markup=markup,
            diy=diy,
            comparison=comparison,
            timeline=timeline,
            exit_month=exit_month,
            max_etf=max_etf,
            no_contract=no_contract,
            share_url=share_url,
            equipment=user_equipment,
            provider_names=PROVIDER_NAMES,
            cove_note="Cove doesn't call this an ETF, but if you financed equipment, this is what you'd owe to cancel.",
        )

    @app.route("/about")
    def about():
        return render_template("about.html")

    def _validate_provider_tier_contract(provider: str, tier_str: str, contract_str: str) -> bool:
        if provider not in MONITORING:
            return False
        try:
            tier_index = int(tier_str)
        except (ValueError, TypeError):
            return False
        if tier_index < 0 or tier_index >= len(MONITORING[provider]["tiers"]):
            return False
        try:
            contract = int(contract_str)
        except (ValueError, TypeError):
            return False
        if contract not in MONITORING[provider]["contract_months"]:
            return False
        return True

    return app
