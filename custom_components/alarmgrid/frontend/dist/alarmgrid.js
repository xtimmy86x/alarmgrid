const ALARMS_UPDATED_EVENT = "alarmgrid_alarms_updated";

// The card and its visual editor intentionally share one source of truth.  The
// editor omits values matching these defaults to keep storage/YAML concise.
const CARD_DEFAULTS = Object.freeze({
  title: "AlarmGrid", view: "active", max_alarms: 5, theme: "auto",
  header_icon: "mdi:alarm-light", hide_header: false,
  show_header_icon: true, show_header_status: true, show_header_actions: true,
  show_summary: true, show_actions: true, show_shelve_action: true,
  show_disable_action: true, show_restore_actions: true, show_value: true,
  show_area: true, show_system: true, show_tag: true, show_open_panel: true,
  min_height: "0px", header_icon_size: "24px", title_font_size: "1.15rem",
  subtitle_font_size: ".85rem", summary_font_size: ".78rem",
  alarm_name_font_size: "1rem", alarm_meta_font_size: ".78rem",
  priority_font_size: ".7rem", action_font_size: ".78rem",
});

const CARD_PRIORITIES = ["critical", "high", "medium", "low", "info", "status"];

const TRANSLATIONS = {
  en: {
    default_title: "AlarmGrid",
    menu: "Menu",
    open_sidebar: "Open sidebar",
    metric_active: "{count} active",
    metric_unack: "{count} unack",
    horn_active: "Horn active",
    horn_idle: "Horn idle",
    enable_alarm_sound: "Enable Alarm Sound",
    silence: "Silence horn",
    ack_all: "Ack All",
    tab_active: "Active Alarms",
    tab_unacknowledged: "Unacknowledged",
    tab_history: "History",
    tab_shelved: "Shelved",
    tab_disabled: "Disabled",
    tab_rules: "Rules",
    tab_settings: "Settings",
    duration_1h: "1 hour",
    duration_4h: "4 hours",
    duration_8h: "8 hours",
    duration_1d: "1 day",
    duration_3d: "3 days",
    duration_7d: "7 days",
    search_placeholder: "Search tag, alarm, entity, area",
    shelve_for: "Shelve for",
    refresh: "Refresh",
    history_from: "From",
    history_to: "To",
    download_history: "Download CSV",
    history_range_required: "Select both the start and end of the time range",
    history_range_invalid: "The end of the time range must be after the start",
    history_exported: "Downloaded {count} history events",
    priority_all: "all",
    priority_critical: "critical",
    priority_high: "high",
    priority_medium: "medium",
    priority_low: "low",
    priority_info: "info",
    priority_status: "status",
    state_normal: "Normal",
    state_active_unack: "Active, unacknowledged",
    state_active_ack: "Active, acknowledged",
    state_cleared_unack: "Cleared, unacknowledged",
    state_cleared_ack: "Cleared, acknowledged",
    state_shelved: "Shelved",
    state_disabled: "Disabled",
    state_suppressed: "Suppressed",
    state_out_of_service: "Out of service",
    col_time: "Time",
    col_priority: "Priority",
    col_area: "Area",
    col_system: "System",
    col_tag: "Tag",
    col_alarm: "Alarm",
    col_source_value: "Source Value",
    col_state: "State",
    col_shelved_until: "Shelved Until",
    col_ack: "Ack",
    col_shelve: "Shelve",
    col_instructions: "Instructions",
    col_event: "Event",
    col_from: "From",
    col_to: "To",
    col_operator: "Operator",
    col_id: "ID",
    col_entity: "Entity",
    col_name: "Name",
    col_condition: "Condition",
    col_threshold: "Threshold",
    col_enabled: "Enabled",
    col_telegram: "Telegram",
    telegram_notifications: "Telegram notifications",
    telegram_policy_inherit: "Use global settings",
    telegram_policy_always: "Always notify",
    telegram_policy_never: "Never notify",
    telegram_table_inherit: "Global",
    telegram_table_always: "Always",
    telegram_table_never: "Never",
    ack: "Ack",
    shelve: "Shelve",
    no_alarms: "No alarms in this view",
    no_history: "No history rows",
    no_rules: "No rules configured",
    select_all: "Select All",
    deselect_all: "Deselect All",
    n_selected: "{count} selected",
    n_estimated_entities: "{count} estimated entities",
    n_rules: "{count} rules",
    placeholder_rule_id: "Rule id",
    placeholder_entity_id: "Entity id",
    placeholder_name: "Name",
    placeholder_system: "System",
    placeholder_threshold: "Threshold",
    condition_builder: "Condition Builder", match: "Match", all_conditions: "ALL conditions", any_condition: "ANY condition",
    add_condition: "+ Add condition", add_group: "+ Add group", delete_condition: "Delete condition", delete_group: "Delete group",
    current_state: "Current", deadband_hysteresis: "Deadband / Hysteresis", hysteresis_help: "Prevents alarm chattering near the threshold.",
    alarm_delay: "Alarm delay", clear_delay: "Clear delay", seconds: "seconds",
    add_rule: "Add Rule",
    edit: "Edit",
    save_rule: "Save Rule",
    cancel: "Cancel",
    editing_rule: "Editing rule {id}",
    rule_updated: "Rule {id} updated",
    delete_selected: "Delete Selected",
    export_rules: "Export CSV",
    import_rules: "Import CSV",
    imported_rules: "Imported {count} rules ({created} created, {updated} updated)",
    invalid_csv_file: "Select a valid CSV file",
    yes: "yes",
    no: "no",
    sound_mode: "Sound mode",
    browser_sound: "Browser sound",
    media_player_sound: "Media player sound",
    active_audible: "Active audible alarms",
    test_sound: "Test Sound",
    enabled: "enabled",
    disabled: "disabled",
    skipped_suffix: ", skipped {count}",
    label_selected_rules: "selected rules",
    no_items_to_delete: "No {label} to delete",
    confirm_delete_rules: "Delete {count} {label} and about {entities} entities? Source entities will not be removed.",
    deleted_rules: "Deleted {count} rules and {entities} entities",
    more_actions: "More actions", suspend_alarm: "Suspend alarm", disable_alarm: "Disable alarm",
    unshelve_now: "Unshelve now", enable_alarm: "Enable alarm", suspend_for: "Suspend for", custom_duration: "Custom…",
    duration: "Duration", minutes: "minutes", hours: "hours", days: "days", comment_optional: "Comment / Reason (optional)",
    confirm_disable_title: 'Disable "{name}"?', confirm_disable_message: "This alarm will no longer be generated until it is manually enabled again.",
    suspend: "Suspend", disable: "Disable", shelved_until: "Suspended until {time}", remaining: "{time} remaining",
    alarm_disabled: "Alarm disabled", expiring: "Expiring…", shelved_temporary: "Shelved · temporary", disabled_persistent: "Disabled · until manually enabled",
    duration_invalid: "Enter a duration greater than zero.", duration_15m: "15 minutes", custom: "Custom…",
  },
  it: {
    default_title: "Allarmi Industriali",
    menu: "Menu",
    open_sidebar: "Apri barra laterale",
    metric_active: "{count} attivi",
    metric_unack: "{count} non riconosciuti",
    horn_active: "Sirena attiva",
    horn_idle: "Sirena a riposo",
    enable_alarm_sound: "Abilita suono allarmi",
    silence: "Silenzia sirena",
    ack_all: "Riconosci tutti",
    tab_active: "Allarmi attivi",
    tab_unacknowledged: "Non riconosciuti",
    tab_history: "Storico",
    tab_shelved: "Sospesi",
    tab_disabled: "Disabilitati",
    tab_rules: "Regole",
    tab_settings: "Impostazioni",
    duration_1h: "1 ora",
    duration_4h: "4 ore",
    duration_8h: "8 ore",
    duration_1d: "1 giorno",
    duration_3d: "3 giorni",
    duration_7d: "7 giorni",
    search_placeholder: "Cerca tag, allarme, entità, area",
    shelve_for: "Sospendi per",
    refresh: "Aggiorna",
    history_from: "Da",
    history_to: "A",
    download_history: "Scarica CSV",
    history_range_required: "Seleziona l'inizio e la fine dell'intervallo",
    history_range_invalid: "La fine dell'intervallo deve essere successiva all'inizio",
    history_exported: "Scaricati {count} eventi dello storico",
    priority_all: "tutte",
    priority_critical: "critica",
    priority_high: "alta",
    priority_medium: "media",
    priority_low: "bassa",
    priority_info: "info",
    priority_status: "stato",
    state_normal: "Normale",
    state_active_unack: "Attivo, non riconosciuto",
    state_active_ack: "Attivo, riconosciuto",
    state_cleared_unack: "Rientrato, non riconosciuto",
    state_cleared_ack: "Rientrato, riconosciuto",
    state_shelved: "Sospeso",
    state_disabled: "Disabilitato",
    state_suppressed: "Soppresso",
    state_out_of_service: "Fuori servizio",
    col_time: "Ora",
    col_priority: "Priorità",
    col_area: "Area",
    col_system: "Sistema",
    col_tag: "Tag",
    col_alarm: "Allarme",
    col_source_value: "Valore sorgente",
    col_state: "Stato",
    col_shelved_until: "Sospeso fino a",
    col_ack: "Riconosci",
    col_shelve: "Sospendi",
    col_instructions: "Istruzioni",
    col_event: "Evento",
    col_from: "Da",
    col_to: "A",
    col_operator: "Operatore",
    col_id: "ID",
    col_entity: "Entità",
    col_name: "Nome",
    col_condition: "Condizione",
    col_threshold: "Soglia",
    col_enabled: "Abilitata",
    col_telegram: "Telegram",
    telegram_notifications: "Notifiche Telegram",
    telegram_policy_inherit: "Usa impostazioni globali",
    telegram_policy_always: "Notifica sempre",
    telegram_policy_never: "Non notificare mai",
    telegram_table_inherit: "Globale",
    telegram_table_always: "Sempre",
    telegram_table_never: "Mai",
    ack: "Riconosci",
    shelve: "Sospendi",
    no_alarms: "Nessun allarme in questa vista",
    no_history: "Nessun evento nello storico",
    no_rules: "Nessuna regola configurata",
    select_all: "Seleziona tutte",
    deselect_all: "Deseleziona tutte",
    n_selected: "{count} selezionate",
    n_estimated_entities: "{count} entità stimate",
    n_rules: "{count} regole",
    placeholder_rule_id: "ID regola",
    placeholder_entity_id: "ID entità",
    placeholder_name: "Nome",
    placeholder_system: "Sistema",
    placeholder_threshold: "Soglia",
    condition_builder: "Costruttore condizioni", match: "Corrispondenza", all_conditions: "Tutte le condizioni", any_condition: "Almeno una condizione",
    add_condition: "+ Aggiungi condizione", add_group: "+ Aggiungi gruppo", delete_condition: "Elimina condizione", delete_group: "Elimina gruppo",
    current_state: "Attuale", deadband_hysteresis: "Banda morta / Isteresi", hysteresis_help: "Evita commutazioni ripetute dell’allarme vicino alla soglia.",
    alarm_delay: "Ritardo allarme", clear_delay: "Ritardo ripristino", seconds: "secondi",
    add_rule: "Aggiungi regola",
    edit: "Modifica",
    save_rule: "Salva regola",
    cancel: "Annulla",
    editing_rule: "Modifica della regola {id}",
    rule_updated: "Regola {id} aggiornata",
    delete_selected: "Elimina selezionate",
    export_rules: "Esporta CSV",
    import_rules: "Importa CSV",
    imported_rules: "Importate {count} regole ({created} create, {updated} aggiornate)",
    invalid_csv_file: "Seleziona un file CSV valido",
    yes: "sì",
    no: "no",
    sound_mode: "Modalità suono",
    browser_sound: "Suono browser",
    media_player_sound: "Suono media player",
    active_audible: "Allarmi udibili attivi",
    test_sound: "Prova suono",
    enabled: "abilitato",
    disabled: "disabilitato",
    skipped_suffix: ", saltate {count}",
    label_selected_rules: "regole selezionate",
    no_items_to_delete: "Nessuna {label} da eliminare",
    confirm_delete_rules: "Eliminare {count} {label} e circa {entities} entità? Le entità sorgente non verranno rimosse.",
    deleted_rules: "Eliminate {count} regole e {entities} entità",
    more_actions: "Altre azioni", suspend_alarm: "Sospendi allarme", disable_alarm: "Disabilita allarme",
    unshelve_now: "Riattiva ora", enable_alarm: "Abilita allarme", suspend_for: "Sospendi per", custom_duration: "Personalizzato…",
    duration: "Durata", minutes: "minuti", hours: "ore", days: "giorni", comment_optional: "Commento / Motivo (opzionale)",
    confirm_disable_title: 'Disabilitare "{name}"?', confirm_disable_message: "L’allarme non verrà più generato finché non verrà riabilitato manualmente.",
    suspend: "Sospendi", disable: "Disabilita", shelved_until: "Sospeso fino alle {time}", remaining: "{time} rimanenti",
    alarm_disabled: "Allarme disabilitato", expiring: "In scadenza…", shelved_temporary: "Sospeso · temporaneo", disabled_persistent: "Disabilitato · fino alla riabilitazione manuale",
    duration_invalid: "Inserisci una durata maggiore di zero.", duration_15m: "15 minuti", custom: "Personalizzato…",
  },
};

class AlarmGrid extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._alarms = [];
    this._history = [];
    this._historyStart = "";
    this._historyEnd = "";
    this._historyExportResult = "";
    this._rules = [];
    this._ruleDraft = {
      id: "",
      entity_id: "",
      name: "",
      condition: "above",
      threshold: "",
      priority: "medium",
      telegram_notification_policy: "inherit",
      system: "",
      deadband: 0, delay_on_seconds: 0, delay_off_seconds: 0, condition_expression: null,
    };
    this._selectedRuleIds = new Set();
    this._editingRuleId = null;
    this._rulesResult = null;
    this._builderRevision = 0;
    this._sound = {};
    this._tab = "active";
    this._themeMode = "auto";
    this._effectiveTheme = "light";
    this._search = "";
    this._priority = "all";
    this._shelveDurationMinutes = 60;
    this._audioEnabled = false;
    this._refreshing = false;
    this._updatesSubscribed = false;
    this._unsubscribeUpdates = undefined;
    this._columnWidths = {};
    this._tableScrollLeft = {};
    this._alarmVisualDelayMs = 2000;
    this._alarmFirstSeenAt = {};
    this._alarmVisualRefreshTimer = undefined;
    this._browserHornCooldownMs = 2000;
    this._lastBrowserHornAt = 0;
  }

  set hass(hass) {
    this._hass = hass;
    this._syncTheme();
    this._subscribeUpdates();
    if (!this._rendered) {
      this._render();
      this._load();
      this._timer = window.setInterval(() => this._load(), 5000);
    }
    this._maybePlayBrowserHorn();
  }

  set narrow(value) {
    this._narrow = value;
    this._render();
  }

  set panel(panel) {
    this._panel = panel;
  }

  disconnectedCallback() {
    if (this._timer) {
      window.clearInterval(this._timer);
    }
    if (this._alarmVisualRefreshTimer) {
      window.clearTimeout(this._alarmVisualRefreshTimer);
      this._alarmVisualRefreshTimer = undefined;
    }
    if (this._retryLoadTimer) {
      window.clearTimeout(this._retryLoadTimer);
      this._retryLoadTimer = undefined;
    }
    if (this._unsubscribeUpdates) {
      Promise.resolve(this._unsubscribeUpdates)
        .then((unsubscribe) => {
          if (typeof unsubscribe === "function") unsubscribe();
        })
        .catch(() => undefined);
      this._unsubscribeUpdates = undefined;
      this._updatesSubscribed = false;
    }
  }

  async _callWS(payload) {
    if (!this._hass) return null;
    return this._hass.callWS(payload);
  }

  _language() {
    const language = this._hass?.locale?.language || this._hass?.language || "en";
    return String(language).toLowerCase().split("-")[0];
  }

  _t(key, replacements = {}) {
    const language = this._language();
    const table = TRANSLATIONS[language] || TRANSLATIONS.en;
    let text = table[key] ?? TRANSLATIONS.en[key] ?? key;
    Object.entries(replacements).forEach(([name, value]) => {
      text = text.replaceAll(`{${name}}`, String(value));
    });
    return text;
  }

  _lifecycleLabel(state) {
    const key = `state_${String(state || "NORMAL").toLowerCase()}`;
    const table = TRANSLATIONS[this._language()] || TRANSLATIONS.en;
    if (table[key] ?? TRANSLATIONS.en[key]) return this._t(key);
    return this._escape(state);
  }

  _subscribeUpdates() {
    const connection = this._hass?.connection;
    if (this._updatesSubscribed || !connection?.subscribeEvents) return;
    this._updatesSubscribed = true;
    try {
      this._unsubscribeUpdates = connection.subscribeEvents(
        (event) => this._handleAlarmUpdateEvent(event),
        ALARMS_UPDATED_EVENT
      );
    } catch (_err) {
      this._updatesSubscribed = false;
      this._unsubscribeUpdates = undefined;
    }
  }

  _handleAlarmUpdateEvent(event) {
    const entryId = this._panel?.config?.entry_id || this._cardConfig?.entry_id;
    if (entryId && event?.data?.entry_id && event.data.entry_id !== entryId) return;
    this._load();
  }

  async _load() {
    if (this._refreshing || !this._hass) return;
    this._refreshing = true;
    try {
      const alarms = await this._callWS({ type: "alarmgrid/list_alarms" });
      const history = await this._callWS({ type: "alarmgrid/list_history", limit: 250 });
      const rules = await this._callWS({ type: "alarmgrid/list_rules" });
      this._alarms = alarms?.alarms || [];
      this._sound = alarms?.sound || {};
      this._history = history?.events || [];
      this._rules = rules?.rules || [];
      const ruleIds = new Set(this._rules.map((rule) => rule.id));
      this._selectedRuleIds = new Set([...this._selectedRuleIds].filter((id) => ruleIds.has(id)));
      this._error = undefined;
      this._maybePlayBrowserHorn();
      if (!this._isEditingRulesForm()) this._render();
    } catch (err) {
      const message = err?.message || String(err);
      if (/not loaded|not configured/i.test(message)) {
        // The config entry is reloading (e.g. after a rule change); retry shortly.
        this._scheduleRetryLoad();
      } else {
        this._error = message;
        if (!this._isEditingRulesForm()) this._render();
      }
    } finally {
      this._refreshing = false;
    }
  }

  _scheduleRetryLoad() {
    if (this._retryLoadTimer) return;
    this._retryLoadTimer = window.setTimeout(() => {
      this._retryLoadTimer = undefined;
      this._load();
    }, 1500);
  }

  async _ack(ruleId) {
    await this._callWS({ type: "alarmgrid/acknowledge", rule_id: ruleId });
    await this._load();
  }

  async _ackAll() {
    await this._callWS({ type: "alarmgrid/acknowledge_all" });
    await this._load();
  }

  async _silence() {
    await this._callWS({ type: "alarmgrid/silence" });
    this._stopBrowserHorn();
    await this._load();
  }

  async _shelve(ruleId) {
    await this._callWS({
      type: "alarmgrid/shelve",
      rule_id: ruleId,
      duration_minutes: this._shelveDurationMinutes,
    });
    await this._load();
  }

  async _testSound() {
    this._audioEnabled = true;
    await this._callWS({ type: "alarmgrid/test_sound", priority: "critical" });
    await this._playBrowserHorn(true);
  }

  _maybePlayBrowserHorn() {
    if (!this._sound?.horn_active || !this._audioEnabled) return;
    const now = Date.now();
    if (now - this._lastBrowserHornAt < this._browserHornCooldownMs) return;
    this._lastBrowserHornAt = now;
    this._playBrowserHorn();
  }

  async _playBrowserHorn(once = false) {
    if (!this._audioEnabled && !once) return;
    try {
      const context = this._audioContext || new AudioContext();
      this._audioContext = context;
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      oscillator.type = "square";
      oscillator.frequency.setValueAtTime(880, context.currentTime);
      gain.gain.setValueAtTime(0.0001, context.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.22, context.currentTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.35);
      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start();
      oscillator.stop(context.currentTime + 0.38);
    } catch (err) {
      this._audioEnabled = false;
    }
  }

  _stopBrowserHorn() {
    this._sound = { ...this._sound, horn_active: false };
  }

  _filteredAlarms() {
    const search = this._search.trim().toLowerCase();
    return this._alarms
      .filter((alarm) => {
        if (this._tab === "active" && !["ACTIVE_UNACK", "ACTIVE_ACK", "CLEARED_UNACK"].includes(alarm.lifecycle_state)) return false;
        if (this._tab === "unacknowledged" && !["ACTIVE_UNACK", "CLEARED_UNACK"].includes(alarm.lifecycle_state)) return false;
        if (this._tab === "shelved" && alarm.lifecycle_state !== "SHELVED") return false;
        if (this._tab === "disabled" && alarm.lifecycle_state !== "DISABLED") return false;
        if (this._priority !== "all" && alarm.priority !== this._priority) return false;
        if (!search) return true;
        return [alarm.tag, alarm.name, alarm.entity_id, alarm.area, alarm.system]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
          .includes(search);
      })
      .sort((a, b) => (b.severity - a.severity) || String(a.active_since || "").localeCompare(String(b.active_since || "")));
  }

  _render() {
    if (!this.shadowRoot) return;
    this._builderRevision += 1;
    this._syncTheme();
    this._captureTableScroll();
    const visible = this._filteredAlarms();
    this.shadowRoot.innerHTML = `
      <style>${this._styles()}</style>
      <main class="panel theme-${this._effectiveTheme}">
        ${this._headerView()}
        ${this._tabsView()}
        ${this._error ? `<div class="error">${this._escape(this._error)}</div>` : ""}
        ${this._tab === "history" ? this._historyView() : ""}
        ${this._tab === "rules" ? this._rulesView() : ""}
        ${this._tab === "settings" ? this._settingsView() : ""}
        ${["active", "unacknowledged", "shelved", "disabled"].includes(this._tab) ? this._alarmView(visible) : ""}
      </main>
    `;
    this._wire();
    this._restoreTableScroll();
    this._rendered = true;
  }

  _syncTheme() {
    const previousTheme = this._effectiveTheme;
    const mode = ["auto", "light", "dark"].includes(this._themeMode) ? this._themeMode : "auto";
    const hassDarkMode = this._hassUsesDarkTheme();
    this._effectiveTheme = mode === "auto" ? (hassDarkMode ? "dark" : "light") : mode;
    if (this._rendered && previousTheme !== this._effectiveTheme) {
      queueMicrotask(() => this._render());
    }
  }

  _hassUsesDarkTheme() {
    const darkMode = this._hass?.themes?.darkMode;
    if (typeof darkMode === "boolean") return darkMode;
    if (typeof darkMode === "string") {
      const normalized = darkMode.trim().toLowerCase();
      if (["dark", "true", "1", "yes", "on"].includes(normalized)) return true;
      if (["light", "false", "0", "no", "off"].includes(normalized)) return false;
    }
    const colorScheme = this._hass?.selectedTheme?.theme?.colors?.["color-scheme"];
    if (typeof colorScheme === "string") {
      const normalized = colorScheme.trim().toLowerCase();
      if (normalized.includes("dark")) return true;
      if (normalized.includes("light")) return false;
    }
    const root = this.getRootNode?.();
    const host = root?.host;
    if (host?.classList?.contains("dark") || document.documentElement.classList.contains("dark")) return true;
    if (host?.classList?.contains("light") || document.documentElement.classList.contains("light")) return false;
    return window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false;
  }

  _headerView() {
    if (this._hideHeader) return "";
    return `
      <header class="topbar">
        ${this._narrow ? `<button class="secondary menu-button" data-action="toggle-menu" aria-label="${this._t("open_sidebar")}">${this._t("menu")}</button>` : ""}
        <div>
          <h1>${this._escape(this._title || this._t("default_title"))}</h1>
          <div class="metrics">
            <span>${this._t("metric_active", { count: this._alarms.filter((a) => ["ACTIVE_UNACK", "ACTIVE_ACK"].includes(a.lifecycle_state)).length })}</span>
            <span>${this._t("metric_unack", { count: this._alarms.filter((a) => ["ACTIVE_UNACK", "CLEARED_UNACK"].includes(a.lifecycle_state)).length })}</span>
            <span class="${this._sound.horn_active ? "horn on" : "horn"}">${this._sound.horn_active ? this._t("horn_active") : this._t("horn_idle")}</span>
          </div>
        </div>
        <div class="actions">
          ${!this._audioEnabled ? `<button class="secondary" data-action="enable-audio">${this._t("enable_alarm_sound")}</button>` : ""}
          <button class="danger" data-action="silence">${this._t("silence")}</button>
          <button class="primary" data-action="ack-all">${this._t("ack_all")}</button>
        </div>
      </header>
    `;
  }

  _tabsView() {
    if (this._hideTabs) return "";
    return `<nav class="tabs">${this._tabs()}</nav>`;
  }

  _tabs() {
    const tabs = [
      ["active", this._t("tab_active")],
      ["unacknowledged", this._t("tab_unacknowledged")],
      ["history", this._t("tab_history")],
      ["shelved", this._t("tab_shelved")],
      ["disabled", this._t("tab_disabled")],
      ["rules", this._t("tab_rules")],
      ["settings", this._t("tab_settings")],
    ];
    return tabs.map(([id, label]) => `<button class="${this._tab === id ? "selected" : ""}" data-tab="${id}">${label}</button>`).join("");
  }

  _shelveDurationOptions() {
    return [
      [60, this._t("duration_1h")],
      [240, this._t("duration_4h")],
      [480, this._t("duration_8h")],
      [1440, this._t("duration_1d")],
      [4320, this._t("duration_3d")],
      [10080, this._t("duration_7d")],
    ];
  }

  _alarmView(alarms) {
    return `
      <section class="toolbar">
        <input type="search" placeholder="${this._t("search_placeholder")}" value="${this._escape(this._search)}" data-field="search">
        <select data-field="priority">
          ${["all", "critical", "high", "medium", "low", "info", "status"].map((priority) => `<option value="${priority}" ${this._priority === priority ? "selected" : ""}>${this._t(`priority_${priority}`)}</option>`).join("")}
        </select>
        <label class="shelve-duration">${this._t("shelve_for")}
          <select data-field="shelve-duration">
            ${this._shelveDurationOptions().map(([minutes, label]) => `<option value="${minutes}" ${this._shelveDurationMinutes === minutes ? "selected" : ""}>${label}</option>`).join("")}
          </select>
        </label>
        <button data-action="refresh">${this._t("refresh")}</button>
      </section>
      <section class="table-shell">
        <table data-table-id="alarms">
          <thead>
            <tr>
              <th>${this._t("col_time")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_area")}</th><th>${this._t("col_system")}</th><th>${this._t("col_tag")}</th><th>${this._t("col_alarm")}</th><th>${this._t("col_source_value")}</th><th>${this._t("col_state")}</th><th>${this._t("col_shelved_until")}</th><th>${this._t("col_ack")}</th><th>${this._t("col_shelve")}</th><th>${this._t("col_instructions")}</th>
            </tr>
          </thead>
          <tbody>
            ${alarms.length ? alarms.map((alarm) => this._alarmRow(alarm)).join("") : `<tr><td colspan="12" class="empty">${this._t("no_alarms")}</td></tr>`}
          </tbody>
        </table>
      </section>
    `;
  }

  _alarmRow(alarm) {
    const stateClass = this._alarmStateClass(alarm);
    const flash = stateClass !== "state-pending-color" && (alarm.lifecycle_state === "ACTIVE_UNACK" || alarm.lifecycle_state === "CLEARED_UNACK");
    return `
      <tr class="alarm-row priority-${alarm.priority} ${stateClass} ${flash ? "flash" : ""}">
        <td>${this._time(alarm.active_since || alarm.cleared_at)}</td>
        <td><span class="badge">${this._t(`priority_${alarm.priority}`)}</span></td>
        <td>${this._escape(alarm.area || "")}</td>
        <td>${this._escape(alarm.system || "")}</td>
        <td>${this._escape(alarm.tag || alarm.id)}</td>
        <td>${this._escape(alarm.name)}</td>
        <td>${this._escape(String(alarm.last_value ?? alarm.last_source_state ?? ""))}</td>
        <td>${this._lifecycleLabel(alarm.lifecycle_state)}</td>
        <td>${this._time(alarm.shelve_expiry)}</td>
        <td><button data-ack="${this._escape(alarm.id)}" ${alarm.acknowledged ? "disabled" : ""}>${this._t("ack")}</button></td>
        <td><button data-shelve="${this._escape(alarm.id)}" ${alarm.shelved || alarm.disabled ? "disabled" : ""}>${this._t("shelve")}</button></td>
        <td>${this._escape(alarm.instructions || "")}</td>
      </tr>
    `;
  }

  _historyView() {
    return `
      <section class="toolbar history-export">
        <label>${this._t("history_from")}
          <input type="datetime-local" data-history-range="start" value="${this._escape(this._historyStart)}">
        </label>
        <label>${this._t("history_to")}
          <input type="datetime-local" data-history-range="end" value="${this._escape(this._historyEnd)}">
        </label>
        <button class="primary" data-action="export-history">${this._t("download_history")}</button>
        ${this._historyExportResult ? `<span class="notice history-export-result">${this._escape(this._historyExportResult)}</span>` : ""}
      </section>
      <section class="table-shell">
        <table data-table-id="history">
          <thead><tr><th>${this._t("col_time")}</th><th>${this._t("col_event")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_area")}</th><th>${this._t("col_tag")}</th><th>${this._t("col_alarm")}</th><th>${this._t("col_from")}</th><th>${this._t("col_to")}</th><th>${this._t("col_operator")}</th></tr></thead>
          <tbody>
            ${this._history.length ? this._history.map((event) => `
              <tr>
                <td>${this._time(event.timestamp)}</td>
                <td>${this._escape(event.event_type)}</td>
                <td>${event.priority ? this._t(`priority_${event.priority}`) : ""}</td>
                <td>${this._escape(event.area || "")}</td>
                <td>${this._escape(event.tag || event.rule_id || "")}</td>
                <td>${this._escape(event.name || event.message || "")}</td>
                <td>${event.previous_state ? this._lifecycleLabel(event.previous_state) : ""}</td>
                <td>${event.new_state ? this._lifecycleLabel(event.new_state) : ""}</td>
                <td>${this._escape(event.operator || "")}</td>
              </tr>`).join("") : `<tr><td colspan="9" class="empty">${this._t("no_history")}</td></tr>`}
          </tbody>
        </table>
      </section>
    `;
  }

  _rulesView() {
    const ruleDraft = this._ruleDraft;
    const selectedRuleCount = this._selectedRuleIds.size;
    return `
      <section class="rules">
        <div class="rule-form">
          <input placeholder="${this._t("placeholder_rule_id")}" value="${this._escape(ruleDraft.id)}" data-new="id" ${this._editingRuleId ? "disabled" : ""}>
          <input placeholder="${this._t("placeholder_name")}" value="${this._escape(ruleDraft.name)}" data-new="name">
          <input placeholder="${this._t("placeholder_system")}" value="${this._escape(ruleDraft.system)}" data-new="system">
          <datalist id="entity-id-options">${this._entityOptions()}</datalist>
          <fieldset class="condition-builder"><legend>${this._t("condition_builder")}</legend>${this._conditionBuilder(ruleDraft)}</fieldset>
          <label>${this._t("alarm_delay")} <input type="number" min="0" data-new="delay_on_seconds" value="${ruleDraft.delay_on_seconds || 0}"> ${this._t("seconds")}</label>
          <label>${this._t("clear_delay")} <input type="number" min="0" data-new="delay_off_seconds" value="${ruleDraft.delay_off_seconds || 0}"> ${this._t("seconds")}</label>
          <select data-new="priority">
            ${["critical", "high", "medium", "low", "info", "status"].map((p) => `<option value="${p}" ${ruleDraft.priority === p ? "selected" : ""}>${this._t(`priority_${p}`)}</option>`).join("")}
          </select>
          <label>${this._t("telegram_notifications")}
            <select data-new="telegram_notification_policy">
              ${["inherit", "always", "never"].map((policy) => `<option value="${policy}" ${ruleDraft.telegram_notification_policy === policy ? "selected" : ""}>${this._t(`telegram_policy_${policy}`)}</option>`).join("")}
            </select>
          </label>
          ${this._editingRuleId
            ? `<button class="primary" data-action="update-rule">${this._t("save_rule")}</button>
          <button class="secondary" data-action="cancel-edit-rule">${this._t("cancel")}</button>`
            : `<button class="primary" data-action="create-rule">${this._t("add_rule")}</button>`}
        </div>
        ${this._editingRuleId ? `<div class="notice">${this._t("editing_rule", { id: this._escape(this._editingRuleId) })}</div>` : ""}
        ${this._rulesResult ? `<div class="notice">${this._escape(this._rulesResult)}</div>` : ""}
        <div class="bulk-actions">
          <span>${this._t("n_rules", { count: this._rules.length })}</span>
          <span>${this._t("n_selected", { count: selectedRuleCount })}</span>
          <span>${this._t("n_estimated_entities", { count: selectedRuleCount * 4 })}</span>
          <button class="danger" data-action="delete-selected-rules" ${selectedRuleCount ? "" : "disabled"}>${this._t("delete_selected")}</button>
          <button class="secondary" data-action="export-rules" ${this._rules.length ? "" : "disabled"}>${this._t("export_rules")}</button>
          <button class="secondary" data-action="choose-rules-csv">${this._t("import_rules")}</button>
          <input class="file-input" type="file" accept=".csv,text/csv" data-rules-csv>
          </div>
        <div class="table-shell">
          <table data-table-id="rules">
            <thead><tr><th></th><th>${this._t("col_id")}</th><th>${this._t("col_entity")}</th><th>${this._t("col_name")}</th><th>${this._t("col_area")}</th><th>${this._t("col_system")}</th><th>${this._t("col_condition")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_telegram")}</th><th>${this._t("col_enabled")}</th><th></th></tr></thead>
            <tbody>${this._rules.length ? this._rules.map((rule) => `<tr><td><input class="row-select" type="checkbox" data-rule-select="${this._escape(rule.id)}" ${this._selectedRuleIds.has(rule.id) ? "checked" : ""}></td><td>${this._escape(rule.id)}</td><td>${this._escape(rule.entity_id)}</td><td>${this._escape(rule.name)}</td><td>${this._escape(rule.area || "")}</td><td>${this._escape(rule.system || "")}</td><td>${this._escape(this._conditionSummary(rule))}</td><td>${this._t(`priority_${rule.priority}`)}</td><td>${this._t(`telegram_table_${rule.telegram_notification_policy || "inherit"}`)}</td><td>${rule.enabled ? this._t("yes") : this._t("no")}</td><td><button data-edit-rule="${this._escape(rule.id)}">${this._t("edit")}</button></td></tr>`).join("") : `<tr><td colspan="11" class="empty">${this._t("no_rules")}</td></tr>`}</tbody>
          </table>
        </div>
      </section>
    `;
  }

  _operatorOptions(selected) {
    const en = {above:"Above",below:"Below",greater_or_equal:"At or above",less_or_equal:"At or below",equal:"Equal",not_equal:"Not equal",contains:"Contains",is_on:"Is ON",is_off:"Is OFF",state_changed:"Changed",unavailable:"Unavailable",between:"Between",outside_range:"Outside range"};
    const it = {above:"Maggiore di",below:"Minore di",greater_or_equal:"Maggiore o uguale",less_or_equal:"Minore o uguale",equal:"Uguale",not_equal:"Diverso",contains:"Contiene",is_on:"È ON",is_off:"È OFF",state_changed:"Cambiato",unavailable:"Non disponibile",between:"Compreso tra",outside_range:"Fuori intervallo"};
    const labels = this._language() === "it" ? it : en;
    return Object.entries(labels).map(([value,label]) => `<option value="${value}" ${selected === value ? "selected" : ""}>${label}</option>`).join("");
  }

  _conditionRow(node, path) {
    const needsValue = !["is_on","is_off","state_changed","unavailable"].includes(node.operator);
    const range = ["between","outside_range"].includes(node.operator);
    const numeric = ["above","below","greater_or_equal","less_or_equal","between","outside_range"].includes(node.operator);
    const state = this._hass?.states?.[node.entity_id];
    const current = state ? `${state.state}${state.attributes?.unit_of_measurement ? ` ${state.attributes.unit_of_measurement}` : ""}` : "—";
    return `<div class="condition-row" data-condition-path="${path}">
      <input aria-label="Entity" list="entity-id-options" value="${this._escape(node.entity_id || "")}" data-condition-field="entity_id">
      <select aria-label="Operator" data-condition-field="operator">${this._operatorOptions(node.operator)}</select>
      ${needsValue ? range ? `<input type="number" aria-label="Lower" value="${node.lower ?? ""}" data-condition-field="lower"><input type="number" aria-label="Upper" value="${node.upper ?? ""}" data-condition-field="upper">` : `<input aria-label="Value" value="${node.value ?? ""}" data-condition-field="value">` : ""}
      ${numeric ? `<label>${this._t("deadband_hysteresis")}<input type="number" min="0" step="any" value="${node.deadband || 0}" data-condition-field="deadband" title="${this._t("hysteresis_help")}"></label>` : ""}
      <small>${this._t("current_state")}: ${this._escape(current)}</small><button type="button" data-delete-condition="${path}" title="${this._t("delete_condition")}">×</button></div>`;
  }

  _groupBuilder(group, path="root") {
    if (!group || group.type !== "group" || !Array.isArray(group.conditions)) return "";
    return `<div class="condition-group ${path === "root" ? "root" : ""}" data-group-path="${path}"><div class="group-head"><select data-group-operator="${path}"><option value="and" ${group.operator === "and" ? "selected" : ""}>${this._t("all_conditions")}</option><option value="or" ${group.operator === "or" ? "selected" : ""}>${this._t("any_condition")}</option></select>${path === "root" ? "" : `<button type="button" data-delete-group="${path}">${this._t("delete_group")}</button>`}</div>${group.conditions.map((node,index) => node?.type === "group" ? this._groupBuilder(node, `${path}.${index}`) : node?.type === "condition" ? this._conditionRow(node, `${path}.${index}`) : "").join("")}<div class="group-actions"><button type="button" data-add-condition="${path}">${this._t("add_condition")}</button><button type="button" data-add-group="${path}">${this._t("add_group")}</button></div></div>`;
  }

  _conditionBuilder(draft) {
    if (draft.condition_expression) return this._groupBuilder(draft.condition_expression);
    const leaf = {entity_id:draft.entity_id,operator:draft.condition,value:draft.threshold,deadband:draft.deadband || 0};
    return `${this._conditionRow(leaf, "simple")}<button type="button" data-add-condition="simple">${this._t("add_condition")}</button><button type="button" data-add-group="simple">${this._t("add_group")}</button>`;
  }

  _conditionSummary(rule) {
    if (!rule.condition_expression) return `${rule.entity_id || ""} ${rule.condition || ""} ${rule.threshold ?? ""}`.trim();
    const count = (node) => node.type === "condition" ? 1 : node.conditions.reduce((total, child) => total + count(child), 0);
    return `${count(rule.condition_expression)} conditions · ${rule.condition_expression.operator.toUpperCase()}`;
  }

  _expressionNode(path) {
    const root = this._ruleDraft?.condition_expression;
    if (!path || typeof path !== "string" || !root || typeof root !== "object" || Array.isArray(root)) return null;
    if (path === "root") return root;
    const parts = path.split(".");
    if (parts[0] !== "root" || parts.length < 2) return null;
    let node = root;
    for (const part of parts.slice(1)) {
      const index = Number(part);
      if (part === "" || node?.type !== "group" || !Array.isArray(node.conditions) || !Number.isInteger(index) || index < 0 || index >= node.conditions.length) return null;
      node = node.conditions[index];
      if (!node || typeof node !== "object" || Array.isArray(node)) return null;
    }
    return node;
  }

  _expressionGroup(path) {
    const node = this._expressionNode(path);
    return node?.type === "group" && Array.isArray(node.conditions) ? node : null;
  }

  _expressionCondition(path) {
    const node = this._expressionNode(path);
    return node?.type === "condition" ? node : null;
  }

  _resolveExpressionParent(path) {
    if (!path || typeof path !== "string" || path === "root") return null;
    const parts = path.split(".");
    const indexPart = parts.pop();
    const index = Number(indexPart);
    if (indexPart === "" || !Number.isInteger(index) || index < 0) return null;
    const parent = this._expressionGroup(parts.join("."));
    if (!parent || index >= parent.conditions.length) return null;
    const node = parent.conditions[index];
    if (!node || typeof node !== "object" || Array.isArray(node)) return null;
    return {parent, index, node};
  }

  _addExpressionNode(path, addGroup) {
    this._promoteSimple();
    const group = this._expressionGroup(path === "simple" ? "root" : path);
    if (!group) return;
    group.conditions.push(addGroup ? {type:"group",operator:"and",conditions:[{type:"condition",entity_id:"",operator:"above",value:"",deadband:0}]} : {type:"condition",entity_id:"",operator:"above",value:"",deadband:0});
    this._render();
  }

  _deleteExpressionNode(path, deleteGroup) {
    if (path === "root") return;
    const resolved = this._resolveExpressionParent(path);
    if (!resolved) return;
    if (deleteGroup) {
      if (resolved.node.type !== "group" || !Array.isArray(resolved.node.conditions)) return;
      if (resolved.node.conditions.length > 1 && !confirm(this._t("delete_group"))) return;
    } else if (resolved.node.type !== "condition") return;
    resolved.parent.conditions.splice(resolved.index, 1);
    this._render();
  }

  _promoteSimple() {
    if (!this._ruleDraft.condition_expression) this._ruleDraft.condition_expression = {type:"group",operator:"and",conditions:[{type:"condition",entity_id:this._ruleDraft.entity_id,operator:this._ruleDraft.condition,value:this._ruleDraft.threshold,deadband:Number(this._ruleDraft.deadband || 0)}]};
  }

  _entityOptions() {
    const states = this._hass?.states || {};
    return Object.keys(states)
      .sort()
      .map((entityId) => {
        const friendlyName = states[entityId]?.attributes?.friendly_name;
        const label = friendlyName ? ` label="${this._escape(friendlyName)}"` : "";
        return `<option value="${this._escape(entityId)}"${label}></option>`;
      })
      .join("");
  }

  _entityAreaName(entityId) {
    if (!entityId || !this._hass) return null;
    const entityEntry = this._hass.entities?.[entityId];
    const areaId = entityEntry?.area_id
      || (entityEntry?.device_id ? this._hass.devices?.[entityEntry.device_id]?.area_id : null);
    if (!areaId) return null;
    return this._hass.areas?.[areaId]?.name || null;
  }

  _settingsView() {
    return `
      <section class="settings">
        <dl>
          <dt>${this._t("sound_mode")}</dt><dd>${this._escape(this._sound.sound_mode || "browser_only")}</dd>
          <dt>${this._t("browser_sound")}</dt><dd>${this._sound.browser_enabled ? this._t("enabled") : this._t("disabled")}</dd>
          <dt>${this._t("media_player_sound")}</dt><dd>${this._sound.media_player_enabled ? this._t("enabled") : this._t("disabled")}</dd>
          <dt>${this._t("active_audible")}</dt><dd>${(this._sound.active_audible_alarms || []).length}</dd>
        </dl>
        <button data-action="test-sound">${this._t("test_sound")}</button>
      </section>
    `;
  }

  _wire() {
    const builderRevision = this._builderRevision;
    this.shadowRoot.querySelectorAll("[data-tab]").forEach((button) => {
      button.addEventListener("click", () => {
        this._tab = button.dataset.tab;
        this._render();
      });
    });
    this.shadowRoot.querySelector("[data-action='ack-all']")?.addEventListener("click", () => this._ackAll());
    this.shadowRoot.querySelector("[data-action='silence']")?.addEventListener("click", () => this._silence());
    this.shadowRoot.querySelector("[data-action='refresh']")?.addEventListener("click", () => this._load());
    this.shadowRoot.querySelector("[data-action='export-history']")?.addEventListener("click", () => this._exportHistory());
    this.shadowRoot.querySelector("[data-action='toggle-menu']")?.addEventListener("click", () => this._toggleSidebar());
    this.shadowRoot.querySelector("[data-action='enable-audio']")?.addEventListener("click", () => this._testSound());
    this.shadowRoot.querySelector("[data-action='test-sound']")?.addEventListener("click", () => this._testSound());
    this.shadowRoot.querySelector("[data-action='create-rule']")?.addEventListener("click", () => this._createRule());
    this.shadowRoot.querySelector("[data-action='update-rule']")?.addEventListener("click", () => this._updateRule());
    this.shadowRoot.querySelector("[data-action='cancel-edit-rule']")?.addEventListener("click", () => this._cancelEditRule());
    this.shadowRoot.querySelectorAll("[data-edit-rule]").forEach((button) => button.addEventListener("click", () => this._startEditRule(button.dataset.editRule)));
    this.shadowRoot.querySelector("[data-action='delete-selected-rules']")?.addEventListener("click", () => this._deleteSelectedRules());
    this.shadowRoot.querySelector("[data-action='export-rules']")?.addEventListener("click", () => this._exportRules());
    this.shadowRoot.querySelector("[data-action='choose-rules-csv']")?.addEventListener("click", () => this.shadowRoot.querySelector("[data-rules-csv]")?.click());
    this.shadowRoot.querySelector("[data-rules-csv]")?.addEventListener("change", (event) => this._importRules(event.target.files?.[0]));
    this.shadowRoot.querySelectorAll("[data-new]").forEach((field) => {
      const updateDraft = () => {
        this._ruleDraft[field.dataset.new] = field.value;
      };
      field.addEventListener("input", updateDraft);
      field.addEventListener("change", updateDraft);
    });
    this.shadowRoot.querySelectorAll("[data-condition-field]").forEach((field) => field.addEventListener("change", () => {
      if (builderRevision !== this._builderRevision) return;
      const path = field.closest("[data-condition-path]")?.dataset.conditionPath;
      if (!path) return;
      if (path === "simple") { const map = {value:"threshold"}; this._ruleDraft[map[field.dataset.conditionField] || field.dataset.conditionField] = field.value; return; }
      const node = this._expressionCondition(path); if (!node) return;
      node[field.dataset.conditionField] = ["lower","upper","deadband"].includes(field.dataset.conditionField) ? Number(field.value) : field.value;
    }));
    this.shadowRoot.querySelectorAll("[data-group-operator]").forEach((field) => field.addEventListener("change", () => {
      if (builderRevision !== this._builderRevision || !["and", "or"].includes(field.value)) return;
      const group = this._expressionGroup(field.dataset.groupOperator); if (group) group.operator = field.value;
    }));
    this.shadowRoot.querySelectorAll("[data-add-condition],[data-add-group]").forEach((button) => button.addEventListener("click", () => {
      if (builderRevision !== this._builderRevision) return;
      const path = button.dataset.addCondition ?? button.dataset.addGroup;
      this._addExpressionNode(path, button.dataset.addGroup !== undefined);
    }));
    this.shadowRoot.querySelectorAll("[data-delete-condition],[data-delete-group]").forEach((button) => button.addEventListener("click", () => {
      if (builderRevision !== this._builderRevision) return;
      const path = button.dataset.deleteCondition ?? button.dataset.deleteGroup;
      this._deleteExpressionNode(path, button.dataset.deleteGroup !== undefined);
    }));
    this.shadowRoot.querySelectorAll("[data-history-range]").forEach((field) => {
      field.addEventListener("change", () => {
        if (field.dataset.historyRange === "start") this._historyStart = field.value;
        else this._historyEnd = field.value;
        this._historyExportResult = "";
      });
    });
    this.shadowRoot.querySelectorAll("[data-rule-select]").forEach((field) => {
      field.addEventListener("change", () => {
        this._setMembership(this._selectedRuleIds, field.dataset.ruleSelect, field.checked);
        this._render();
      });
    });
    this.shadowRoot.querySelector("[data-field='search']")?.addEventListener("input", (event) => {
      this._search = event.target.value;
      this._render();
    });
    this.shadowRoot.querySelector("[data-field='priority']")?.addEventListener("change", (event) => {
      this._priority = event.target.value;
      this._render();
    });
    this.shadowRoot.querySelector("[data-field='shelve-duration']")?.addEventListener("change", (event) => {
      const minutes = Number(event.target.value);
      const validDurations = new Set(this._shelveDurationOptions().map(([value]) => value));
      this._shelveDurationMinutes = validDurations.has(minutes) ? minutes : 60;
    });
    this.shadowRoot.querySelectorAll("[data-ack]").forEach((button) => button.addEventListener("click", () => this._ack(button.dataset.ack)));
    this.shadowRoot.querySelectorAll("[data-shelve]").forEach((button) => button.addEventListener("click", () => this._shelve(button.dataset.shelve)));
    this._wireColumnResizers();
  }

  async _createRule() {
    const fields = { ...this._ruleDraft };
    Object.keys(fields).forEach((key) => {
      if (fields[key] === "") delete fields[key];
    });
    if (fields.threshold !== undefined && fields.threshold !== "") fields.threshold = Number(fields.threshold);
    const areaName = this._entityAreaName(fields.entity_id);
    if (areaName) fields.area = areaName;
    await this._callWS({ type: "alarmgrid/create_rule", rule: fields });
    this._resetRuleDraft();
    await this._load();
  }

  _resetRuleDraft() {
    this._editingRuleId = null;
    this._ruleDraft = {
      id: "",
      entity_id: "",
      name: "",
      condition: "above",
      threshold: "",
      priority: "medium",
      telegram_notification_policy: "inherit",
      system: "",
      deadband: 0, delay_on_seconds: 0, delay_off_seconds: 0, condition_expression: null,
    };
  }

  _startEditRule(ruleId) {
    const rule = this._rules.find((item) => item.id === ruleId);
    if (!rule) return;
    this._editingRuleId = ruleId;
    this._ruleDraft = {
      id: rule.id || "",
      entity_id: rule.entity_id || "",
      name: rule.name || "",
      condition: rule.condition || "above",
      threshold: rule.threshold ?? "",
      priority: rule.priority || "medium",
      telegram_notification_policy: rule.telegram_notification_policy || "inherit",
      system: rule.system || "",
      deadband: rule.deadband || 0, delay_on_seconds: rule.delay_on_seconds || 0, delay_off_seconds: rule.delay_off_seconds || 0,
      condition_expression: rule.condition_expression ? structuredClone(rule.condition_expression) : null,
    };
    this._render();
    this.shadowRoot.querySelector("[data-new='entity_id']")?.focus();
  }

  _cancelEditRule() {
    this._resetRuleDraft();
    this._render();
  }

  async _updateRule() {
    if (!this._editingRuleId) return;
    const changes = { ...this._ruleDraft };
    delete changes.id;
    if (changes.system === "") changes.system = null;
    Object.keys(changes).forEach((key) => {
      if (changes[key] === "") delete changes[key];
    });
    if (changes.threshold !== undefined && changes.threshold !== null) changes.threshold = Number(changes.threshold);
    const areaName = this._entityAreaName(changes.entity_id);
    if (areaName) changes.area = areaName;
    try {
      await this._callWS({
        type: "alarmgrid/update_rule",
        rule_id: this._editingRuleId,
        changes,
      });
      this._rulesResult = this._t("rule_updated", { id: this._editingRuleId });
      this._resetRuleDraft();
      await this._load();
    } catch (err) {
      this._rulesResult = err.message || String(err);
      this._render();
    }
  }

  _toggleSidebar() {
    this.dispatchEvent(new CustomEvent("hass-toggle-menu", {
      detail: { open: true },
      bubbles: true,
      composed: true,
    }));
  }


  async _deleteSelectedRules() {
    const ruleIds = [...this._selectedRuleIds];
    await this._deleteRules({ rule_ids: ruleIds }, ruleIds.length, this._t("label_selected_rules"));
  }

  async _exportRules() {
    try {
      const result = await this._callWS({ type: "alarmgrid/export_rules" });
      const blob = new Blob([result?.csv || ""], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `alarmgrid-rules-${new Date().toISOString().slice(0, 10)}.csv`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      this._rulesResult = err.message || String(err);
      this._render();
    }
  }

  async _exportHistory() {
    if (!this._historyStart || !this._historyEnd) {
      this._historyExportResult = this._t("history_range_required");
      this._render();
      return;
    }
    const start = new Date(this._historyStart);
    const end = new Date(this._historyEnd);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || end <= start) {
      this._historyExportResult = this._t("history_range_invalid");
      this._render();
      return;
    }
    try {
      const result = await this._callWS({
        type: "alarmgrid/export_history",
        start_time: start.toISOString(),
        end_time: end.toISOString(),
        format: "csv",
      });
      const rows = result?.rows || [];
      const columns = ["timestamp", "event_type", "priority", "area", "system", "tag", "rule_id", "entity_id", "name", "previous_state", "new_state", "source_state", "source_value", "message", "operator"];
      const csvCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
      const csv = [columns, ...rows.map((row) => columns.map((column) => row[column]))]
        .map((row) => row.map(csvCell).join(","))
        .join("\r\n");
      const blob = new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `alarmgrid-history-${this._historyStart.replaceAll(":", "-")}-${this._historyEnd.replaceAll(":", "-")}.csv`;
      link.click();
      URL.revokeObjectURL(url);
      this._historyExportResult = this._t("history_exported", { count: rows.length });
    } catch (err) {
      this._historyExportResult = err.message || String(err);
    }
    this._render();
  }

  async _importRules(file) {
    if (!file || (!file.name.toLowerCase().endsWith(".csv") && file.type !== "text/csv")) {
      this._rulesResult = this._t("invalid_csv_file");
      this._render();
      return;
    }
    try {
      const result = await this._callWS({
        type: "alarmgrid/import_rules",
        csv: await file.text(),
      });
      this._rulesResult = this._t("imported_rules", {
        count: result?.imported_count || 0,
        created: result?.created_ids?.length || 0,
        updated: result?.updated_ids?.length || 0,
      });
      await this._load();
    } catch (err) {
      this._rulesResult = err.message || String(err);
      this._render();
    }
  }


  async _deleteRules(payload, count, label) {
    if (!count) {
      this._rulesResult = this._t("no_items_to_delete", { label });
      this._render();
      return;
    }
    const estimatedEntities = count * 4;
    if (!window.confirm(this._t("confirm_delete_rules", { count, label, entities: estimatedEntities }))) return;
    try {
      const result = await this._callWS({
        type: "alarmgrid/delete_rules",
        ...payload,
      });
      const deletedCount = result?.deleted_count || 0;
      const removedEntityCount = result?.removed_entity_count || 0;
      const skippedCount = result?.skipped_rule_ids?.length || 0;
      this._rulesResult = `${this._t("deleted_rules", { count: deletedCount, entities: removedEntityCount })}${skippedCount ? this._t("skipped_suffix", { count: skippedCount }) : ""}`;
      this._selectedRuleIds = new Set();
      await this._load();
    } catch (err) {
      this._rulesResult = err.message || String(err);
      this._render();
    }
  }


  _setMembership(set, value, selected) {
    if (!value) return;
    if (selected) set.add(value);
    else set.delete(value);
  }

  _isEditingRulesForm() {
    const active = this.shadowRoot?.activeElement;
    if (this._tab !== "rules" || !active) return false;
    return Boolean(active.matches("[data-new]"));
  }

  _alarmStateClass(alarm) {
    const lifecycle = String(alarm.lifecycle_state || "NORMAL");
    const stateClass = `state-${lifecycle.toLowerCase().replace(/_/g, "-")}`;
    if (!["ACTIVE_UNACK", "CLEARED_UNACK"].includes(lifecycle)) return stateClass;
    if (this._isAlarmVisualDelayElapsed(alarm, lifecycle)) return stateClass;
    this._scheduleAlarmVisualRefresh();
    return "state-pending-color";
  }

  _isAlarmVisualDelayElapsed(alarm, lifecycle) {
    const timestamp = Date.parse(alarm.active_since || alarm.cleared_at || "");
    if (!Number.isNaN(timestamp)) {
      return Date.now() - timestamp >= this._alarmVisualDelayMs;
    }
    const key = `${alarm.id || alarm.entity_id || alarm.name}:${lifecycle}`;
    this._alarmFirstSeenAt[key] = this._alarmFirstSeenAt[key] || Date.now();
    return Date.now() - this._alarmFirstSeenAt[key] >= this._alarmVisualDelayMs;
  }

  _scheduleAlarmVisualRefresh() {
    if (this._alarmVisualRefreshTimer) return;
    this._alarmVisualRefreshTimer = window.setTimeout(() => {
      this._alarmVisualRefreshTimer = undefined;
      if (!this._isEditingRulesForm()) this._render();
    }, this._alarmVisualDelayMs);
  }

  _captureTableScroll() {
    this.shadowRoot.querySelectorAll("table[data-table-id]").forEach((table) => {
      const shell = table.closest(".table-shell");
      if (shell) this._tableScrollLeft[table.dataset.tableId] = shell.scrollLeft;
    });
  }

  _restoreTableScroll() {
    const restore = () => {
      this.shadowRoot.querySelectorAll("table[data-table-id]").forEach((table) => {
        const shell = table.closest(".table-shell");
        const scrollLeft = this._tableScrollLeft[table.dataset.tableId];
        if (shell && scrollLeft !== undefined) shell.scrollLeft = scrollLeft;
      });
    };
    if (typeof requestAnimationFrame === "function") requestAnimationFrame(restore);
    else restore();
  }

  _wireColumnResizers() {
    this.shadowRoot.querySelectorAll("table").forEach((table, tableIndex) => {
      const tableId = table.dataset.tableId || `table-${tableIndex}`;
      const headers = Array.from(table.querySelectorAll("thead th"));
      if (!headers.length) return;
      let colgroup = table.querySelector("colgroup");
      if (!colgroup) {
        colgroup = document.createElement("colgroup");
        headers.forEach(() => colgroup.appendChild(document.createElement("col")));
        table.insertBefore(colgroup, table.firstElementChild);
      }
      const columns = Array.from(colgroup.children);
      const savedWidths = this._columnWidths[tableId] || {};
      headers.forEach((header, index) => {
        const savedWidth = savedWidths[index];
        if (savedWidth) {
          header.style.width = `${savedWidth}px`;
          if (columns[index]) columns[index].style.width = `${savedWidth}px`;
        }
        header.classList.add("resizable-column");
        if (header.querySelector(".col-resizer")) return;
        const handle = document.createElement("span");
        handle.className = "col-resizer";
        handle.addEventListener("pointerdown", (event) => {
          event.preventDefault();
          event.stopPropagation();
          const startX = event.clientX;
          const startWidth = header.getBoundingClientRect().width;
          const column = columns[index];
          const onMove = (moveEvent) => {
            const width = Math.max(72, startWidth + moveEvent.clientX - startX);
            this._columnWidths[tableId] = this._columnWidths[tableId] || {};
            this._columnWidths[tableId][index] = width;
            header.style.width = `${width}px`;
            if (column) column.style.width = `${width}px`;
          };
          const onUp = () => {
            document.removeEventListener("pointermove", onMove);
            document.removeEventListener("pointerup", onUp);
            document.removeEventListener("pointercancel", onUp);
          };
          document.addEventListener("pointermove", onMove);
          document.addEventListener("pointerup", onUp, { once: true });
          document.addEventListener("pointercancel", onUp, { once: true });
        });
        header.appendChild(handle);
      });
    });
  }

  _time(value) {
    if (!value) return "";
    try {
      return new Date(value).toLocaleString();
    } catch (_err) {
      return value;
    }
  }

  _escape(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    })[char]);
  }

  _styles() {
    return `
      :host { display: block; color: var(--ag-text); background: var(--ag-bg); min-height: var(--ag-min-height, 100vh); font-family: Arial, sans-serif; }
      .panel { min-height: var(--ag-min-height, 100vh); background: var(--ag-bg); color: var(--ag-text); }
      .theme-dark {
        --ag-bg: #101316; --ag-surface: #11161b; --ag-surface-alt: #14191f; --ag-header: #181d22; --ag-control: #202832; --ag-control-hover: #2a3541; --ag-text: #e6edf3; --ag-muted: #9fb1c1; --ag-heading-muted: #b8c7d4; --ag-border: #303942; --ag-border-soft: #28323c; --ag-selected-bg: #d9e2ec; --ag-selected-text: #101316; --ag-row-neutral: #252c33; --ag-row-neutral-text: #aebdcc; --ag-row-pending: #202832; --ag-row-pending-text: #dbe4ec; --ag-notice: #dbeafe; --ag-error-bg: #5b1c1c; --ag-error-text: #ffd5d5; --ag-error-border: #a83737;
      }
      .theme-light {
        --ag-bg: #f5f7fb; --ag-surface: #ffffff; --ag-surface-alt: #eef3f8; --ag-header: #ffffff; --ag-control: #ffffff; --ag-control-hover: #e8eef6; --ag-text: #1f2937; --ag-muted: #526170; --ag-heading-muted: #425466; --ag-border: #d7e0ea; --ag-border-soft: #e3e9f0; --ag-selected-bg: #1d4ed8; --ag-selected-text: #ffffff; --ag-row-neutral: #eef2f7; --ag-row-neutral-text: #526170; --ag-row-pending: #e7edf5; --ag-row-pending-text: #334155; --ag-notice: #1e40af; --ag-error-bg: #fee2e2; --ag-error-text: #7f1d1d; --ag-error-border: #fca5a5;
      }
      .topbar { display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 14px 18px; background: var(--ag-header); border-bottom: 1px solid var(--ag-border); }
      .menu-button { display: none; flex: 0 0 auto; }
      h1 { margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0; }
      .metrics { display: flex; gap: 10px; margin-top: 6px; color: var(--ag-muted); font-size: 13px; }
      .horn.on { color: #ffcf33; font-weight: 700; }
      .actions, .toolbar, .tabs, .rule-form, .bulk-actions, .bulk-summary { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
      button, select, input { background: var(--ag-control); color: var(--ag-text); border: 1px solid var(--ag-border); min-height: 34px; border-radius: 4px; padding: 0 10px; font-size: 14px; }
      input { min-width: 260px; }
      button { cursor: pointer; }
      button:hover { background: var(--ag-control-hover); }
      button:disabled { opacity: .45; cursor: default; }
      .primary { background: #2563eb; border-color: #3473ff; color: #ffffff; }
      .primary:hover { background: #1d4ed8; }
      .danger { background: #9f1d1d; border-color: #d23b3b; color: #ffffff; }
      .danger:hover { background: #831717; }
      .secondary { background: #30515d; border-color: #4b7b8c; color: #ffffff; }
      .secondary:hover { background: #3c6373; }
      .tabs { padding: 10px 18px; background: var(--ag-surface-alt); border-bottom: 1px solid var(--ag-border-soft); }
      .tabs button.selected { background: var(--ag-selected-bg); color: var(--ag-selected-text); border-color: var(--ag-selected-bg); }
      .toolbar { padding: 12px 18px; }
      .shelve-duration { display: flex; gap: 6px; align-items: center; color: var(--ag-heading-muted); font-size: 13px; }
      .history-export label { display: grid; gap: 4px; color: var(--ag-heading-muted); font-size: 12px; }
      .history-export input { min-width: 210px; }
      .history-export-result { margin-top: 0; }      
      .table-shell { overflow: auto; padding: 0 18px 18px; }
      table { width: 100%; border-collapse: collapse; background: var(--ag-surface); table-layout: auto; }
      th, td { border-bottom: 1px solid var(--ag-border-soft); padding: 8px 9px; text-align: left; font-size: 13px; white-space: nowrap; }
      th { background: var(--ag-control); color: var(--ag-heading-muted); position: sticky; top: 0; z-index: 1; }
      td:nth-child(6), td:nth-child(12) { white-space: normal; min-width: 180px; }
      tr { border-left: 6px solid #4b5563; }
      .alarm-row { background: var(--ag-surface); color: var(--ag-text); }
      .alarm-row td { border-bottom-color: rgba(16, 19, 22, .35); }
      .alarm-row button { background: rgba(16, 19, 22, .22); color: inherit; border-color: rgba(16, 19, 22, .4); }
      .alarm-row button:hover { background: rgba(16, 19, 22, .34); }
      .alarm-row.priority-critical.state-active-unack { background: #ef2b1d; color: #101316; border-left-color: #8f1711; }
      .alarm-row.priority-high.state-active-unack { background: #ff9f00; color: #101316; border-left-color: #a85b00; }
      .alarm-row.priority-medium.state-active-unack { background: #ffd800; color: #101316; border-left-color: #b69100; }
      .alarm-row.priority-low.state-active-unack { background: #58a6ff; color: #101316; border-left-color: #1d5fa8; }
      .alarm-row.priority-info.state-active-unack { background: #83d2e6; color: #101316; border-left-color: #34899f; }
      .alarm-row.priority-status.state-active-unack { background: #7ee787; color: #101316; border-left-color: #2f8a39; }
      .alarm-row.state-pending-color { background: var(--ag-row-pending); color: var(--ag-row-pending-text); border-left-color: #687585; }
      .alarm-row.state-cleared-unack { background: #d85b9d; color: #101316; border-left-color: #8e2f63; }
      .alarm-row.state-active-ack, .alarm-row.state-cleared-ack { background: #f3f4f6; color: #1f2933; border-left-color: #9ca3af; }
      .alarm-row.state-shelved, .alarm-row.state-disabled, .alarm-row.state-normal { background: var(--ag-row-neutral); color: var(--ag-row-neutral-text); border-left-color: #596675; }
      .badge { text-transform: uppercase; font-size: 12px; font-weight: 700; }
      .flash { animation: flashRow 1s step-end infinite; }
      @keyframes flashRow { 50% { filter: brightness(1.25); } }
      .empty, .error { color: var(--ag-muted); padding: 18px; }
      .error { margin: 12px 18px; color: var(--ag-error-text); background: var(--ag-error-bg); border: 1px solid var(--ag-error-border); }
      .rules, .settings { padding: 12px 18px 18px; }
      .file-input { display: none; }
      .bulk-actions, .bulk-summary { margin-top: 8px; color: var(--ag-heading-muted); font-size: 13px; }
      .bulk-actions { margin-bottom: 10px; }
      .row-select { min-width: 0; width: 16px; height: 16px; padding: 0; }
      .notice { margin-top: 8px; color: var(--ag-notice); font-size: 13px; }
      .rule-form { margin-bottom: 12px; }
      .condition-builder { flex-basis:100%; border:1px solid var(--divider-color); border-radius:10px; padding:12px; }
      .condition-group { border-left:3px solid var(--primary-color); margin:8px 0; padding:8px; background:var(--card-background-color); }
      .condition-group .condition-group { margin-left:min(18px,3vw); } .group-head,.group-actions{display:flex;gap:8px;margin-bottom:8px}
      .condition-row { display:grid;grid-template-columns:minmax(150px,2fr) minmax(120px,1fr) repeat(2,minmax(90px,1fr)) auto auto;gap:8px;align-items:end;margin:8px 0; }
      .condition-row label{display:grid;font-size:.75rem}.condition-row small{align-self:center}
      @media(max-width:720px){.condition-row{grid-template-columns:1fr}.condition-group .condition-group{margin-left:8px}}
      .settings dl { display: grid; grid-template-columns: max-content minmax(120px, 1fr); gap: 10px 18px; max-width: 560px; }
      .settings dt { color: var(--ag-muted); }
      .settings dd { margin: 0; }
      .resizable-column { position: relative; min-width: 72px; padding-right: 16px; }
      .col-resizer { position: absolute; top: 0; right: 0; width: 8px; height: 100%; cursor: col-resize; touch-action: none; user-select: none; }
      .col-resizer:hover { background: rgba(255, 255, 255, .18); }
      @media (max-width: 720px) {
        .topbar { align-items: flex-start; flex-direction: column; }
        .menu-button { display: inline-flex; align-items: center; justify-content: center; }
        input { min-width: 0; width: 100%; }
        .actions, .toolbar, .rule-form { width: 100%; }
        .shelve-duration { width: 100%; }
        .shelve-duration select { flex: 1 1 auto; }
        button, select { flex: 1 1 auto; }
      }
    `;
  }
}

const EDITOR_TRANSLATIONS = {
  en: {
    editor_general: "General", editor_header: "Header", editor_content: "Content", editor_actions: "Actions", editor_appearance: "Advanced appearance",
    editor_title: "Title", editor_view: "View", editor_max_alarms: "Maximum alarms", editor_theme: "Theme", editor_show_header: "Show header",
    editor_header_icon: "Header icon", editor_show_header_icon: "Show header icon", editor_show_header_status: "Show header status", editor_show_header_actions: "Show header actions",
    editor_show_summary: "Show summary", editor_show_value: "Show value", editor_show_area: "Show area", editor_show_system: "Show system", editor_show_tag: "Show tag", editor_show_open_panel: "Show AlarmGrid link",
    editor_show_actions: "Show actions", editor_show_shelve: "Show shelve action", editor_show_disable: "Show disable action", editor_show_restore: "Show restore actions",
    editor_priorities: "Priorities", editor_min_height: "Minimum height", editor_supported_units: "Supported units: px, rem, em, %",
    active: "Active alarms", unacknowledged: "Unacknowledged", shelved: "Shelved", disabled_view: "Disabled", inactive: "Shelved + disabled",
  },
  it: {
    editor_general: "Generale", editor_header: "Header", editor_content: "Contenuto", editor_actions: "Azioni", editor_appearance: "Aspetto avanzato",
    editor_title: "Titolo", editor_view: "Vista", editor_max_alarms: "Numero massimo di allarmi", editor_theme: "Tema", editor_show_header: "Mostra header",
    editor_header_icon: "Icona header", editor_show_header_icon: "Mostra icona header", editor_show_header_status: "Mostra stato header", editor_show_header_actions: "Mostra azioni header",
    editor_show_summary: "Mostra riepilogo", editor_show_value: "Mostra valore", editor_show_area: "Mostra area", editor_show_system: "Mostra sistema", editor_show_tag: "Mostra tag", editor_show_open_panel: "Mostra link ad AlarmGrid",
    editor_show_actions: "Mostra azioni", editor_show_shelve: "Mostra azione sospendi", editor_show_disable: "Mostra azione disabilita", editor_show_restore: "Mostra azioni ripristino",
    editor_priorities: "Priorità", editor_min_height: "Altezza minima", editor_supported_units: "Unità supportate: px, rem, em, %",
    active: "Allarmi attivi", unacknowledged: "Non riconosciuti", shelved: "Sospesi", disabled_view: "Disabilitati", inactive: "Sospesi + disabilitati",
  },
};

class AlarmGridCardEditor extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._rendered = false;
    this._appearanceOpen = false;
  }

  setConfig(config = {}) {
    const nextConfig = { ...config };
    if (this._rendered && this._configsEqual(this._config, nextConfig)) return;
    this._config = nextConfig;
    // Normalize deprecated names only when the editor next emits a change.
    this._legacyView = config.view ?? config.tab;
    this._legacyShelve = config.show_shelve_action ?? config.show_shelve;
    if (!this._rendered) this._render();
    else this._syncControlsFromConfig();
  }

  set hass(hass) {
    const previousLanguage = this._language();
    this._hass = hass;
    const nextLanguage = this._language();
    if (!this._rendered) {
      this._render();
    } else if (previousLanguage !== nextLanguage) {
      this._renderPreservingUiState();
    }
  }

  _configsEqual(left, right) {
    const canonical = (value) => {
      if (Array.isArray(value)) return value.map(canonical);
      if (value && typeof value === "object") return Object.keys(value).sort().reduce((result, key) => {
        result[key] = canonical(value[key]);
        return result;
      }, {});
      return value;
    };
    return JSON.stringify(canonical(left)) === JSON.stringify(canonical(right));
  }

  _language() {
    const language = this._hass?.locale?.language || this._hass?.language || "en";
    return String(language).toLowerCase().split("-")[0] === "it" ? "it" : "en";
  }

  _t(key) { return EDITOR_TRANSLATIONS[this._language()][key] ?? key; }
  _value(name) {
    if (name === "view" && this._config.view === undefined) return this._legacyView ?? CARD_DEFAULTS.view;
    if (name === "show_shelve_action" && this._config[name] === undefined && this._legacyShelve !== undefined) return this._legacyShelve !== false;
    return this._config[name] ?? CARD_DEFAULTS[name];
  }

  _normalizedConfig() {
    const config = { ...this._config };
    if (config.view === undefined && this._legacyView !== undefined) config.view = this._legacyView;
    if (config.show_shelve_action === undefined && this._legacyShelve !== undefined) config.show_shelve_action = this._legacyShelve !== false;
    delete config.tab;
    delete config.hide_tabs;
    delete config.show_shelve;
    return config;
  }

  _commit(config) {
    this._config = config;
    this._legacyView = config.view;
    this._legacyShelve = config.show_shelve_action;
    this._emitConfigChanged();
    this._syncDependentControls();
  }

  _setBooleanOption(name, checked, defaultValue = true) {
    const newConfig = this._normalizedConfig();
    if (checked === defaultValue) delete newConfig[name]; else newConfig[name] = checked;
    this._commit(newConfig);
  }

  _setStringOption(name, value, defaultValue = "") {
    const newConfig = this._normalizedConfig();
    const normalized = value.trim();
    if (!normalized || normalized === defaultValue) delete newConfig[name]; else newConfig[name] = normalized;
    this._commit(newConfig);
  }

  _setNumberOption(name, value, defaultValue = 5) {
    const number = Math.max(0, Math.floor(Number(value)));
    if (!Number.isFinite(number)) return;
    const newConfig = this._normalizedConfig();
    if (number === defaultValue) delete newConfig[name]; else newConfig[name] = number;
    this._commit(newConfig);
  }

  _setPriority(priority, checked) {
    const current = Array.isArray(this._config.priorities) ? this._config.priorities : CARD_PRIORITIES;
    const selected = new Set(current);
    checked ? selected.add(priority) : selected.delete(priority);
    const priorities = CARD_PRIORITIES.filter((item) => selected.has(item));
    const newConfig = this._normalizedConfig();
    if (priorities.length === 0 || priorities.length === CARD_PRIORITIES.length) delete newConfig.priorities;
    else newConfig.priorities = priorities;
    this._commit(newConfig);
  }

  _emitConfigChanged() {
    this.dispatchEvent(new CustomEvent("config-changed", { bubbles: true, composed: true, detail: { config: { ...this._config } } }));
  }

  _syncControlsFromConfig() {
    if (!this._rendered || !this.shadowRoot) return;
    const setValue = (control, value) => {
      const nextValue = String(value ?? "");
      if (control && control.value !== nextValue) control.value = nextValue;
    };
    this.shadowRoot.querySelectorAll("[data-string]").forEach((control) => {
      setValue(control, this._value(control.dataset.string));
    });
    const numberControl = this.shadowRoot.querySelector("[data-number]");
    setValue(numberControl, this._value(numberControl?.dataset.number));
    this.shadowRoot.querySelectorAll("[data-boolean]").forEach((control) => {
      const checked = control.dataset.boolean === "show_header"
        ? this._config.hide_header !== true
        : this._value(control.dataset.boolean) !== false;
      if (control.checked !== checked) control.checked = checked;
    });
    const priorities = Array.isArray(this._config.priorities) && this._config.priorities.length
      ? this._config.priorities : CARD_PRIORITIES;
    this.shadowRoot.querySelectorAll("[data-priority]").forEach((control) => {
      const checked = priorities.includes(control.dataset.priority);
      if (control.checked !== checked) control.checked = checked;
    });
    this.shadowRoot.querySelectorAll("[data-size]").forEach((control) => {
      setValue(control, this._config[control.dataset.size] ?? "");
    });
    this._syncDependentControls();
  }

  _syncDependentControls() {
    if (!this.shadowRoot) return;
    const syncGroup = (names, disabled) => names.forEach((name) => {
      const control = this.shadowRoot.querySelector(`[data-string="${name}"], [data-boolean="${name}"]`);
      if (!control) return;
      control.disabled = disabled;
      control.closest(".grid, .toggle-row")?.classList.toggle("disabled", disabled);
    });
    syncGroup(["header_icon", "show_header_icon", "show_header_status", "show_header_actions"], this._config.hide_header === true);
    syncGroup(["show_shelve_action", "show_disable_action", "show_restore_actions"], this._value("show_actions") === false);
  }

  _renderPreservingUiState() {
    const appearance = this.shadowRoot?.querySelector("details.section");
    if (appearance) this._appearanceOpen = appearance.open;
    this._render();
  }

  _render() {
    if (!this.shadowRoot) return;
    const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
    const text = (name, label, type = "text", extra = "") => `<label class="field"><span>${this._t(label)}</span><input data-string="${name}" type="${type}" value="${esc(this._value(name))}" ${extra}></label>`;
    const toggle = (name, label, disabled = false) => `<label class="toggle-row ${disabled ? "disabled" : ""}"><input data-boolean="${name}" type="checkbox" ${this._value(name) !== false ? "checked" : ""} ${disabled ? "disabled" : ""}><span>${this._t(label)}</span></label>`;
    const headerShown = this._config.hide_header !== true;
    const actionsShown = this._value("show_actions") !== false;
    const priorities = Array.isArray(this._config.priorities) && this._config.priorities.length ? this._config.priorities : CARD_PRIORITIES;
    const sizes = ["min_height", "header_icon_size", "title_font_size", "subtitle_font_size", "summary_font_size", "alarm_name_font_size", "alarm_meta_font_size", "priority_font_size", "action_font_size"];
    const sizeLabel = (name) => name === "min_height" ? this._t("editor_min_height") : name.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
    this.shadowRoot.innerHTML = `<style>
      :host{display:block;font-family:inherit;color:var(--primary-text-color)} .editor{display:grid;gap:16px;background:transparent}.section{padding:14px;border:1px solid var(--divider-color);border-radius:10px}.section-title,summary{font-size:1rem;font-weight:600;margin:0 0 12px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 16px}.field{display:grid;gap:6px;color:var(--secondary-text-color);font-size:.9rem}.field input,.field select{box-sizing:border-box;width:100%;min-height:42px;padding:8px 10px;font:inherit;color:var(--primary-text-color);background:transparent;border:1px solid var(--divider-color);border-radius:8px}.field input:focus,.field select:focus{outline:2px solid var(--primary-color);outline-offset:1px}.toggle-row{display:flex;align-items:center;gap:9px;min-height:34px}.toggle-row input{width:18px;height:18px;accent-color:var(--primary-color)}.disabled{opacity:.5}.priorities{display:flex;flex-wrap:wrap;gap:4px 16px;margin-top:12px}.helper{color:var(--secondary-text-color);font-size:.8rem;margin:10px 0 0}details.section summary{cursor:pointer} @media(max-width:600px){.grid{grid-template-columns:1fr}}
    </style><div class="editor">
      <section class="section"><h3 class="section-title">${this._t("editor_general")}</h3><div class="grid">
        ${text("title", "editor_title")}
        <label class="field"><span>${this._t("editor_view")}</span><select data-string="view">${["active","unacknowledged","shelved","disabled","inactive"].map((view) => `<option value="${view}" ${this._value("view") === view ? "selected" : ""}>${this._t(view === "disabled" ? "disabled_view" : view)}</option>`).join("")}</select></label>
        ${text("max_alarms", "editor_max_alarms", "number", 'min="0" step="1" data-number="max_alarms"')}
        <label class="field"><span>${this._t("editor_theme")}</span><select data-string="theme">${["auto","light","dark"].map((theme) => `<option ${this._value("theme") === theme ? "selected" : ""}>${theme}</option>`).join("")}</select></label>
      </div></section>
      <section class="section"><h3 class="section-title">${this._t("editor_header")}</h3>${toggle("show_header", "editor_show_header")}<div class="grid ${headerShown ? "" : "disabled"}">
        ${text("header_icon", "editor_header_icon", "text", headerShown ? "" : "disabled")}${toggle("show_header_icon", "editor_show_header_icon", !headerShown)}${toggle("show_header_status", "editor_show_header_status", !headerShown)}${toggle("show_header_actions", "editor_show_header_actions", !headerShown)}
      </div></section>
      <section class="section"><h3 class="section-title">${this._t("editor_content")}</h3><div class="grid">${toggle("show_summary","editor_show_summary")}${toggle("show_value","editor_show_value")}${toggle("show_area","editor_show_area")}${toggle("show_system","editor_show_system")}${toggle("show_tag","editor_show_tag")}${toggle("show_open_panel","editor_show_open_panel")}</div><div class="priorities"><strong>${this._t("editor_priorities")}</strong>${CARD_PRIORITIES.map((priority) => `<label class="toggle-row"><input data-priority="${priority}" type="checkbox" ${priorities.includes(priority) ? "checked" : ""}><span>${priority[0].toUpperCase()+priority.slice(1)}</span></label>`).join("")}</div></section>
      <section class="section"><h3 class="section-title">${this._t("editor_actions")}</h3><div class="grid">${toggle("show_actions","editor_show_actions")}${toggle("show_shelve_action","editor_show_shelve",!actionsShown)}${toggle("show_disable_action","editor_show_disable",!actionsShown)}${toggle("show_restore_actions","editor_show_restore",!actionsShown)}</div></section>
      <details class="section" ${this._appearanceOpen ? "open" : ""}><summary>${this._t("editor_appearance")}</summary><div class="grid">${sizes.map((name) => `<label class="field"><span>${sizeLabel(name)}</span><input data-size="${name}" value="${esc(this._config[name] ?? "")}" placeholder="${CARD_DEFAULTS[name]}"></label>`).join("")}</div><p class="helper">${this._t("editor_supported_units")}</p></details>
    </div>`;
    this.shadowRoot.querySelector('[data-boolean="show_header"]')?.addEventListener("change", (event) => this._setBooleanOption("hide_header", !event.target.checked, false));
    this.shadowRoot.querySelectorAll("[data-boolean]:not([data-boolean=show_header])").forEach((control) => control.addEventListener("change", (event) => this._setBooleanOption(control.dataset.boolean, event.target.checked)));
    this.shadowRoot.querySelectorAll("select[data-string]").forEach((control) => control.addEventListener("change", (event) => this._setStringOption(control.dataset.string, event.target.value, CARD_DEFAULTS[control.dataset.string])));
    this.shadowRoot.querySelectorAll("input[data-string]:not([data-number])").forEach((control) => control.addEventListener("input", (event) => this._setStringOption(control.dataset.string, event.target.value, CARD_DEFAULTS[control.dataset.string])));
    this.shadowRoot.querySelector("[data-number]")?.addEventListener("input", (event) => this._setNumberOption("max_alarms", event.target.value, CARD_DEFAULTS.max_alarms));
    this.shadowRoot.querySelectorAll("[data-priority]").forEach((control) => control.addEventListener("change", (event) => this._setPriority(control.dataset.priority, event.target.checked)));
    this.shadowRoot.querySelectorAll("[data-size]").forEach((control) => control.addEventListener("input", (event) => this._setStringOption(control.dataset.size, event.target.value, CARD_DEFAULTS[control.dataset.size])));
    this.shadowRoot.querySelector("details.section")?.addEventListener("toggle", (event) => { this._appearanceOpen = event.target.open; });
    this._rendered = true;
    this._syncDependentControls();
  }
}


// The dashboard card deliberately owns its rendering and data lifecycle.  The
// sidebar remains the full DCS console above; sharing that renderer here would
// re-introduce its tables, tabs and desktop interaction model.
class AlarmGridCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._alarms = [];
    this._sound = {};
    this._config = {};
    this._refreshing = false;
    this._subscribed = false;
    this._closeActionMenus = (event) => {
      if (event?.type === "keydown" && event.key !== "Escape") return;
      if (event?.type === "pointerdown" && event.composedPath().includes(this)) return;
      this.shadowRoot?.querySelectorAll("details.action-menu[open]").forEach((menu) => { menu.open = false; });
    };
  }

  connectedCallback() {
    document.addEventListener("pointerdown", this._closeActionMenus);
    document.addEventListener("keydown", this._closeActionMenus);
  }

  setConfig(config = {}) {
    const views = new Set(["active", "unacknowledged", "shelved", "disabled", "inactive"]);
    const requestedView = config.view ?? config.tab;
    const showActions = config.show_actions !== false;
    const priorities = Array.isArray(config.priorities)
      ? config.priorities.map((value) => String(value).toLowerCase()).filter((value) => ["critical", "high", "medium", "low", "info", "status"].includes(value))
      : null;
    this._config = {
      ...config,
      title: config.title || CARD_DEFAULTS.title,
      header_icon: typeof config.header_icon === "string" && config.header_icon.trim() ? config.header_icon.trim() : CARD_DEFAULTS.header_icon,
      show_header_icon: config.show_header_icon !== false,
      show_header_status: config.show_header_status !== false,
      show_header_actions: config.show_header_actions !== undefined ? config.show_header_actions !== false : showActions,
      header_icon_size: this._normalizeCssSize(config.header_icon_size, CARD_DEFAULTS.header_icon_size),
      title_font_size: this._normalizeCssSize(config.title_font_size, CARD_DEFAULTS.title_font_size),
      subtitle_font_size: this._normalizeCssSize(config.subtitle_font_size, CARD_DEFAULTS.subtitle_font_size),
      summary_font_size: this._normalizeCssSize(config.summary_font_size, CARD_DEFAULTS.summary_font_size),
      alarm_name_font_size: this._normalizeCssSize(config.alarm_name_font_size, CARD_DEFAULTS.alarm_name_font_size),
      alarm_meta_font_size: this._normalizeCssSize(config.alarm_meta_font_size, CARD_DEFAULTS.alarm_meta_font_size),
      priority_font_size: this._normalizeCssSize(config.priority_font_size, CARD_DEFAULTS.priority_font_size),
      action_font_size: this._normalizeCssSize(config.action_font_size, CARD_DEFAULTS.action_font_size),
      view: views.has(requestedView) ? requestedView : CARD_DEFAULTS.view,
      max_alarms: Math.max(0, Number.isFinite(Number(config.max_alarms)) ? Math.floor(Number(config.max_alarms)) : CARD_DEFAULTS.max_alarms),
      show_summary: config.show_summary !== false,
      show_actions: showActions,
      show_value: config.show_value !== false,
      show_area: config.show_area !== false,
      show_system: config.show_system !== false,
      show_tag: config.show_tag !== false,
      show_open_panel: config.show_open_panel !== false,
      show_shelve_action: config.show_shelve_action !== false && config.show_shelve !== false,
      show_disable_action: config.show_disable_action !== false,
      show_restore_actions: config.show_restore_actions !== false,
      hide_header: config.hide_header === true,
      priorities,
      theme: ["auto", "light", "dark"].includes(config.theme) ? config.theme : "auto",
    };
    this.style.setProperty("--ag-card-min-height", config.min_height || "0px");
    const sizeProperties = {
      "--ag-header-icon-size": this._config.header_icon_size,
      "--ag-title-font-size": this._config.title_font_size,
      "--ag-subtitle-font-size": this._config.subtitle_font_size,
      "--ag-summary-font-size": this._config.summary_font_size,
      "--ag-alarm-name-font-size": this._config.alarm_name_font_size,
      "--ag-alarm-meta-font-size": this._config.alarm_meta_font_size,
      "--ag-priority-font-size": this._config.priority_font_size,
      "--ag-action-font-size": this._config.action_font_size,
    };
    Object.entries(sizeProperties).forEach(([property, value]) => this.style.setProperty(property, value));
    if (this._rendered) this._render();
  }

  _normalizeCssSize(value, fallback) {
    const normalized = typeof value === "string" ? value.trim() : "";
    return /^(?:\d+(?:\.\d+)?|\.\d+)(?:px|rem|em|%)$/.test(normalized) ? normalized : fallback;
  }

  set hass(hass) {
    this._hass = hass;
    this._subscribeUpdates();
    if (!this._rendered) {
      this._render();
      this._load();
      this._timer = window.setInterval(() => this._load(), 5000);
    }
  }

  disconnectedCallback() {
    document.removeEventListener("pointerdown", this._closeActionMenus);
    document.removeEventListener("keydown", this._closeActionMenus);
    if (this._timer) window.clearInterval(this._timer);
    if (this._retryTimer) window.clearTimeout(this._retryTimer);
    if (this._unsubscribe) {
      Promise.resolve(this._unsubscribe).then((unsubscribe) => typeof unsubscribe === "function" && unsubscribe()).catch(() => undefined);
      this._unsubscribe = undefined;
      this._subscribed = false;
    }
  }

  _subscribeUpdates() {
    if (this._subscribed || !this._hass?.connection?.subscribeEvents) return;
    this._subscribed = true;
    try {
      this._unsubscribe = this._hass.connection.subscribeEvents((event) => {
        if (this._config.entry_id && event?.data?.entry_id && event.data.entry_id !== this._config.entry_id) return;
        this._load();
      }, ALARMS_UPDATED_EVENT);
    } catch (_err) {
      this._subscribed = false;
    }
  }

  async _load() {
    if (!this._hass || this._refreshing) return;
    this._refreshing = true;
    try {
      const result = await this._hass.callWS({ type: "alarmgrid/list_alarms" });
      this._alarms = result?.alarms || [];
      this._sound = result?.sound || {};
      this._error = undefined;
      this._render();
    } catch (err) {
      this._error = err?.message || String(err);
      this._render();
      if (/not loaded|not configured/i.test(this._error) && !this._retryTimer) {
        this._retryTimer = window.setTimeout(() => { this._retryTimer = undefined; this._load(); }, 1500);
      }
    } finally {
      this._refreshing = false;
    }
  }

  async _action(type, ruleId, extra = {}) {
    const payload = { type: `alarmgrid/${type}`, ...extra };
    if (ruleId) payload.rule_id = ruleId;
    await this._hass.callWS(payload);
    await this._load();
  }

  _showShelveDialog(alarm) {
    this._dialog = { kind: "shelve", alarm, preset: "15" };
    this._render();
    this.shadowRoot.querySelector("dialog")?.showModal();
  }

  _showDisableDialog(alarm) {
    this._dialog = { kind: "disable", alarm };
    this._render();
    this.shadowRoot.querySelector("dialog")?.showModal();
  }

  _durationMinutes(dialog) {
    const preset = dialog.querySelector("[name=preset]").value;
    if (preset !== "custom") return Number(preset);
    const value = Number(dialog.querySelector("[name=duration]").value);
    const factor = { minutes: 1, hours: 60, days: 1440 }[dialog.querySelector("[name=unit]").value];
    const minutes = value * factor;
    return Number.isFinite(minutes) && minutes > 0 ? Math.ceil(minutes) : null;
  }

  _remaining(expiry) {
    const milliseconds = new Date(expiry).getTime() - Date.now();
    if (!Number.isFinite(milliseconds) || milliseconds <= 0) return this._t("expiring");
    const minutes = Math.ceil(milliseconds / 60000);
    const days = Math.floor(minutes / 1440), hours = Math.floor((minutes % 1440) / 60), mins = minutes % 60;
    return this._t("remaining", { time: [days && `${days} d`, hours && `${hours} h`, !days && mins && `${mins} min`].filter(Boolean).join(" ") });
  }

  _dialogMarkup() {
    if (!this._dialog) return "";
    const alarm = this._dialog.alarm;
    const comment = `<label>${this._t("comment_optional")}<textarea name="comment" rows="2"></textarea></label>`;
    if (this._dialog.kind === "disable") return `<dialog aria-labelledby="dialog-title"><form method="dialog"><h3 id="dialog-title">${this._escape(this._t("confirm_disable_title", { name: alarm.name || alarm.id }))}</h3><p>${this._t("confirm_disable_message")}</p>${comment}<div class="dialog-actions"><button value="cancel">${this._t("cancel")}</button><button class="destructive" value="default" data-confirm-disable>${this._t("disable")}</button></div></form></dialog>`;
    return `<dialog aria-labelledby="dialog-title"><form method="dialog"><h3 id="dialog-title">${this._t("suspend_alarm")}</h3><label>${this._t("suspend_for")}<select name="preset"><option value="15">${this._t("duration_15m")}</option><option value="60">${this._t("duration_1h")}</option><option value="240">${this._t("duration_4h")}</option><option value="480">${this._t("duration_8h")}</option><option value="1440">${this._t("duration_1d")}</option><option value="4320">${this._t("duration_3d")}</option><option value="10080">${this._t("duration_7d")}</option><option value="custom">${this._t("custom")}</option></select></label><div class="custom-duration" hidden><label>${this._t("duration")}<input name="duration" type="number" min="0.01" step="any" inputmode="decimal"></label><select name="unit" aria-label="${this._t("duration")}"><option value="minutes">${this._t("minutes")}</option><option value="hours">${this._t("hours")}</option><option value="days">${this._t("days")}</option></select></div>${comment}<div class="validation" role="alert"></div><div class="dialog-actions"><button value="cancel">${this._t("cancel")}</button><button value="default" data-confirm-shelve>${this._t("suspend")}</button></div></form></dialog>`;
  }

  _visibleAlarms() {
    const states = {
      active: ["ACTIVE_UNACK", "ACTIVE_ACK", "CLEARED_UNACK"],
      unacknowledged: ["ACTIVE_UNACK", "CLEARED_UNACK"],
      shelved: ["SHELVED"],
      disabled: ["DISABLED"],
      inactive: ["SHELVED", "DISABLED"],
    };
    return this._alarms
      .filter((alarm) => states[this._config.view].includes(alarm.lifecycle_state))
      .filter((alarm) => !this._config.priorities || this._config.priorities.includes(String(alarm.priority).toLowerCase()))
      .sort((a, b) => (Number(b.severity) - Number(a.severity)) || String(b.active_since || b.cleared_at || "").localeCompare(String(a.active_since || a.cleared_at || "")));
  }

  _language() {
    return String(this._hass?.locale?.language || this._hass?.language || "en").toLowerCase().split("-")[0];
  }

  _t(key, replacements = {}) {
    const table = TRANSLATIONS[this._language()] || TRANSLATIONS.en;
    let value = table[key] ?? TRANSLATIONS.en[key] ?? key;
    Object.entries(replacements).forEach(([name, replacement]) => { value = value.replaceAll(`{${name}}`, String(replacement)); });
    return value;
  }

  _escape(value) {
    return String(value ?? "").replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[character]);
  }

  _time(value) {
    if (!value) return "";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? this._escape(value) : new Intl.DateTimeFormat(this._language(), { hour: "2-digit", minute: "2-digit" }).format(date);
  }

  _alarmItem(alarm) {
    const priority = String(alarm.priority || "status").toLowerCase();
    const state = alarm.lifecycle_state;
    const unack = ["ACTIVE_UNACK", "CLEARED_UNACK"].includes(state);
    const context = [this._config.show_system && alarm.system, this._config.show_area && alarm.area].filter(Boolean);
    const value = alarm.last_value ?? alarm.last_source_state;
    let status = this._t(`state_${String(state || "normal").toLowerCase()}`);
    if (state === "SHELVED") status = `${this._t("shelved_until", { time: this._time(alarm.shelve_expiry) })}<br>${this._remaining(alarm.shelve_expiry)}`;
    if (state === "DISABLED") status = this._t("alarm_disabled");
    const activeActions = ["active", "unacknowledged"].includes(this._config.view) && state !== "DISABLED" && state !== "SHELVED";
    const menu = activeActions && (this._config.show_shelve_action || this._config.show_disable_action) ? `<details class="action-menu"><summary class="icon-button" title="${this._t("more_actions")}" aria-label="${this._t("more_actions")}"><ha-icon icon="mdi:dots-vertical" aria-hidden="true"></ha-icon></summary><div class="menu-popover">${this._config.show_shelve_action ? `<button data-open-shelve="${this._escape(alarm.id)}">${this._t("suspend_alarm")}</button>` : ""}${this._config.show_disable_action ? `<button class="destructive-text" data-open-disable="${this._escape(alarm.id)}">${this._t("disable_alarm")}</button>` : ""}</div></details>` : "";
    const restore = this._config.show_restore_actions && state === "SHELVED" ? `<button data-unshelve="${this._escape(alarm.id)}">${this._t("unshelve_now")}</button>` : this._config.show_restore_actions && state === "DISABLED" ? `<button data-enable="${this._escape(alarm.id)}">${this._t("enable_alarm")}</button>` : "";
    return `<article class="alarm-item priority-${this._escape(priority)} state-${state?.toLowerCase()}"><div class="accent" aria-hidden="true"></div><div class="alarm-content"><div class="alarm-leading"><span class="priority-badge"><span class="state-icon" aria-hidden="true">${state === "SHELVED" ? "💤" : state === "DISABLED" ? "🚫" : ""}</span><span class="priority-dot" aria-hidden="true"></span>${this._escape(this._t(`priority_${priority}`))}</span><time>${this._time(alarm.active_since || alarm.cleared_at)}</time></div><div class="alarm-name">${this._escape(alarm.name || alarm.tag || alarm.id)}</div>${this._config.show_tag && alarm.tag ? `<div class="alarm-tag">${this._escape(alarm.tag)}</div>` : ""}${context.length ? `<div class="alarm-context">${context.map((item) => this._escape(item)).join(" · ")}</div>` : ""}<div class="alarm-footer"><div class="alarm-details">${this._config.show_value && value != null && value !== "" ? `${this._escape(value)} · ` : ""}<span class="state">${status}</span></div>${this._config.show_actions ? `<div class="item-actions">${activeActions ? `<button data-ack="${this._escape(alarm.id)}" ${alarm.acknowledged ? "disabled" : ""}>${this._t("ack")}</button>${menu}` : restore}</div>` : ""}</div></div></article>`;
  }

  _openPanel() {
    history.pushState(null, "", "/alarmgrid");
    window.dispatchEvent(new Event("location-changed"));
  }

  _render() {
    if (!this.shadowRoot) return;
    const visible = this._visibleAlarms();
    const shown = visible.slice(0, this._config.max_alarms);
    const active = this._alarms.filter((alarm) => ["ACTIVE_UNACK", "ACTIVE_ACK"].includes(alarm.lifecycle_state)).length;
    const unack = this._alarms.filter((alarm) => ["ACTIVE_UNACK", "CLEARED_UNACK"].includes(alarm.lifecycle_state)).length;
    const shelved = this._alarms.filter((alarm) => alarm.lifecycle_state === "SHELVED").length;
    const disabled = this._alarms.filter((alarm) => alarm.lifecycle_state === "DISABLED").length;
    const count = (priority) => this._alarms.filter((alarm) => alarm.priority === priority && ["ACTIVE_UNACK", "ACTIVE_ACK", "CLEARED_UNACK"].includes(alarm.lifecycle_state)).length;
    const themeClass = this._config.theme === "auto" ? "" : ` force-${this._config.theme}`;
    this.shadowRoot.innerHTML = `<style>${this._styles()}</style><ha-card class="alarm-card${themeClass}">
      ${this._config.hide_header ? "" : `<header><div class="heading">${this._config.show_header_icon ? `<ha-icon icon="${this._escape(this._config.header_icon)}" aria-hidden="true"></ha-icon>` : ""}<div><h2>${this._escape(this._config.title)}</h2>${this._config.show_header_status ? `<p>${this._t("metric_active", { count: active })} · ${this._t("metric_unack", { count: unack })}${this._sound.horn_active ? ` · ${this._t("horn_active")}` : ""}</p>` : ""}</div></div>${this._config.show_header_actions ? `<div class="header-actions"><button class="icon-button" data-action="silence" title="${this._t("silence")}" aria-label="${this._t("silence")}"><ha-icon icon="mdi:volume-off"></ha-icon></button><button class="icon-button" data-action="ack-all" title="${this._t("ack_all")}" aria-label="${this._t("ack_all")}"><ha-icon icon="mdi:check-all"></ha-icon></button></div>` : ""}</header>`}
      ${this._config.show_summary ? `<section class="summary" aria-label="Alarm summary"><span class="chip critical"><b>${count("critical")}</b> ${this._t("priority_critical")}</span><span class="chip high"><b>${count("high")}</b> ${this._t("priority_high")}</span><span class="chip unack"><b>${unack}</b> ${this._t("metric_unack", { count: "" }).trim()}</span><span class="chip"><b>💤 ${shelved}</b></span><span class="chip"><b>🚫 ${disabled}</b></span></section>` : ""}
      ${this._error ? `<div class="error" role="alert">${this._escape(this._error)}</div>` : ""}
      <section class="alarm-list">${shown.length ? shown.map((alarm) => this._alarmItem(alarm)).join("") : `<div class="empty"><ha-icon icon="mdi:check-circle-outline"></ha-icon><span>${this._t("no_alarms")}</span></div>`}</section>
      ${visible.length > shown.length ? `<button class="more" data-action="open-panel">+${visible.length - shown.length} more alarms</button>` : ""}
      ${this._config.show_open_panel ? `<footer><button data-action="open-panel">Open AlarmGrid <span aria-hidden="true">→</span></button></footer>` : ""}
    </ha-card>${this._dialogMarkup()}`;
    this.shadowRoot.querySelector("[data-action='silence']")?.addEventListener("click", () => this._action("silence"));
    this.shadowRoot.querySelector("[data-action='ack-all']")?.addEventListener("click", () => this._action("acknowledge_all"));
    this.shadowRoot.querySelectorAll("[data-ack]").forEach((button) => button.addEventListener("click", () => this._action("acknowledge", button.dataset.ack)));
    this.shadowRoot.querySelectorAll("details.action-menu").forEach((menu) => menu.addEventListener("toggle", () => {
      if (!menu.open) return;
      this.shadowRoot.querySelectorAll("details.action-menu[open]").forEach((other) => { if (other !== menu) other.open = false; });
    }));
    this.shadowRoot.querySelectorAll("[data-open-shelve]").forEach((button) => button.addEventListener("click", () => this._showShelveDialog(this._alarms.find((alarm) => alarm.id === button.dataset.openShelve))));
    this.shadowRoot.querySelectorAll("[data-open-disable]").forEach((button) => button.addEventListener("click", () => this._showDisableDialog(this._alarms.find((alarm) => alarm.id === button.dataset.openDisable))));
    this.shadowRoot.querySelectorAll("[data-unshelve]").forEach((button) => button.addEventListener("click", () => this._action("unshelve", button.dataset.unshelve)));
    this.shadowRoot.querySelectorAll("[data-enable]").forEach((button) => button.addEventListener("click", () => this._action("enable", button.dataset.enable)));
    const dialog = this.shadowRoot.querySelector("dialog");
    dialog?.addEventListener("close", () => { this._dialog = undefined; this._render(); });
    dialog?.querySelector("[name=preset]")?.addEventListener("change", (event) => { dialog.querySelector(".custom-duration").hidden = event.target.value !== "custom"; });
    dialog?.querySelector("[data-confirm-shelve]")?.addEventListener("click", async (event) => { const duration_minutes = this._durationMinutes(dialog); if (!duration_minutes) { event.preventDefault(); dialog.querySelector(".validation").textContent = this._t("duration_invalid"); return; } const comment = dialog.querySelector("[name=comment]").value.trim(); await this._action("shelve", this._dialog.alarm.id, { duration_minutes, ...(comment ? { comment } : {}) }); });
    dialog?.querySelector("[data-confirm-disable]")?.addEventListener("click", async () => { const comment = dialog.querySelector("[name=comment]").value.trim(); await this._action("disable", this._dialog.alarm.id, comment ? { comment } : {}); });
    this.shadowRoot.querySelectorAll("[data-action='open-panel']").forEach((button) => button.addEventListener("click", () => this._openPanel()));
    this._rendered = true;
  }

  _styles() {
    return `:host { display:block; min-width:0; font-family:inherit; --ag-critical:#d64545; --ag-high:#e17825; --ag-medium:#c79618; --ag-low:#4285b4; --ag-info:#477fc1; --ag-status:#718096; }
      .alarm-card { min-height:var(--ag-card-min-height, 0); overflow:visible; color:var(--primary-text-color); background:var(--ha-card-background, var(--card-background-color)); border-radius:var(--ha-card-border-radius, 12px); }
      .force-light { color-scheme:light; --primary-text-color:#202124; --secondary-text-color:#5f6368; --divider-color:#dfe1e5; --ha-card-background:#fff; }
      .force-dark { color-scheme:dark; --primary-text-color:#e8eaed; --secondary-text-color:#aab0b6; --divider-color:#45494e; --ha-card-background:#202124; }
      header { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; padding:16px 16px 10px; }
      .heading { display:flex; min-width:0; gap:12px; align-items:center; } .heading>ha-icon { width:var(--ag-header-icon-size, 24px); height:var(--ag-header-icon-size, 24px); --mdc-icon-size:var(--ag-header-icon-size, 24px); color:var(--error-color, var(--ag-critical)); flex:none; }
      h2 { margin:0; font-size:var(--ag-title-font-size, 1.15rem); line-height:1.3; font-weight:600; overflow-wrap:anywhere; } p { margin:3px 0 0; color:var(--secondary-text-color); font-size:.85rem; } header p { font-size:var(--ag-subtitle-font-size, .85rem); overflow-wrap:anywhere; }
      button { font:inherit; color:inherit; background:none; border:0; cursor:pointer; border-radius:var(--ha-card-border-radius, 12px); }
      button:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; } button:disabled { opacity:.45; cursor:default; }
      .header-actions { display:flex; gap:4px; flex:none; } .icon-button { display:grid; place-items:center; width:44px; height:44px; }
      .icon-button:hover, footer button:hover, .more:hover { background:color-mix(in srgb, var(--primary-text-color) 8%, transparent); }
      .summary { display:flex; flex-wrap:wrap; gap:7px; padding:4px 16px 12px; font-size:var(--ag-summary-font-size, .78rem); }
      .chip { display:inline-flex; gap:4px; align-items:center; padding:4px 9px; border:1px solid var(--divider-color); border-radius:999px; color:var(--secondary-text-color); font-size:inherit; }
      .chip.critical b { color:var(--ag-critical); } .chip.high b { color:var(--ag-high); } .chip.unack b { color:var(--warning-color, var(--ag-medium)); }
      .alarm-list { display:grid; gap:9px; padding:4px 12px 12px; min-width:0; }
      .alarm-item { --priority:var(--ag-status); position:relative; display:flex; min-width:0; border:1px solid var(--divider-color); border-radius:var(--ha-card-border-radius, 12px); background:color-mix(in srgb, var(--ha-card-background, var(--card-background-color)) 96%, var(--priority)); overflow:visible; }
      .priority-critical { --priority:var(--ag-critical); } .priority-high { --priority:var(--ag-high); } .priority-medium { --priority:var(--ag-medium); } .priority-low { --priority:var(--ag-low); } .priority-info { --priority:var(--ag-info); }
      .accent { width:4px; flex:none; background:var(--priority); border-radius:var(--ha-card-border-radius, 12px) 0 0 var(--ha-card-border-radius, 12px); } .alarm-content { padding:10px 12px; min-width:0; flex:1; border-radius:0 var(--ha-card-border-radius, 12px) var(--ha-card-border-radius, 12px) 0; }
      .alarm-leading, .alarm-footer { display:flex; justify-content:space-between; align-items:center; gap:10px; min-width:0; }
      .priority-badge { display:inline-flex; align-items:center; gap:6px; color:var(--priority); font-size:var(--ag-priority-font-size, .7rem); font-weight:700; letter-spacing:.04em; text-transform:uppercase; }
      .priority-dot { width:7px; height:7px; border-radius:50%; background:currentColor; } time, .alarm-tag, .alarm-context, .alarm-details { color:var(--secondary-text-color); font-size:var(--ag-alarm-meta-font-size, .78rem); }
      .alarm-name { margin:5px 0 2px; min-width:0; font-size:var(--ag-alarm-name-font-size, 1rem); font-weight:600; line-height:1.35; overflow-wrap:anywhere; } .alarm-tag { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
      .alarm-context { margin-top:3px; overflow-wrap:anywhere; } .alarm-footer { margin-top:7px; align-items:flex-end; } .alarm-details { min-width:0; overflow-wrap:anywhere; }
      .state { color:var(--primary-text-color); } .item-actions { position:relative; z-index:1; display:flex; flex:none; align-items:center; gap:3px; } .item-actions button { min-height:40px; padding:0 10px; color:var(--primary-color); font-size:var(--ag-action-font-size, .78rem); font-weight:600; text-transform:uppercase; }
      .action-menu { position:relative; flex:none; } .action-menu[open] { z-index:4; } .action-menu summary { box-sizing:border-box; list-style:none; cursor:pointer; color:var(--primary-text-color); border-radius:var(--ha-card-border-radius, 12px); } .action-menu summary::-webkit-details-marker { display:none; } .action-menu summary::marker { content:""; } .action-menu summary:hover { background:color-mix(in srgb, var(--primary-text-color) 8%, transparent); } .action-menu summary:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; } .action-menu summary ha-icon { display:block; width:24px; height:24px; color:var(--primary-text-color); }
      .menu-popover { position:absolute; z-index:4; right:0; bottom:calc(100% + 4px); box-sizing:border-box; min-width:170px; max-width:min(240px, calc(100vw - 32px)); padding:5px; border:1px solid var(--divider-color); border-radius:10px; color:var(--primary-text-color); background:var(--ha-card-background, var(--card-background-color)); box-shadow:var(--ha-card-box-shadow, 0 3px 12px rgba(0,0,0,.2)); } .menu-popover button { display:block; width:100%; min-height:40px; padding:8px 10px; color:var(--primary-text-color); text-align:left; } .destructive-text { color:var(--error-color)!important; }
      .state-shelved .accent { background:var(--info-color, var(--primary-color)); } .state-disabled .accent { background:var(--disabled-text-color, var(--secondary-text-color)); }
      dialog { width:min(420px, calc(100vw - 32px)); box-sizing:border-box; color:var(--primary-text-color); background:var(--ha-card-background, var(--card-background-color)); border:1px solid var(--divider-color); border-radius:var(--ha-card-border-radius, 12px); padding:20px; } dialog::backdrop { background:rgba(0,0,0,.45); } dialog form, dialog label { display:grid; gap:8px; } dialog h3, dialog p { margin:0 0 12px; } dialog select, dialog input, dialog textarea { box-sizing:border-box; width:100%; min-height:42px; padding:8px; color:inherit; background:var(--input-fill-color, transparent); border:1px solid var(--divider-color); border-radius:8px; font:inherit; } .custom-duration { display:grid; grid-template-columns:1fr 1fr; gap:8px; align-items:end; } .custom-duration[hidden] { display:none; } .dialog-actions { display:flex; justify-content:flex-end; gap:8px; margin-top:16px; } .dialog-actions button { min-height:44px; padding:0 14px; color:var(--primary-color); } .dialog-actions .destructive { color:var(--text-primary-color, white); background:var(--error-color); } .validation { min-height:1.2em; color:var(--error-color); font-size:.85rem; } .is-unack .accent, .is-unack .priority-dot { animation:cardPulse 1.8s ease-in-out infinite; }
      @keyframes cardPulse { 50% { opacity:.42; } } @media (prefers-reduced-motion:reduce) { .is-unack .accent, .is-unack .priority-dot { animation:none; } }
      .empty { display:flex; justify-content:center; align-items:center; gap:8px; min-height:96px; color:var(--secondary-text-color); text-align:center; }
      .empty ha-icon { color:var(--primary-color); } .error { margin:0 16px 10px; padding:10px; color:var(--error-color); border:1px solid var(--error-color); border-radius:var(--ha-card-border-radius, 12px); }
      .more { display:block; margin:0 auto 6px; min-height:40px; padding:0 12px; color:var(--secondary-text-color); font-size:.82rem; }
      footer { border-top:1px solid var(--divider-color); padding:5px 8px; text-align:center; } footer button { min-height:44px; width:100%; color:var(--primary-color); font-weight:500; }
      @media (max-width:420px) { header { padding-inline:12px; } .summary { padding-inline:12px; } .alarm-footer { align-items:flex-start; flex-direction:column; } .item-actions { align-self:flex-end; } }
    `;
  }

  getCardSize() {
    return Math.max(2, Math.min(this._config.max_alarms || 5, this._visibleAlarms().length) * 2 + 2);
  }

  static getStubConfig() {
    return {
      title: "AlarmGrid",
      view: "active",
      max_alarms: 5,
    };
  }

  static getConfigElement() {
    return document.createElement("alarmgrid-card-editor");
  }
}

if (!customElements.get("alarmgrid-panel")) {
  customElements.define("alarmgrid-panel", AlarmGrid);
}

if (!customElements.get("alarmgrid-card")) {
  customElements.define("alarmgrid-card", AlarmGridCard);
}

if (!customElements.get("alarmgrid-card-editor")) {
  customElements.define("alarmgrid-card-editor", AlarmGridCardEditor);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === "alarmgrid-card")) {
  window.customCards.push({
    type: "alarmgrid-card",
    name: "AlarmGrid",
    description: "Compact, responsive alarm summary for Home Assistant dashboards.",
    documentationURL: "https://github.com/xtimmy86x/alarmgrid#lovelace-card",
    preview: true,
  });
}
