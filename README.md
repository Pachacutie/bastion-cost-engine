# BASTION Cost Engine

**Find out what you're really paying for home security.**

A browser-based calculator that shows the true cost of home security — including hidden fees, equipment markups, and what you'd save going DIY.

## What It Does

1. **Select your provider** — ADT, Vivint, Frontpoint, Ring, SimpliSafe, Abode, or Cove
2. **Build your system** — add sensors, cameras, and devices with real-time pricing
3. **See the truth** — true monthly cost, 3-year total, equipment markups, ETF timeline, and side-by-side comparison

## What It Shows

- **True Monthly Cost** — advertised rate + hidden recurring fees
- **3-Year Total** — equipment + monitoring + hidden fees vs. DIY alternative
- **Equipment Markup** — provider price vs. generic retail equivalents
- **ETF Escape Timeline** — cancellation cost at every point in your contract
- **Provider Comparison** — all 7 providers + DIY for your equipment profile
- **Shareable Summary** — share the numbers with friends

## Try It

Live at [bastion-cost-engine.onrender.com](https://bastion-cost-engine.onrender.com)

## Run Locally

    pip install -e ".[web]"
    flask --app bastion_cost.web:create_app run --debug

## Run Tests

    pip install -e ".[dev,web]"
    pytest -v

## About the Data

Pricing sourced from provider websites, subscriber agreements, and industry review sites as of April 2026. [Report outdated pricing](https://github.com/Pachacutie/bastion-cost-engine/issues/new?title=Outdated+pricing:+[Provider]).

## Part of BASTION

An open-source portfolio of tools that make the home security industry's information asymmetry visible. See [BASTION](https://github.com/Pachacutie/BASTION) for all tools.

## License

MIT
