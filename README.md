# BASTION Cost Engine

Find out what you're really paying for home security. True cost transparency across 7 providers — hidden fees, equipment markups, ETF escape timelines, and side-by-side comparisons. No sales pitch required.

Built on a decade of home security industry experience.

Part of the [BASTION](https://github.com/Pachacutie/BASTION) portfolio.

---

## Use It Online

No install needed. Open in your browser, pick your provider, build your system, see the truth:

**[bastion-cost-engine.onrender.com](https://bastion-cost-engine.onrender.com)**

No data stored. No accounts. No tracking. Your equipment choices live in the URL — close the tab, it's gone.

---

## Run It Locally (Complete Privacy)

For maximum privacy, install and run on your own computer. No network calls, no telemetry.

### Install

Requires Python 3.12+.

```bash
pip install bastion-cost-engine
```

### Launch the Web Interface

```bash
flask --app bastion_cost.web:create_app run
```

Opens the same interface — running entirely on your machine.

---

## What It Does

1. **Select your provider** — ADT, Vivint, Frontpoint, Ring, SimpliSafe, Abode, or Cove
2. **Pick your plan** — each provider's monitoring tiers with real pricing
3. **Build your system** — add sensors, cameras, locks, and devices with real-time pricing
4. **See the truth** — six sections of cost transparency

### Results Dashboard

| Section | What It Shows |
|---------|---------------|
| **True Monthly Cost** | Advertised rate + hidden recurring fees (service fees, cloud storage, guard response) that aren't on the pricing page |
| **3-Year Total Cost** | Equipment + monitoring + hidden fees vs. the same system DIY — and how much more you're paying |
| **Equipment Markup** | Provider price vs. generic retail equivalent for every device, with per-item and total markup percentage |
| **ETF Escape Timeline** | Cancellation cost at every point in your contract, with the optimal exit month where paying the ETF beats staying |
| **Provider Comparison** | All 7 providers + DIY side-by-side using your equipment profile |
| **Shareable Summary** | Permalink URL with your full results — no database, no account needed |

## Providers

| Provider | Plans | Contract Options | Hidden Fees Tracked |
|----------|-------|-----------------|-------------------|
| **Frontpoint** | Interactive, Ultimate | 12mo, month-to-month | Service fee |
| **ADT** | Secure, Smart, Complete | 36mo, 60mo | Service fee, guard response |
| **Ring** | Basic, Plus, Pro | Month-to-month | Cloud storage |
| **SimpliSafe** | Standard, Interactive, Fast Protect | Month-to-month | Cloud storage |
| **Vivint** | Smart Home, Smart Home Video | 60mo | Service fee |
| **Abode** | Standard, Pro | 12mo, month-to-month | — |
| **Cove** | Basic, Plus, Max | 36mo, 60mo, month-to-month | — |

## How It Works

All state lives in URL query parameters. No database, no sessions, no cookies. Every calculation runs server-side from curated pricing data:

1. Provider/plan/contract selection → URL params
2. Equipment builder → quantities added to URL params
3. Results page reads params, runs all calculations, renders the dashboard

Pricing data is sourced from provider websites, subscriber agreements, and industry review sites. Generic retail prices use the cheapest functionally equivalent device from major retailers (Amazon, Home Depot).

No AI, no cloud APIs. Pure arithmetic against curated data.

## Development

```bash
git clone https://github.com/Pachacutie/bastion-cost-engine.git
cd bastion-cost-engine
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev,web]"
pytest -v
```

### Run the Dev Server

```bash
flask --app bastion_cost.web:create_app run --debug
```

## Contributing

Prices change. Providers run promotions. If you find outdated pricing:

- [Report outdated pricing](https://github.com/Pachacutie/bastion-cost-engine/issues/new?title=Outdated+pricing:+[Provider])
- [Request a new provider](https://github.com/Pachacutie/bastion-cost-engine/issues/new?title=New+provider:+[Name])

PRs welcome. Provider data lives in `src/bastion_cost/data/providers.py`. DIY equivalents in `src/bastion_cost/data/diy.py`.

## License

MIT
