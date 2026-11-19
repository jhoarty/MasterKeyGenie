(() => {
  const notice = document.getElementById("pricing-notice");
  const checkoutUrl = String(
    (window.MKG_LINKS && window.MKG_LINKS.lockmastersCheckoutUrl) || "",
  ).trim();
  const anonKey = String(
    (window.MKG_LINKS && window.MKG_LINKS.supabaseAnonKey) || "",
  ).trim();
  const plans = {
    shop_annual: "shop",
    crew_annual: "crew",
    organization_annual: "organization",
  };

  function showStatus(message) {
    if (!notice) return;
    notice.hidden = false;
    notice.textContent = message;
  }

  const buttons = document.querySelectorAll("[data-buy]");
  if (!checkoutUrl || !anonKey || buttons.length === 0) {
    showStatus("This checkout is not open yet. You have not been charged.");
    return;
  }
  if (notice) notice.hidden = true;

  function setButtonsDisabled(disabled) {
    buttons.forEach((item) => {
      item.disabled = disabled;
    });
  }

  window.addEventListener("pageshow", () => {
    setButtonsDisabled(false);
  });

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const kind = button.getAttribute("data-buy") || "";
      const tier = plans[kind];
      const offline =
        kind === "government" ||
        kind === "government_facilities" ||
        kind === "government_facilities_only";
      const quantityInput = document.getElementById("license-quantity");
      const codeInput = document.getElementById("lockmasters-code");
      const quantity = quantityInput ? Number(quantityInput.value) : 1;
      const code = codeInput ? String(codeInput.value || "").trim() : "";
      if (!offline && !tier) return;
      if (!code) {
        showStatus("Enter the checkout code. You have not been charged.");
        return;
      }
      if (!Number.isFinite(quantity) || quantity < 1 || quantity > 500) {
        showStatus("Quantity must be from 1 to 500. You have not been charged.");
        return;
      }
      const payload = offline
        ? kind === "government_facilities_only"
          ? {
              product: "government-facilities",
              quantity: Math.floor(quantity),
              code,
            }
          : {
              product: "government",
              quantity: Math.floor(quantity),
              facilities: kind === "government_facilities",
              code,
            }
        : {
            tier,
            quantity: Math.floor(quantity),
            code,
          };

      setButtonsDisabled(true);
      fetch(checkoutUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          apikey: anonKey,
          Authorization: `Bearer ${anonKey}`,
        },
        body: JSON.stringify(payload),
      })
        .then((response) =>
          response.json().then((body) => ({ ok: response.ok, body })),
        )
        .then((result) => {
          if (result.ok && result.body && result.body.url) {
            window.location.assign(result.body.url);
            return;
          }
          setButtonsDisabled(false);
          showStatus(
            (result.body && result.body.error) ||
              "Checkout could not be started. You have not been charged.",
          );
        })
        .catch(() => {
          setButtonsDisabled(false);
          showStatus(
            "This checkout is not open yet. You have not been charged.",
          );
        });
    });
  });
})();
