(() => {
  const notice = document.getElementById("pricing-notice");

  function purchaseUrl(packageId) {
    const raw = (window.MKG_LINKS && window.MKG_LINKS.revenueCatPurchaseLink) || "";
    const trimmed = String(raw).trim();
    if (!trimmed) return null;

    let url;
    try {
      url = new URL(trimmed);
    } catch {
      return null;
    }

    const sandbox = /sandbox/i.test(`${url.pathname}${url.search}`);
    if (url.protocol !== "https:" || url.hostname !== "pay.rev.cat" || sandbox) {
      return null;
    }

    url.searchParams.set("package_id", packageId);
    url.searchParams.set("hide_back_button", "true");
    return url.toString();
  }

  function showNotConnected() {
    if (!notice) return;
    notice.hidden = false;
    notice.textContent =
      "Online checkout is not connected yet. You have not been charged. The prices below are the yearly plans.";
  }

  const buttons = document.querySelectorAll("[data-buy]");
  let ready = buttons.length > 0;

  buttons.forEach((button) => {
    const packageId = button.getAttribute("data-buy");
    const href = packageId ? purchaseUrl(packageId) : null;
    if (!href) ready = false;

    button.addEventListener("click", () => {
      const target = packageId ? purchaseUrl(packageId) : null;
      if (!target) {
        showNotConnected();
        return;
      }
      window.location.assign(target);
    });
  });

  if (!ready) showNotConnected();
  else if (notice) notice.hidden = true;
})();
