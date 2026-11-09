/* Store & download URLs — update these when apps / builds change */
window.MKG_LINKS = {
  appStore: "https://apps.apple.com/app/master-key-genie/id6826968898",
  playStore:
    "https://play.google.com/store/apps/details?id=com.masterkeygenie.app&pcampaignid=web_share",
  windowsMsi:
    "https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.32/MasterKeyGenie-0.1.32-x64.msi",
  macDmg:
    "https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.32/MasterKeyGenie-0.1.32-universal.dmg",
  /*
   * Same GitHub Release host as the Windows installer. The signed disk image
   * is not in this repo and is not attached to v0.1.32 yet. Upload
   * MasterKeyGenie-0.1.32-universal.dmg to that release so this URL resolves:
   * https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.32/MasterKeyGenie-0.1.32-universal.dmg
   */
  macDmg:
    "https://github.com/jhoarty/MasterKeyGenie/releases/download/v0.1.32/MasterKeyGenie-0.1.32-universal.dmg",
  /*
   * Stripe Checkout is created by the Supabase function. The function holds
   * the Stripe secret. The anon key is the public client key, same as the apps.
   */
  licenseCheckoutUrl:
    "https://uwlpgnlcdvysuaidvywk.supabase.co/functions/v1/create-license-checkout",
  lockmastersCheckoutUrl:
    "https://uwlpgnlcdvysuaidvywk.supabase.co/functions/v1/create-lockmasters-checkout",
  licenseKeysUrl:
    "https://uwlpgnlcdvysuaidvywk.supabase.co/functions/v1/license-keys-for-session",
  supabaseAnonKey:
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3bHBnbmxjZHZ5c3VhaWR2eXdrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU0OTQ2MTgsImV4cCI6MjEwMTA3MDYxOH0.Dsp5bBogC6otWjWJaNNlmMOwnD6007lvibyoL7vwh_A",
};
