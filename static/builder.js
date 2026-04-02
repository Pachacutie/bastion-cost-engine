/**
 * Equipment builder interactivity.
 * Manages device quantities, live-updating totals, and navigation to results.
 */

var quantities = {};
var providerSlug = '';
var tierIndex = 0;
var contractMonths = 0;
var installationType = 'diy';

function initBuilder(provider, tier, contract, installation) {
    providerSlug = provider;
    tierIndex = tier;
    contractMonths = contract;
    installationType = installation;

    var params = new URLSearchParams(window.location.search);
    document.querySelectorAll('.device-row').forEach(function(row) {
        var key = row.dataset.key;
        var urlQty = parseInt(params.get(key)) || 0;
        quantities[key] = urlQty;
        var qtyEl = document.getElementById('qty-' + key);
        if (qtyEl) qtyEl.textContent = urlQty;
    });

    // Auto-include hub if not set from URL
    if (!params.has('hub_base') && document.getElementById('qty-hub_base')) {
        quantities['hub_base'] = 1;
        document.getElementById('qty-hub_base').textContent = '1';
    }

    document.querySelectorAll('.qty-plus').forEach(function(btn) {
        btn.addEventListener('click', function() { changeQty(btn.dataset.key, 1); });
    });
    document.querySelectorAll('.qty-minus').forEach(function(btn) {
        btn.addEventListener('click', function() { changeQty(btn.dataset.key, -1); });
    });

    document.getElementById('see-results').addEventListener('click', goToResults);

    updateTotals();
}

function changeQty(key, delta) {
    var current = quantities[key] || 0;
    var newQty = Math.max(0, Math.min(99, current + delta));
    quantities[key] = newQty;

    var qtyEl = document.getElementById('qty-' + key);
    if (qtyEl) qtyEl.textContent = newQty;

    var row = document.querySelector('.device-row[data-key="' + key + '"]');
    var providerPrice = parseFloat(row.dataset.providerPrice) || 0;
    var lineEl = document.getElementById('line-' + key);
    if (lineEl) lineEl.textContent = '$' + (providerPrice * newQty).toFixed(2);

    updateTotals();
}

function updateTotals() {
    var providerTotal = 0;
    var genericTotal = 0;

    document.querySelectorAll('.device-row').forEach(function(row) {
        var key = row.dataset.key;
        var qty = quantities[key] || 0;
        var pp = parseFloat(row.dataset.providerPrice) || 0;
        var gp = parseFloat(row.dataset.genericPrice) || 0;
        providerTotal += pp * qty;
        genericTotal += gp * qty;
    });

    document.getElementById('provider-total').textContent = '$' + providerTotal.toFixed(2);
    document.getElementById('generic-total').textContent = '$' + genericTotal.toFixed(2);

    var pct = genericTotal > 0 ? ((providerTotal - genericTotal) / genericTotal * 100).toFixed(0) : '0';
    document.getElementById('markup-pct').textContent = pct + '%';

    var hasEquipment = Object.values(quantities).some(function(q) { return q > 0; });
    document.getElementById('see-results').disabled = !hasEquipment;
}

function goToResults() {
    var params = new URLSearchParams({
        provider: providerSlug,
        tier: tierIndex,
        contract: contractMonths,
        installation: installationType,
    });

    Object.keys(quantities).forEach(function(key) {
        if (quantities[key] > 0) params.set(key, quantities[key]);
    });

    window.location.href = '/results?' + params.toString();
}
