/* RT-7 collective facility risk model - JavaScript port.

   Runs the same model as risk-tools/collective/rt7_model.py so the dashboard
   tab can re-run it in the browser with edited inputs. The Python file is the
   reference implementation; test_rt7.py checks that this port agrees with it
   within Monte Carlo error (through risk-tools/collective/parity_runner.js).

   Plain ES5-ish, no dependencies, works in a browser and in node. Result keys
   deliberately match the Python result dict, snake_case and all, so the two
   can be compared field by field.

   Nothing here is calibrated. See risk-tools/rt-7-collective-facility-model.md. */
(function (root) {
  "use strict";
  var RT7 = { version: "0.2" };

  /* ---------------------------------------------------------------- rng */
  /* mulberry32: small, fast, good enough for a Monte Carlo of this size and
     deterministic for a given seed, which is what "same inputs, same chart"
     needs. Not numpy's generator, so parity with Python is statistical. */
  function makeRng(seed) {
    var a = (seed >>> 0) || 1;
    var spare = null;
    function u() {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    function normal() {                       /* Marsaglia polar */
      if (spare !== null) { var s = spare; spare = null; return s; }
      var x, y, r;
      do { x = 2 * u() - 1; y = 2 * u() - 1; r = x * x + y * y; } while (r >= 1 || r === 0);
      var f = Math.sqrt(-2 * Math.log(r) / r);
      spare = y * f;
      return x * f;
    }
    return { uniform: u, normal: normal,
             lognormal: function (mu, sigma) { return Math.exp(mu + sigma * normal()); } };
  }
  RT7.makeRng = makeRng;

  /* ----------------------------------------------------------- numerics */
  RT7.normPpf = function (p) {
    if (p <= 1e-300) return -8;
    if (p >= 1 - 1e-16) return 8;
    var a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
             1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
    var b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
             6.680131188771972e+01, -1.328068155288572e+01];
    var c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
             -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
    var d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
             3.754408661907416e+00];
    var plow = 0.02425, phigh = 1 - plow, q, r, v;
    if (p < plow) {
      q = Math.sqrt(-2 * Math.log(p));
      v = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
    } else if (p > phigh) {
      q = Math.sqrt(-2 * Math.log(1 - p));
      v = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
    } else {
      q = p - 0.5; r = q * q;
      v = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
    }
    return Math.max(-8, Math.min(8, v));
  };

  function lognormalSigma(cv) { return Math.sqrt(Math.log(1 + cv * cv)); }
  RT7.lognormalSigma = lognormalSigma;

  RT7.annuityPayment = function (principal, rate, years) {
    if (years <= 0) return 0;
    if (rate <= 0) return principal / years;
    return principal * rate / (1 - Math.pow(1 + rate, -years));
  };

  /* Anchored logistic: PD == basePd at pd_anchor_dscr, floor pd_floor_share x
     basePd as cover strengthens, ceiling pd_max as it collapses. */
  RT7.pdCurve = function (dscr, basePd, p) {
    var pdMin = p.pd_floor_share * basePd, pdMax = p.pd_max;
    var base = Math.min(Math.max(basePd, pdMin + 1e-12), pdMax - 1e-12);
    var frac = (base - pdMin) / (pdMax - pdMin);
    var c = Math.log(frac / (1 - frac));
    var z = p.pd_dscr_sensitivity * (p.pd_anchor_dscr - dscr) + c;
    z = Math.max(-40, Math.min(40, z));
    return pdMin + (pdMax - pdMin) / (1 + Math.exp(-z));
  };

  /* numpy's default (linear) percentile on an unsorted array. */
  function percentile(arr, q) {
    if (!arr.length) return 0;
    var s = arr.slice().sort(function (x, y) { return x - y; });
    var idx = (s.length - 1) * q / 100, lo = Math.floor(idx), hi = Math.ceil(idx);
    if (lo === hi) return s[lo];
    return s[lo] + (s[hi] - s[lo]) * (idx - lo);
  }
  RT7.percentile = percentile;
  function mean(arr) { var t = 0; for (var i = 0; i < arr.length; i++) t += arr[i]; return arr.length ? t / arr.length : 0; }
  function median(arr) { return percentile(arr, 50); }

  /* --------------------------------------------------------- parameters */
  /* Merge the tracker rows (data/rt7-parameters.csv as the dashboard sees
     them) into {parameter: value} for a region: "all" first, region wins. */
  var INTEGER_PARAMS = { n_members: 1, capex_tenor_years: 1, opex_tenor_years: 1 };
  RT7.mergeParams = function (rows, region) {
    var out = {}, i, r;
    for (i = 0; i < rows.length; i++) { r = rows[i]; if (r.Region === "all") out[r.Parameter] = r.Value; }
    for (i = 0; i < rows.length; i++) { r = rows[i]; if (r.Region === region) out[r.Parameter] = r.Value; }
    var keys = Object.keys(out);
    for (i = 0; i < keys.length; i++) {
      out[keys[i]] = INTEGER_PARAMS[keys[i]] ? Math.round(parseFloat(out[keys[i]])) : parseFloat(out[keys[i]]);
    }
    return out;
  };
  /* Same, but keeping the full provenance row per parameter. */
  RT7.provenance = function (rows, region) {
    var by = {}, i, r;
    for (i = 0; i < rows.length; i++) { r = rows[i]; if (r.Region === "all") by[r.Parameter] = r; }
    for (i = 0; i < rows.length; i++) { r = rows[i]; if (r.Region === region) by[r.Parameter] = r; }
    return Object.keys(by).map(function (k) { return by[k]; });
  };

  /* ------------------------------------------------------------ members */
  RT7.generateMembers = function (p, seed) {
    var rng = makeRng(seed), n = Math.round(p.n_members), i;
    var area = [], prod = [], hedge = [], other = [], hasC = [], hasO = [], capex = [], opex = [];
    for (i = 0; i < n; i++) area.push(Math.max(0.2, p.avg_area_ha + p.area_sd * rng.normal()));
    var s = lognormalSigma(p.member_yield_dispersion);
    for (i = 0; i < n; i++) prod.push(rng.lognormal(-0.5 * s * s, s));
    for (i = 0; i < n; i++) hedge.push(Math.min(1, Math.max(0, p.hedge_ratio_mean + p.hedge_ratio_sd * rng.normal())));
    for (i = 0; i < n; i++) other.push(Math.max(0, p.other_income_mean + p.other_income_sd * rng.normal()));
    for (i = 0; i < n; i++) hasC.push(rng.uniform() < p.capex_share);
    for (i = 0; i < n; i++) hasO.push(rng.uniform() < p.opex_share);
    var sl = p.loan_size_sigma;
    for (i = 0; i < n; i++) {
      var scale = area[i] / p.avg_area_ha;
      var c = p.avg_capex_size * scale * rng.lognormal(-0.5 * sl * sl, sl);
      capex.push(hasC[i] ? c : 0);
    }
    for (i = 0; i < n; i++) {
      var scale2 = area[i] / p.avg_area_ha;
      var o = p.avg_opex_size * scale2 * rng.lognormal(-0.5 * sl * sl, sl);
      opex.push(hasO[i] ? o : 0);
    }
    var ds = [], ead = [], basePd = [], lgd = [], hasLoan = [];
    for (i = 0; i < n; i++) {
      var dC = capex[i] > 0 ? RT7.annuityPayment(capex[i], p.capex_rate, Math.round(p.capex_tenor_years)) : 0;
      var dO = opex[i] * (1 + p.opex_rate);
      ds.push(dC + dO);
      var e = capex[i] + opex[i];
      ead.push(e);
      var w = e > 0 ? capex[i] / e : 0;
      basePd.push(w * p.base_pd_capex + (1 - w) * p.base_pd_opex);
      lgd.push(w * p.lgd_capex + (1 - w) * p.lgd_opex);
      hasLoan.push(e > 0);
    }
    return { n: n, area: area, productivity: prod, hedge: hedge, other_income: other,
             capex: capex, opex: opex, debt_service: ds, ead: ead, base_pd: basePd, lgd: lgd, has_loan: hasLoan };
  };

  /* ----------------------------------------------------------- simulate */
  RT7.simulate = function (p, opts) {
    opts = opts || {};
    var S = opts.nPaths || 5000, seed = (opts.seed == null ? 42 : opts.seed);
    var scen = opts.scenario || { climate_shift: 0, price_shift: 0 };
    var m = opts.members || RT7.generateMembers(p, seed);
    var rng = makeRng(seed + 1000003);
    var n = m.n, i, s;

    var expectedProd = [], expectedDelivered = 0;
    for (i = 0; i < n; i++) { expectedProd.push(m.area[i] * m.productivity[i] * p.base_yield_t_ha); expectedDelivered += m.hedge[i] * expectedProd[i]; }
    var fwdBook = p.fwd_share * expectedDelivered, fwdPrice = p.fwd_price_usd_per_t;
    var sY = lognormalSigma(p.yield_vol), sP = p.price_vol, sI = lognormalSigma(p.member_yield_idio_vol);
    var rhoCP = p.climate_price_correlation, rho = p.residual_correlation;
    var sqRho = Math.sqrt(rho), sq1Rho = Math.sqrt(1 - rho);
    var nBorrowers = 0; for (i = 0; i < n; i++) if (m.has_loan[i]) nBorrowers++;

    var facilityLoss = [], memberLoss = [], netCfs = [], yields = [], spots = [], shortfalls = [], diverteds = [];
    var sumPd = 0, cntPd = 0, cntDscrBelow1 = 0, sumDefaults = 0, sumAbsorbed = 0, sumShortCost = 0, sumDeficit = 0, capped = 0;
    var pool = 0; for (i = 0; i < n; i++) pool += m.ead[i];

    for (s = 0; s < S; s++) {
      var zc = rng.normal() + scen.climate_shift;
      var zp = rhoCP * (zc - scen.climate_shift) + Math.sqrt(1 - rhoCP * rhoCP) * rng.normal();
      var regionalYield = p.base_yield_t_ha * Math.exp(sY * zc - 0.5 * sY * sY);
      var jump = (rng.uniform() < p.price_jump_prob) ? (p.price_jump_mean + p.price_jump_sd * rng.normal()) : 0;
      /* the python draws the jump size for every path; drawing only when it
         fires changes the stream but not the distribution */
      var refPrice = p.price_base_usd_per_t * (1 + scen.price_shift) * Math.exp(sP * zp - 0.5 * sP * sP + jump);
      var spot = refPrice * (1 - p.basis_local);

      var premium = spot / fwdPrice - 1;
      var diverted = Math.min(1, Math.max(0, p.side_sell_elasticity * (premium - p.side_sell_threshold)));

      var production = new Array(n), delivered = 0;
      for (i = 0; i < n; i++) {
        var idio = rng.lognormal(-0.5 * sI * sI, sI);
        production[i] = m.area[i] * m.productivity[i] * regionalYield * idio;
        delivered += m.hedge[i] * production[i] * (1 - diverted);
      }
      var fwdSold = Math.min(delivered, fwdBook);
      var spotSold = Math.max(delivered - fwdBook, 0);
      var shortT = Math.max(fwdBook - delivered, 0);
      var shortCost = shortT * (Math.max(spot - fwdPrice, 0) + p.penalty_per_ton_short);
      var gross = fwdSold * fwdPrice + spotSold * spot;
      var margin = p.collective_margin_rate * gross;
      var payoutPerT = delivered > 0 ? (gross - margin) / delivered : 0;
      var netCf = margin - shortCost - p.collective_fixed_cost_usd;

      var zr = rng.normal(), mLoss = 0, nDef = 0;
      for (i = 0; i < n; i++) {
        var eps = rng.normal();                       /* drawn for every member, as in python */
        if (!m.has_loan[i]) continue;
        var committed = m.hedge[i] * production[i];
        var revenue = committed * (1 - diverted) * payoutPerT + (committed * diverted + (1 - m.hedge[i]) * production[i]) * spot + m.other_income[i];
        var cfads = revenue - m.area[i] * p.production_cost_per_ha - p.household_floor_usd;
        var dscr = cfads / m.debt_service[i];
        var pd = RT7.pdCurve(dscr, m.base_pd[i], p);
        sumPd += pd; cntPd++;
        if (dscr < 1) cntDscrBelow1++;
        var latent = sqRho * zr + sq1Rho * eps;
        if (latent < RT7.normPpf(pd)) { nDef++; mLoss += m.ead[i] * m.lgd[i]; }
      }
      var buffer = p.reserve_share_of_margin * Math.max(netCf, 0) - Math.max(-netCf, 0);
      var uncapped = Math.max(mLoss - buffer, 0);
      var fl = Math.min(uncapped, pool);
      if (uncapped > pool) capped++;
      facilityLoss.push(fl); memberLoss.push(mLoss); netCfs.push(netCf);
      yields.push(regionalYield); spots.push(spot); shortfalls.push(shortT); diverteds.push(diverted);
      sumDefaults += nDef; sumAbsorbed += Math.min(mLoss, Math.max(buffer, 0));
      sumShortCost += shortCost; sumDeficit += Math.max(-netCf, 0);
    }

    var ref = normalYear(p, m);
    var res = summarise(facilityLoss, memberLoss, pool, p);
    var lf = facilityLoss.map(function (x) { return pool > 0 ? x / pool : x; });
    var cnt = function (arr, f) { var c = 0; for (var k = 0; k < arr.length; k++) if (f(arr[k])) c++; return c / arr.length; };
    res.model_version = RT7.version;
    res.n_paths = S; res.n_members = n; res.n_borrowers = nBorrowers;
    res.pool_notional_usd = pool; res.fwd_book_t = fwdBook; res.expected_delivered_t = expectedDelivered;
    res.mean_default_rate = nBorrowers ? sumDefaults / S / nBorrowers : 0;
    res.mean_pd = cntPd ? sumPd / cntPd : 0;
    res.normal_year_pd = ref.pd; res.normal_year_median_dscr = ref.median_dscr;
    res.share_dscr_below_1 = cntPd ? cntDscrBelow1 / cntPd : 0;
    res.p_shortfall = cnt(shortfalls, function (x) { return x > 0; });
    res.mean_shortfall_cost_usd = sumShortCost / S;
    res.mean_diverted_share = mean(diverteds);
    res.p_side_selling = cnt(diverteds, function (x) { return x > 0; });
    res.mean_collective_net_cf_usd = mean(netCfs);
    res.p_collective_deficit = cnt(netCfs, function (x) { return x < 0; });
    res.mean_collective_deficit_usd = sumDeficit / S;
    res.p_loss_capped_at_pool = capped / S;
    res.mean_buffer_absorbed_usd = sumAbsorbed / S;
    res.mean_member_loss_usd = mean(memberLoss);
    res.member_el_pct = pool ? mean(memberLoss) / pool : 0;
    res.mean_regional_yield_t_ha = mean(yields);
    res.mean_spot_usd_per_t = mean(spots);
    res.loss_histogram = histogram(lf);
    if (opts.returnPaths) res.paths = { facility_loss: facilityLoss, member_loss: memberLoss, net_cf: netCfs };
    return res;
  };

  function normalYear(p, m) {
    var n = m.n, i, expectedProd = [], delivered = 0;
    for (i = 0; i < n; i++) { expectedProd.push(m.area[i] * m.productivity[i] * p.base_yield_t_ha); delivered += m.hedge[i] * expectedProd[i]; }
    var spot = p.price_base_usd_per_t * (1 - p.basis_local);
    var fwdBook = p.fwd_share * delivered;
    var fwdSold = Math.min(delivered, fwdBook);
    var gross = fwdSold * p.fwd_price_usd_per_t + Math.max(delivered - fwdBook, 0) * spot;
    var payout = delivered > 0 ? gross * (1 - p.collective_margin_rate) / delivered : 0;
    var dscrs = [], wpd = 0, w = 0;
    for (i = 0; i < n; i++) {
      if (!m.has_loan[i]) continue;
      var revenue = m.hedge[i] * expectedProd[i] * payout + (1 - m.hedge[i]) * expectedProd[i] * spot + m.other_income[i];
      var cfads = revenue - m.area[i] * p.production_cost_per_ha - p.household_floor_usd;
      var d = cfads / m.debt_service[i];
      dscrs.push(d);
      wpd += RT7.pdCurve(d, m.base_pd[i], p) * m.ead[i]; w += m.ead[i];
    }
    return { pd: w ? wpd / w : 0, median_dscr: dscrs.length ? median(dscrs) : NaN };
  }

  /* ---------------------------------------------------------- summaries */
  function trancheMetrics(lf, attach, detach) {
    var width = detach - attach, tl = lf.map(function (x) { return Math.min(Math.max(x - attach, 0), width) / width; });
    var cnt = function (f) { var c = 0; for (var k = 0; k < tl.length; k++) if (f(tl[k])) c++; return c / tl.length; };
    return { attach: attach, detach: detach, el_pct: mean(tl), ul95_pct: percentile(tl, 95), ul99_pct: percentile(tl, 99),
             p_any_loss: cnt(function (x) { return x > 0; }), p_wipeout: cnt(function (x) { return x >= 1 - 1e-12; }) };
  }
  RT7.trancheMetrics = trancheMetrics;

  function attachmentForTarget(lf, target) {
    function seniorEl(a) {
      if (a >= 1) return 0;
      var t = 0; for (var k = 0; k < lf.length; k++) t += Math.min(Math.max(lf[k] - a, 0), 1 - a);
      return (t / lf.length) / (1 - a);
    }
    if (seniorEl(0) <= target) return 0;
    var lo = 0, hi = 1;
    for (var it = 0; it < 40; it++) { var mid = 0.5 * (lo + hi); if (seniorEl(mid) <= target) hi = mid; else lo = mid; }
    return hi;
  }
  RT7.attachmentForTarget = attachmentForTarget;

  function histogram(lf, nBins) {
    nBins = nBins || 40;
    var hi = lf.length ? percentile(lf, 99) : 0;
    var cap = Math.max(0.02, Math.ceil(hi * 100 / 2) * 2 / 100);
    var edges = [], counts = [], k;
    for (k = 0; k <= nBins; k++) edges.push(cap * k / nBins);
    for (k = 0; k < nBins; k++) counts.push(0);
    for (k = 0; k < lf.length; k++) {
      var x = Math.min(lf[k], cap - 1e-12);
      var b = Math.min(nBins - 1, Math.max(0, Math.floor(x / cap * nBins)));
      counts[b]++;
    }
    return { edges: edges, counts: counts, n: lf.length };
  }
  RT7.histogram = histogram;

  function summarise(facilityLoss, memberLoss, pool, p) {
    var lf = facilityLoss.map(function (x) { return pool > 0 ? x / pool : 0; });
    var eq = p.tranche_equity_detach, mz = p.tranche_mezz_detach;
    var m = mean(lf), v = 0; for (var k = 0; k < lf.length; k++) v += (lf[k] - m) * (lf[k] - m);
    var noLoss = 0; for (k = 0; k < facilityLoss.length; k++) if (facilityLoss[k] <= 1e-9) noLoss++;
    return {
      el_usd: mean(facilityLoss), el_pct: m,
      ul95_pct: percentile(lf, 95), ul99_pct: percentile(lf, 99),
      ul95_usd: percentile(facilityLoss, 95), ul99_usd: percentile(facilityLoss, 99),
      sd_pct: Math.sqrt(lf.length ? v / lf.length : 0),
      p_no_loss: facilityLoss.length ? noLoss / facilityLoss.length : 0,
      tranches: { equity: trancheMetrics(lf, 0, eq), mezz: trancheMetrics(lf, eq, mz), senior: trancheMetrics(lf, mz, 1) },
      attachment_for_senior_target: attachmentForTarget(lf, p.senior_el_target_bp / 10000)
    };
  }

  /* -------------------------------------------------------- sensitivity */
  RT7.TORNADO = [
    ["hedge_ratio_mean", "abs", -0.20, 0.20], ["fwd_share", "abs", -0.25, 0.25],
    ["fwd_price_usd_per_t", "mul", 0.90, 1.10], ["yield_vol", "mul", 0.50, 1.50],
    ["price_vol", "mul", 0.50, 1.50], ["basis_local", "abs", -0.05, 0.05],
    ["base_pd_opex", "mul", 0.50, 1.50], ["base_pd_capex", "mul", 0.50, 1.50],
    ["lgd_opex", "abs", -0.15, 0.15], ["lgd_capex", "abs", -0.15, 0.15],
    ["residual_correlation", "set", 0.0, 0.30], ["household_floor_usd", "mul", 0.75, 1.25],
    ["production_cost_per_ha", "mul", 0.75, 1.25], ["side_sell_elasticity", "set", 0.0, 2.0],
    ["collective_fixed_cost_usd", "mul", 0.5, 2.0], ["pd_dscr_sensitivity", "mul", 0.5, 1.5]
  ];
  var CLAMP_01 = { hedge_ratio_mean: 1, fwd_share: 1, basis_local: 1, base_pd_opex: 1, base_pd_capex: 1,
                   lgd_opex: 1, lgd_capex: 1, residual_correlation: 1 };
  RT7.shocked = function (p, name, how, v) {
    var q = {}, k; for (k in p) if (Object.prototype.hasOwnProperty.call(p, k)) q[k] = p[k];
    var base = p[name], val = how === "abs" ? base + v : how === "mul" ? base * v : v;
    if (CLAMP_01[name]) val = Math.min(Math.max(val, 0), name === "residual_correlation" ? 0.95 : 1);
    if (name === "yield_vol" || name === "price_vol") val = Math.max(val, 0);
    q[name] = val;
    return q;
  };
  RT7.tornado = function (p, opts) {
    opts = opts || {};
    var base = RT7.simulate(p, opts), rows = [];
    for (var i = 0; i < RT7.TORNADO.length; i++) {
      var t = RT7.TORNADO[i], name = t[0], how = t[1], lo = t[2], hi = t[3];
      if (!(name in p)) continue;
      var pl = RT7.shocked(p, name, how, lo), ph = RT7.shocked(p, name, how, hi);
      var rl = RT7.simulate(pl, opts), rh = RT7.simulate(ph, opts);
      rows.push({ parameter: name, how: how, low: lo, high: hi, value_low: pl[name], value_high: ph[name],
                  el_low: rl.el_pct, el_high: rh.el_pct, el_base: base.el_pct,
                  ul99_low: rl.ul99_pct, ul99_high: rh.ul99_pct, ul99_base: base.ul99_pct,
                  swing_el: Math.abs(rh.el_pct - rl.el_pct) });
    }
    rows.sort(function (x, y) { return y.swing_el - x.swing_el; });
    return { base: base, rows: rows };
  };

  root.RT7 = RT7;
  if (typeof module !== "undefined" && module.exports) module.exports = RT7;
})(typeof window !== "undefined" ? window : globalThis);
