const form = document.getElementById("loan-form");
const resultEl = document.getElementById("result");

function dollarsToCents(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return null;
  return Math.round(n * 100);
}

function formatMoneyFromCents(cents) {
  if (cents === null || cents === undefined) return null;
  return (cents / 100).toFixed(2);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultEl.textContent = "Submitting...";

  const fd = new FormData(form);

  const rawSsn = (fd.get("ssn") || "").trim();
  const ssnDigits = rawSsn.replace(/\D/g, ""); // keep only digits

  const payload = {
    full_name: fd.get("full_name")?.trim(),
    email: fd.get("email")?.trim(),
    phone: fd.get("phone")?.trim(),
    ssn: ssnDigits,
    address_line_1: fd.get("address_line_1")?.trim(),
    address_line_2: (fd.get("address_line_2") || "").trim() || null,
    city: fd.get("city")?.trim(),
    state: fd.get("state")?.trim().toUpperCase(),
    zip_code: fd.get("zip_code")?.trim(),
    requested_amount_cents: dollarsToCents(fd.get("requested_amount_usd")),
  };

  if (payload.requested_amount_cents === null) {
    resultEl.textContent = "Invalid requested amount.";
    return;
  }

  try {
    const resp = await fetch("/v1/loan_applications", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await resp.json().catch(() => null);

    if (!resp.ok) {
      resultEl.textContent = JSON.stringify(
        { status: resp.status, response: json },
        null,
        2
      );
      return;
    }

    const loan = json?.data || {};

    const view = {
      status: loan.status,
      open_credit_lines: loan.open_credit_lines,
      requested_amount_usd: formatMoneyFromCents(loan.requested_amount_cents),
      total_loan_amount_usd: formatMoneyFromCents(loan.total_loan_amount_cents),
      interest_rate_bps: loan.interest_rate_bps,
      apr_percent:
        loan.interest_rate_bps != null
          ? (loan.interest_rate_bps / 100).toFixed(2)
          : null,
      term_months: loan.term_months,
      monthly_payment_usd: formatMoneyFromCents(loan.monthly_payment_cents),
      created_at: loan.created_at,
      id: loan.id,
    };

    resultEl.textContent =
      "Raw response:\n" +
      JSON.stringify(json, null, 2) +
      "\n\nOffer view:\n" +
      JSON.stringify(view, null, 2);
  } catch (err) {
    resultEl.textContent = "Request failed: " + String(err);
  }
});