/* Store & download URLs — update these when apps / builds change */
window.MKG_LINKS = {
  appStore: "#app-store",
  playStore: "#play-store",
  windowsMsi:
    "https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.22/MasterKeyGenie-0.1.22-x64.msi",
  /*
   * Production RevenueCat Web Purchase Link only.
   * Funnels -> Purchase Links -> Share URL.
   * Shape: https://pay.rev.cat/<id>/
   * Do not paste the sandbox URL. Do not append app_user_id.
   * Buy appends package_id=shop_annual, crew_annual, or organization_annual
   * and hide_back_button=true.
   * This site has no sign-in. Turn on Redemption Links in the web config,
   * or a visit without an app user id returns RevenueCat's 404.
   */
  revenueCatPurchaseLink: "https://pay.rev.cat/bvwykjqsahqmmjwr/",
};
