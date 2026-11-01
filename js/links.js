/* Store & download URLs — update these when apps / builds change */
window.MKG_LINKS = {
  appStore: "#app-store",
  playStore:
    "https://play.google.com/store/apps/details?id=com.masterkeygenie.app&pcampaignid=web_share",
  windowsMsi:
    "https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.29/MasterKeyGenie-0.1.29-x64.msi",
  /*
   * Stripe Checkout is created by the Supabase function. The function holds
   * the Stripe secret. The anon key is the public client key, same as the apps.
   */
  licenseCheckoutUrl:
    "https://uwlpgnlcdvysuaidvywk.supabase.co/functions/v1/create-license-checkout",
  licenseKeysUrl:
    "https://uwlpgnlcdvysuaidvywk.supabase.co/functions/v1/license-keys-for-session",
  supabaseAnonKey:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3bHBnbmxjZHZ5c3VhaWR2eXdrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU0OTQ2MTgsImV4cCI6MjEwMTA3MDYxOH0.Dsp5bBogC6otWjWJaNNlmMOwnD6007lvibyoL7vwh_A",
};
