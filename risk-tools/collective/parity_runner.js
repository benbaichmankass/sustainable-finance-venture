#!/usr/bin/env node
/* Runs the JS port of RT-7 on inputs read from stdin and writes the result to
   stdout, so test_rt7.py can check the two implementations agree.

   stdin:  {"params": {...}, "nPaths": N, "seed": S, "scenario": {...},
            "pd_probe": [dscr, ...]}      # optional deterministic probes
   stdout: {"result": {...}, "pd_probe": [...], "ppf_probe": [...]}
*/
"use strict";
var path = require("path");
var RT7 = require(path.join(__dirname, "..", "..", "dashboard", "rt7-model.js"));

var chunks = [];
process.stdin.on("data", function (c) { chunks.push(c); });
process.stdin.on("end", function () {
  var inp = JSON.parse(chunks.join(""));
  var res = RT7.simulate(inp.params, { nPaths: inp.nPaths, seed: inp.seed, scenario: inp.scenario,
                                       members: inp.members || null, climateHistory: inp.climate_history || null });
  delete res.loss_histogram;
  var out = { result: res, version: RT7.version };
  if (inp.pd_probe) {
    out.pd_probe = inp.pd_probe.map(function (d) { return RT7.pdCurve(d, inp.pd_probe_base, inp.params); });
  }
  if (inp.ppf_probe) {
    out.ppf_probe = inp.ppf_probe.map(RT7.normPpf);
  }
  if (inp.annuity_probe) {
    out.annuity_probe = inp.annuity_probe.map(function (a) { return RT7.annuityPayment(a[0], a[1], a[2]); });
  }
  process.stdout.write(JSON.stringify(out));
});
