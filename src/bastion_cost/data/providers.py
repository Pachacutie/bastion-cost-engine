"""Provider pricing data for home security cost calculations.

Sources: Provider websites, subscriber agreements, industry review sites.
Data as of April 2026.
"""

MONITORING = {
    "frontpoint": {
        "tiers": [
            {"name": "Standard", "monthly": 34.99, "features": ["24/7 monitoring", "cellular", "app control"]},
            {"name": "Premium", "monthly": 49.99, "features": ["24/7 monitoring", "cellular", "app control", "video", "smart home"]},
        ],
        "contract_months": [12, 36],
        "etf_formula": "remaining_months * monthly_rate * 0.80",
        "etf_description": "80% of remaining monthly charges",
    },
    "adt": {
        "tiers": [
            {"name": "Secure", "monthly": 24.99, "features": ["24/7 monitoring", "cellular"]},
            {"name": "Smart", "monthly": 29.99, "features": ["24/7 monitoring", "cellular", "smart home"]},
            {"name": "Complete", "monthly": 39.99, "features": ["24/7 monitoring", "cellular", "smart home", "video"]},
            {"name": "Complete + Video", "monthly": 49.99, "features": ["24/7 monitoring", "cellular", "smart home", "video", "cloud storage"]},
        ],
        "contract_months": [36],
        "etf_formula": "remaining_months * monthly_rate * 0.75",
        "etf_description": "75% of remaining monthly charges + equipment financing balance",
    },
    "ring": {
        "tiers": [
            {"name": "Basic (free)", "monthly": 0, "features": ["live view", "app alerts"]},
            {"name": "Solo", "monthly": 4.99, "features": ["1 device recording", "person detection"]},
            {"name": "Multi", "monthly": 9.99, "features": ["all devices", "cellular backup", "recording", "extended warranty"]},
            {"name": "AI Pro", "monthly": 19.99, "features": ["all Multi features", "24/7 pro monitoring", "AI detection"]},
        ],
        "contract_months": [0],
        "etf_formula": "0",
        "etf_description": "No contract. No ETF. Cancel anytime.",
    },
    "simplisafe": {
        "tiers": [
            {"name": "Free (local siren)", "monthly": 0, "features": ["local siren", "no app"]},
            {"name": "Self-Monitor", "monthly": 9.99, "features": ["app alerts", "camera recording"]},
            {"name": "Standard", "monthly": 22.99, "features": ["24/7 monitoring", "cellular", "dispatch"]},
            {"name": "Core", "monthly": 32.99, "features": ["Standard + video verification"]},
            {"name": "Pro Plus", "monthly": 79.99, "features": ["Core + 24/7 live agent Active Guard"]},
        ],
        "contract_months": [0],
        "etf_formula": "0",
        "etf_description": "No contract. No ETF. Cancel anytime.",
    },
    "vivint": {
        "tiers": [
            {"name": "Smart Security", "monthly": 24.99, "features": ["24/7 monitoring", "smart home"]},
            {"name": "Smart Home", "monthly": 39.99, "features": ["monitoring", "smart home", "cameras (limited)"]},
            {"name": "Smart Home Video", "monthly": 44.99, "features": ["monitoring", "smart home", "full video", "storage"]},
            {"name": "Premium", "monthly": 57.00, "features": ["all features", "premium support"]},
        ],
        "contract_months": [42, 60],
        "etf_formula": "equipment_balance + (300 if months_elapsed < 12 else 150)",
        "etf_description": "Remaining equipment balance + $300 penalty (year 1) or $150 (after year 1)",
    },
    "abode": {
        "tiers": [
            {"name": "Free", "monthly": 0, "features": ["smart home integration", "app control", "live view"]},
            {"name": "Standard", "monthly": 8.49, "features": ["Free + 10-day timeline", "automation"]},
            {"name": "Pro", "monthly": 26.99, "features": ["Standard + 24/7 monitoring", "cellular"]},
        ],
        "contract_months": [0],
        "etf_formula": "0",
        "etf_description": "No contract. $35 fee only if returning plan with financed equipment.",
    },
    "cove": {
        "tiers": [
            {"name": "Basic", "monthly": 19.99, "features": ["24/7 monitoring", "cellular"]},
            {"name": "Plus", "monthly": 29.99, "features": ["Basic + video", "smart home", "lifetime warranty"]},
        ],
        "contract_months": [0, 36],
        "etf_formula": "equipment_retail_value if financed else 0",
        "etf_description": "No ETF if equipment paid upfront. Full retail value of equipment if financed.",
    },
}

EQUIPMENT = {
    "door_window_sensor": {
        "category": "Entry Sensors",
        "generic_retail": 8,
        "generic_name": "Sonoff SNZB-04 Zigbee",
        "providers": {
            "frontpoint": 34.99, "adt": 40.00, "ring": 25.00,
            "simplisafe": 15.99, "vivint": 50.00, "abode": 29.99, "cove": 15.00,
        },
    },
    "motion_sensor": {
        "category": "Motion Sensors",
        "generic_retail": 10,
        "generic_name": "Sonoff SNZB-03 Zigbee",
        "providers": {
            "frontpoint": 74.99, "adt": 30.00, "ring": 35.00,
            "simplisafe": 34.99, "vivint": 50.00, "abode": 39.99, "cove": 50.00,
        },
    },
    "glass_break_sensor": {
        "category": "Glass Break Sensors",
        "generic_retail": 20,
        "generic_name": "Honeywell FG1625 (Z-Wave)",
        "providers": {
            "frontpoint": 99.99, "adt": 50.00, "ring": 39.99,
            "simplisafe": 39.99, "vivint": 50.00, "abode": 44.99, "cove": 50.00,
        },
    },
    "smoke_sensor": {
        "category": "Environmental",
        "generic_retail": 40,
        "generic_name": "First Alert ZCOMBO-G (Z-Wave)",
        "providers": {
            "frontpoint": 79.99, "adt": 60.00, "ring": 39.99,
            "simplisafe": 44.99, "vivint": 100.00, "abode": 49.99, "cove": 95.00,
        },
    },
    "co_sensor": {
        "category": "Environmental",
        "generic_retail": 40,
        "generic_name": "First Alert ZCOMBO-G (combo)",
        "providers": {
            "frontpoint": 99.99, "adt": 60.00, "ring": 39.99,
            "simplisafe": 69.99, "vivint": 100.00, "abode": None, "cove": 125.00,
        },
    },
    "indoor_camera": {
        "category": "Cameras",
        "generic_retail": 20,
        "generic_name": "Wyze Cam OG",
        "providers": {
            "frontpoint": None, "adt": 149.99, "ring": 44.99,
            "simplisafe": 149.99, "vivint": 200.00, "abode": 59.99, "cove": 80.00,
        },
    },
    "outdoor_camera": {
        "category": "Cameras",
        "generic_retail": 40,
        "generic_name": "Wyze Cam v4 (outdoor kit)",
        "providers": {
            "frontpoint": None, "adt": 179.99, "ring": 99.99,
            "simplisafe": 199.99, "vivint": 400.00, "abode": 259.00, "cove": 160.00,
        },
    },
    "video_doorbell": {
        "category": "Cameras",
        "generic_retail": 50,
        "generic_name": "Wyze Video Doorbell v2",
        "providers": {
            "frontpoint": None, "adt": 179.99, "ring": 99.99,
            "simplisafe": 169.00, "vivint": 250.00, "abode": 119.99, "cove": 100.00,
        },
    },
    "smart_lock": {
        "category": "Access Control",
        "generic_retail": 120,
        "generic_name": "Schlage Encode Plus",
        "providers": {
            "frontpoint": None, "adt": None, "ring": None,
            "simplisafe": 119.99, "vivint": 180.00, "abode": 159.99, "cove": None,
        },
    },
    "keypad": {
        "category": "Access Control",
        "generic_retail": 30,
        "generic_name": "Ring Alarm Keypad (generic equiv)",
        "providers": {
            "frontpoint": 54.99, "adt": None, "ring": 37.49,
            "simplisafe": 69.99, "vivint": None, "abode": 89.99, "cove": 150.00,
        },
    },
    "hub_base": {
        "category": "Hub / Base Station",
        "generic_retail": 80,
        "generic_name": "Hubitat Elevation C-8",
        "providers": {
            "frontpoint": 269.99, "adt": 269.00, "ring": 149.99,
            "simplisafe": 199.98, "vivint": None, "abode": 199.00, "cove": 150.00,
        },
    },
    "water_sensor": {
        "category": "Environmental",
        "generic_retail": 8,
        "generic_name": "Govee WiFi Water Sensor",
        "providers": {
            "frontpoint": None, "adt": 60.00, "ring": 39.99,
            "simplisafe": 19.99, "vivint": 50.00, "abode": 49.99, "cove": 125.00,
        },
    },
    "panic_button": {
        "category": "Other",
        "generic_retail": 15,
        "generic_name": "Generic Z-Wave panic button",
        "providers": {
            "frontpoint": None, "adt": None, "ring": 29.99,
            "simplisafe": 19.99, "vivint": 50.00, "abode": 24.99, "cove": 30.00,
        },
    },
    "key_fob": {
        "category": "Access Control",
        "generic_retail": 15,
        "generic_name": "Generic Z-Wave key fob",
        "providers": {
            "frontpoint": None, "adt": None, "ring": None,
            "simplisafe": 24.99, "vivint": 50.00, "abode": 19.99, "cove": 30.00,
        },
    },
}

HIDDEN_FEES = {
    "frontpoint": {
        "activation": 0, "installation": 0, "cellular_monthly": 0,
        "notes": "No hidden fees. Equipment markup is the primary cost driver.",
    },
    "adt": {
        "activation": 99, "installation": 149, "cellular_monthly": 0,
        "service_call": 99, "guard_response_monthly": 8, "permit_processing": 8,
        "notes": "Billing starts on activation OR 31 days after signing (whichever first). Rate increases permitted after year 1.",
    },
    "ring": {
        "activation": 0, "installation": 0, "cellular_monthly": 0,
        "pro_install_per_device": 129.99,
        "notes": "No hidden fees on subscription. Pro install optional and expensive.",
    },
    "simplisafe": {
        "activation": 0, "installation": 0, "cellular_monthly": 0,
        "pro_install": 124.99,
        "notes": "Repeated monitoring price increases documented. Cancellation requires phone call.",
    },
    "vivint": {
        "activation": 0, "installation": 0, "cellular_monthly": 1.48,
        "premium_service_monthly": 10, "camera_addon_monthly": 5,
        "large_system_monthly": 30, "move_removal": 149,
        "move_reinstall": 149, "account_transfer": 99,
        "notes": "Cellular fee ($1.48/mo) appears in fine print everywhere but never in advertised pricing. Premium Service Plan ($10/mo) is soft-sold as 'included.'",
    },
    "abode": {
        "activation": 0, "installation": 0, "cellular_monthly": 0,
        "camera_standalone_monthly": 3.99, "camera_continuous_monthly": 9.99,
        "notes": "Camera cloud fees can add up fast. No phone support.",
    },
    "cove": {
        "activation": 0, "installation": 0, "cellular_monthly": 0,
        "economy_surcharge_monthly": 10, "late_fee_monthly_rate": 0.015,
        "declined_payment_fee": 20,
        "notes": "'No contract' claim is misleading - Economy Plan creates 36-month effective commitment. 18% APR late fee.",
    },
}

PROVIDER_NAMES = {
    "frontpoint": "Frontpoint",
    "adt": "ADT",
    "ring": "Ring",
    "simplisafe": "SimpliSafe",
    "vivint": "Vivint",
    "abode": "Abode",
    "cove": "Cove",
}
