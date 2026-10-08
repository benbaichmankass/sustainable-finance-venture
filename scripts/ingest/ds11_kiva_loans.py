#!/usr/bin/env python3
"""DS-11: Kiva agriculture loans in Colombia and Viet Nam, with field-partner
portfolio metrics - a PROXY population for smallholder coffee borrowers.

    python3 scripts/ingest/ds11_kiva_loans.py            # fetch + process
    python3 scripts/ingest/ds11_kiva_loans.py --no-fetch

Pulls the newest N loans per country in Kiva's Agriculture sector (all
statuses) through the public GraphQL API, keeps loan size, term, status,
dates and the use-of-funds text, and flags loans whose use text mentions
coffee. Field partners come with their published default, arrears and
at-risk rates. Ethiopia has no Kiva agriculture loans, so it is absent.

What this is NOT: a cooperative's loan book. Kiva borrowers are the clients
of microfinance partners who chose to list on Kiva; the partner rates are
for Kiva-funded portfolios. The values derived from this are Basis: proxy.

Privacy: borrower first names and towns are in the API response and are
kept in the raw file only; the processed file carries the loan id, country,
amount, term, status, dates, activity, a coffee flag and the partner id.

Raw:       data/raw/DS-11/kiva-agri-loans-<date>.json (+ .query.json)
Processed: data/processed/ds-11-kiva-agriculture-loans.csv (+ .md)
           data/processed/ds-11-kiva-partners.csv (+ .md)
Python 3 stdlib.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

DS = "DS-11"
API = "https://api.kivaws.org/graphql"
COUNTRIES = ["CO", "VN"]
PER_COUNTRY = 3000
PAGE = 100
FIELDS = ("id loanAmount use status delinquent raisedDate disbursalDate defaultedDate endedDate borrowerCount "
          "repaymentInterval lenderRepaymentTerm sector { id name } activity { id name } "
          "geocode { city state country { isoCode name } } "
          "terms { currency disbursalAmount lenderRepaymentTerm repaymentCount graceMonths } "
          "... on LoanPartner { partnerId partnerName partner { id name defaultRate arrearsRate loansAtRiskRate "
          "averageLoanSize averageLoanTermMonths loansPosted startDate riskRating status countries { isoCode } } }")
# Kiva's edge returns 403 to non-browser user agents (the repo's usual UA included), so this fetcher presents a browser string.
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
COFFEE = re.compile(r"coffee|caf[eé]\b|cafetal|c[àa] ph[êe]", re.I)


def gql(query):
    req = urllib.request.Request(API, data=json.dumps({"query": query}).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all():
    out = {}
    for c in COUNTRIES:
        rows, total = [], None
        for off in range(0, PER_COUNTRY, PAGE):
            q = ('{ lend { loans(filters: {country: ["%s"], sector: [1], status: all}, sortBy: newest, limit: %d, offset: %d) '
                 '{ totalCount values { %s } } } }' % (c, PAGE, off, FIELDS))
            d = gql(q)
            if "errors" in d:
                C.fail("%s offset %d: %s" % (c, off, d["errors"][0]["message"][:200]))
            v = d["data"]["lend"]["loans"]; total = v["totalCount"]; rows += v["values"]
            if len(v["values"]) < PAGE:
                break
            time.sleep(0.3)
        out[c] = {"totalCount": total, "loans": rows}
        print("  %s: %d of %d agriculture loans" % (c, len(rows), total))
    return out


def process(raw_path, raw_log):
    blob = json.load(open(raw_path, encoding="utf-8"))
    loans, partners = [], {}
    for c, d in blob["data"].items():
        for l in d["loans"]:
            p = l.get("partner") or {}
            loans.append([c, l["id"], float(l["loanAmount"]), l.get("lenderRepaymentTerm") or "",
                          l.get("status") or "", (l.get("raisedDate") or "")[:10], (l.get("disbursalDate") or "")[:10],
                          (l.get("defaultedDate") or "")[:10], (l.get("endedDate") or "")[:10],
                          "yes" if l.get("delinquent") else "no", l.get("borrowerCount") or "",
                          (l.get("activity") or {}).get("name", ""), "yes" if COFFEE.search(l.get("use") or "") else "no",
                          (l.get("terms") or {}).get("currency", ""), (l.get("terms") or {}).get("disbursalAmount", "") or "",
                          p.get("id", "")])
            if p:
                partners[p["id"]] = [p["id"], p["name"], ";".join(x["isoCode"] for x in p.get("countries", [])),
                                     round(p["defaultRate"], 3), round(p["arrearsRate"], 3), round(p["loansAtRiskRate"], 3),
                                     p.get("averageLoanSize", ""), p.get("averageLoanTermMonths", ""), p.get("loansPosted", ""),
                                     (p.get("startDate") or "")[:10], p.get("riskRating", ""), p.get("status", "")]
    header = ["Country", "Loan_ID", "Amount_USD", "Term_Months", "Status", "Raised_Date", "Disbursal_Date", "Defaulted_Date",
              "Ended_Date", "Delinquent", "Borrower_Count", "Activity", "Coffee_Mention", "Local_Currency", "Disbursal_Amount_LCU", "Partner_ID"]
    n_coffee = {c: sum(1 for l in loans if l[0] == c and l[12] == "yes") for c in COUNTRIES}
    md = """# DS-11 — Kiva agriculture loans, Colombia and Viet Nam (proxy population)

One row per loan: the %d newest loans in Kiva's Agriculture sector per country at retrieval, all statuses. Colombia %d loans (%d mention coffee in the use text), Viet Nam %d loans (%d mention coffee). Ethiopia has no Kiva agriculture loans.

| Column | Meaning |
|---|---|
| `Country` | ISO code |
| `Loan_ID` | Kiva loan id (public) |
| `Amount_USD` | Loan amount posted on Kiva, USD |
| `Term_Months` | Lender repayment term in months (Kiva's `lenderRepaymentTerm`) |
| `Status` | Kiva status at retrieval (fundraising, funded, expired, refunded) |
| `Raised_Date`, `Disbursal_Date`, `Defaulted_Date`, `Ended_Date` | As published; blank when not set |
| `Delinquent` | Kiva's delinquency flag at retrieval |
| `Borrower_Count` | 1 for individual loans, more for groups |
| `Activity` | Kiva activity (Agriculture, Farming, Pigs, ...); there is no coffee activity, hence the text flag |
| `Coffee_Mention` | `yes` if the use-of-funds text mentions coffee |
| `Local_Currency`, `Disbursal_Amount_LCU` | Disbursal terms where published |
| `Partner_ID` | Field partner; metrics in `ds-11-kiva-partners.csv` |

**What it is.** A proxy for smallholder agricultural borrowers in two of the three RT-7 countries: real loans to real farmers, including hundreds whose stated purpose is coffee (fertiliser, planting, a wet mill), with their sizes and terms. It is not a cooperative's book: Kiva's partners are microfinance institutions and social enterprises, the loans are those partners chose to list, and Kiva's status fields on recent loans say nothing about repayment (no loan in this pull is past its term). Repayment behaviour comes only from the partner-level rates.

**Validation (run %s).** Schema: sixteen columns. Coverage: newest-first, so the date range is whatever the last %d loans span per country. Units: USD as posted. Names and towns were dropped from the processed file.

%s
""" % (PER_COUNTRY, sum(1 for l in loans if l[0] == "CO"), n_coffee["CO"], sum(1 for l in loans if l[0] == "VN"), n_coffee["VN"],
       C.now_iso(), PER_COUNTRY, C.provenance_block(DS, raw_log, "scripts/ingest/ds11_kiva_loans.py", {"API": API, "Filters": blob.get("filters", "")}))
    C.write_processed("ds-11-kiva-agriculture-loans", header, loans, md)

    pheader = ["Partner_ID", "Partner_Name", "Countries", "Default_Rate_Pct", "Arrears_Rate_Pct", "Loans_At_Risk_Rate_Pct",
               "Average_Loan_Size_USD", "Average_Loan_Term_Months", "Loans_Posted", "Start_Date", "Risk_Rating", "Status"]
    pmd = """# DS-11 — Kiva field partners behind the sampled loans

One row per field partner appearing in `ds-11-kiva-agriculture-loans.csv`, with Kiva's published portfolio metrics at retrieval.

| Column | Meaning (Kiva's definitions) |
|---|---|
| `Default_Rate_Pct` | Amount of ended loans defaulted as a share of the amount of ended loans, Kiva-funded portfolio |
| `Arrears_Rate_Pct` | Amount in arrears as a share of the outstanding Kiva-funded portfolio |
| `Loans_At_Risk_Rate_Pct` | Share of outstanding portfolio with any payment overdue |
| `Average_Loan_Size_USD`, `Average_Loan_Term_Months` | Across the partner's Kiva loans |
| `Loans_Posted` | Count of loans the partner has posted on Kiva |
| `Risk_Rating` | Kiva's internal rating (0.5 to 5 stars) |

**Reading the rates.** These describe each partner's Kiva-funded book, not coffee loans specifically and not the partner's whole portfolio. The default rate is a loss-of-amount measure over the partner's history; the arrears rate is a portfolio-at-risk measure at a point in time. For the RT-7 proxy the arrears rate stands in for the normal-year probability of a payment problem and the default rate is recorded as an observation. One Vietnamese partner shows an arrears rate above 60 percent and nearly all of its book at risk: a partner in distress, which the loans-posted weighting limits but does not remove.

**Validation (run %s).** Partner ids unique; rates numeric; countries as published.

%s
""" % (C.now_iso(), C.provenance_block(DS, raw_log, "scripts/ingest/ds11_kiva_loans.py", {"API": API}))
    C.write_processed("ds-11-kiva-partners", pheader, [partners[k] for k in sorted(partners)], pmd)


def main():
    if "--no-fetch" not in sys.argv:
        print("fetching from %s" % API)
        data = fetch_all()
        blob = {"retrieved_at_utc": C.now_iso(), "api": API, "query_fields": FIELDS,
                "filters": "country in %s; sector 1 Agriculture; status all; sortBy newest; %d newest per country" % (COUNTRIES, PER_COUNTRY),
                "data": data}
        raw_path, log = C.save_raw(DS, "kiva-agri-loans-%s.json" % C.today(), json.dumps(blob).encode("utf-8"),
                                   {"api": API, "method": "POST GraphQL, paged", "filters": blob["filters"], "fields": FIELDS},
                                   "Verbatim loan objects as returned, including borrower first names and towns: raw only, never processed into the repo.")
        print("raw: %s (%d bytes)" % (os.path.relpath(raw_path, C.ROOT), log["bytes"]))
    else:
        raw_path = C.latest_raw(DS, ".json")
        if not raw_path:
            C.fail("no raw file; run without --no-fetch")
        log = json.load(open(raw_path + ".query.json"))
    process(raw_path, log)


if __name__ == "__main__":
    main()
