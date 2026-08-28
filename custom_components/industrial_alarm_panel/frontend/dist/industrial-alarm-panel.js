const ALARMS_UPDATED_EVENT = "industrial_alarm_panel_alarms_updated";

const TRANSLATIONS = {
  en: {
    default_title: "Industrial Alarms",
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
    ack: "Ack",
    shelve: "Shelve",
    no_alarms: "No alarms in this view",
    no_history: "No history rows",
    no_rules: "No rules configured",
    suggested_rules: "Suggested Rules",
    label_high_w: "High W",
    label_low_v: "Low V",
    label_high_v: "High V",
    label_solar_c: "Solar C",
    preview_suggested: "Preview Suggested Rules",
    select_all: "Select All",
    deselect_all: "Deselect All",
    create_selected: "Create Selected",
    create_all: "Create All",
    remove_auto: "Remove Auto-Generated Rules",
    n_suggested: "{count} suggested",
    n_selected: "{count} selected",
    n_estimated_entities: "{count} estimated entities",
    n_generated_estimated: "{count} generated estimated entities",
    n_rules: "{count} rules",
    n_auto_generated: "{count} auto-generated",
    n_auto_generated_estimated: "{count} auto-generated estimated entities",
    placeholder_rule_id: "Rule id",
    placeholder_entity_id: "Entity id",
    placeholder_name: "Name",
    placeholder_system: "System",
    placeholder_threshold: "Threshold",
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
    previewing_suggested: "Previewing {count} suggested rules, {entities} estimated entities",
    no_suggested_found: "No suggested rules found",
    select_before_create: "Select suggested rules before creating them",
    confirm_create_suggested: "Create {count} suggested rules and about {entities} entities?",
    created_suggested: "Created {count} suggested rules, {entities} estimated entities",
    skipped_suffix: ", skipped {count}",
    no_new_suggested: "No new suggested alarm rules",
    preview_again: "Preview suggested rules again after changing thresholds",
    label_selected_rules: "selected rules",
    label_auto_rules: "auto-generated rules",
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
    ack: "Riconosci",
    shelve: "Sospendi",
    no_alarms: "Nessun allarme in questa vista",
    no_history: "Nessun evento nello storico",
    no_rules: "Nessuna regola configurata",
    suggested_rules: "Regole suggerite",
    label_high_w: "W max",
    label_low_v: "V min",
    label_high_v: "V max",
    label_solar_c: "Solare °C",
    preview_suggested: "Anteprima regole suggerite",
    select_all: "Seleziona tutte",
    deselect_all: "Deseleziona tutte",
    create_selected: "Crea selezionate",
    create_all: "Crea tutte",
    remove_auto: "Rimuovi regole auto-generate",
    n_suggested: "{count} suggerite",
    n_selected: "{count} selezionate",
    n_estimated_entities: "{count} entità stimate",
    n_generated_estimated: "{count} entità stimate generate",
    n_rules: "{count} regole",
    n_auto_generated: "{count} auto-generate",
    n_auto_generated_estimated: "{count} entità stimate auto-generate",
    placeholder_rule_id: "ID regola",
    placeholder_entity_id: "ID entità",
    placeholder_name: "Nome",
    placeholder_system: "Sistema",
    placeholder_threshold: "Soglia",
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
    previewing_suggested: "Anteprima di {count} regole suggerite, {entities} entità stimate",
    no_suggested_found: "Nessuna regola suggerita trovata",
    select_before_create: "Seleziona le regole suggerite prima di crearle",
    confirm_create_suggested: "Creare {count} regole suggerite e circa {entities} entità?",
    created_suggested: "Create {count} regole suggerite, {entities} entità stimate",
    skipped_suffix: ", saltate {count}",
    no_new_suggested: "Nessuna nuova regola di allarme suggerita",
    preview_again: "Rigenera l'anteprima delle regole suggerite dopo aver cambiato le soglie",
    label_selected_rules: "regole selezionate",
    label_auto_rules: "regole auto-generate",
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

class IndustrialAlarmPanel extends HTMLElement {
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
      system: "",
    };
    this._suggestionDraft = {
      power_threshold_w: 2000,
      low_voltage_v: 207,
      high_voltage_v: 253,
      high_solar_water_temp_c: 75,
    };
    this._suggestedRules = [];
    this._selectedSuggestedRuleIds = new Set();
    this._selectedRuleIds = new Set();
    this._editingRuleId = null;
    this._rulesResult = null;
    this._suggestedRulesResult = null;
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
      const alarms = await this._callWS({ type: "industrial_alarm_panel/list_alarms" });
      const history = await this._callWS({ type: "industrial_alarm_panel/list_history", limit: 250 });
      const rules = await this._callWS({ type: "industrial_alarm_panel/list_rules" });
      this._alarms = alarms?.alarms || [];
      this._sound = alarms?.sound || {};
      this._history = history?.events || [];
      this._rules = rules?.rules || [];
      const ruleIds = new Set(this._rules.map((rule) => rule.id));
      this._selectedRuleIds = new Set([...this._selectedRuleIds].filter((id) => ruleIds.has(id)));
      this._suggestedRules = this._suggestedRules.filter((rule) => !ruleIds.has(rule.id));
      const suggestedRuleIds = new Set(this._suggestedRules.map((rule) => rule.id));
      this._selectedSuggestedRuleIds = new Set([...this._selectedSuggestedRuleIds].filter((id) => suggestedRuleIds.has(id)));
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
    await this._callWS({ type: "industrial_alarm_panel/acknowledge", rule_id: ruleId });
    await this._load();
  }

  async _ackAll() {
    await this._callWS({ type: "industrial_alarm_panel/acknowledge_all" });
    await this._load();
  }

  async _silence() {
    await this._callWS({ type: "industrial_alarm_panel/silence" });
    this._stopBrowserHorn();
    await this._load();
  }

  async _shelve(ruleId) {
    await this._callWS({
      type: "industrial_alarm_panel/shelve",
      rule_id: ruleId,
      duration_minutes: this._shelveDurationMinutes,
    });
    await this._load();
  }

  async _testSound() {
    this._audioEnabled = true;
    await this._callWS({ type: "industrial_alarm_panel/test_sound", priority: "critical" });
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
    const suggestionDraft = this._suggestionDraft;
    const selectedSuggestedCount = this._selectedSuggestedRuleIds.size;
    const selectedRuleCount = this._selectedRuleIds.size;
    const autoGeneratedCount = this._rules.filter((rule) => String(rule.id || "").startsWith("auto_")).length;
    return `
      <section class="rules">
        <div class="suggested-rules">
          <h2>${this._t("suggested_rules")}</h2>
          <div class="suggested-rules-controls">
            <label>${this._t("label_high_w")} <input type="number" min="1" step="50" value="${this._escape(suggestionDraft.power_threshold_w)}" data-suggest="power_threshold_w"></label>
            <label>${this._t("label_low_v")} <input type="number" min="1" step="1" value="${this._escape(suggestionDraft.low_voltage_v)}" data-suggest="low_voltage_v"></label>
            <label>${this._t("label_high_v")} <input type="number" min="1" step="1" value="${this._escape(suggestionDraft.high_voltage_v)}" data-suggest="high_voltage_v"></label>
            <label>${this._t("label_solar_c")} <input type="number" min="1" step="1" value="${this._escape(suggestionDraft.high_solar_water_temp_c)}" data-suggest="high_solar_water_temp_c"></label>
            <button class="secondary" data-action="preview-suggested-rules">${this._t("preview_suggested")}</button>
            <button class="secondary" data-action="select-all-suggested-rules" ${this._suggestedRules.length && selectedSuggestedCount !== this._suggestedRules.length ? "" : "disabled"}>${this._t("select_all")}</button>
            <button class="secondary" data-action="deselect-all-suggested-rules" ${selectedSuggestedCount ? "" : "disabled"}>${this._t("deselect_all")}</button>
            <button class="primary" data-action="create-selected-suggested-rules" ${selectedSuggestedCount ? "" : "disabled"}>${this._t("create_selected")}</button>
            <button class="primary" data-action="create-all-suggested-rules" ${this._suggestedRules.length ? "" : "disabled"}>${this._t("create_all")}</button>
            <button class="danger" data-action="remove-auto-generated-rules" ${autoGeneratedCount ? "" : "disabled"}>${this._t("remove_auto")}</button>
          </div>
          <div class="bulk-summary">
            <span>${this._t("n_suggested", { count: this._suggestedRules.length })}</span>
            <span>${this._t("n_selected", { count: selectedSuggestedCount })}</span>
            <span>${this._t("n_estimated_entities", { count: selectedSuggestedCount * 4 })}</span>
            <span>${this._t("n_generated_estimated", { count: this._suggestedRules.length * 4 })}</span>
          </div>
          ${this._suggestedRulesResult ? `<div class="notice">${this._escape(this._suggestedRulesResult)}</div>` : ""}
          ${this._suggestedRules.length ? `
            <div class="table-shell suggested-preview">
              <table data-table-id="suggested-rules">
                <thead><tr><th></th><th>${this._t("col_id")}</th><th>${this._t("col_entity")}</th><th>${this._t("col_name")}</th><th>${this._t("col_condition")}</th><th>${this._t("col_threshold")}</th><th>${this._t("col_priority")}</th></tr></thead>
                <tbody>${this._suggestedRules.map((rule) => `
                  <tr>
                    <td><input class="row-select" type="checkbox" data-suggested-select="${this._escape(rule.id)}" ${this._selectedSuggestedRuleIds.has(rule.id) ? "checked" : ""}></td>
                    <td>${this._escape(rule.id)}</td>
                    <td>${this._escape(rule.entity_id)}</td>
                    <td>${this._escape(rule.name)}</td>
                    <td>${this._escape(rule.condition)}</td>
                    <td>${this._escape(rule.threshold ?? "")}</td>
                    <td>${this._escape(rule.priority)}</td>
                  </tr>`).join("")}</tbody>
              </table>
            </div>
          ` : ""}
        </div>
        <div class="rule-form">
          <input placeholder="${this._t("placeholder_rule_id")}" value="${this._escape(ruleDraft.id)}" data-new="id" ${this._editingRuleId ? "disabled" : ""}>
          <input placeholder="${this._t("placeholder_entity_id")}" value="${this._escape(ruleDraft.entity_id)}" data-new="entity_id" list="entity-id-options" autocomplete="off">
          <datalist id="entity-id-options">${this._entityOptions()}</datalist>
          <input placeholder="${this._t("placeholder_name")}" value="${this._escape(ruleDraft.name)}" data-new="name">
          <input placeholder="${this._t("placeholder_system")}" value="${this._escape(ruleDraft.system)}" data-new="system">
          <select data-new="condition">
            ${["above", "below", "equal", "not_equal", "contains", "is_on", "is_off", "state_changed", "unavailable", "unavailable_for", "unknown_for", "manual"].map((c) => `<option value="${c}" ${ruleDraft.condition === c ? "selected" : ""}>${c}</option>`).join("")}
          </select>
          <input placeholder="${this._t("placeholder_threshold")}" value="${this._escape(ruleDraft.threshold)}" data-new="threshold">
          <select data-new="priority">
            ${["critical", "high", "medium", "low", "info", "status"].map((p) => `<option value="${p}" ${ruleDraft.priority === p ? "selected" : ""}>${this._t(`priority_${p}`)}</option>`).join("")}
          </select>
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
          <span>${this._t("n_auto_generated", { count: autoGeneratedCount })}</span>
          <span>${this._t("n_estimated_entities", { count: selectedRuleCount * 4 })}</span>
          <span>${this._t("n_auto_generated_estimated", { count: autoGeneratedCount * 4 })}</span>
          <button class="danger" data-action="delete-selected-rules" ${selectedRuleCount ? "" : "disabled"}>${this._t("delete_selected")}</button>
          <button class="secondary" data-action="export-rules" ${this._rules.length ? "" : "disabled"}>${this._t("export_rules")}</button>
          <button class="secondary" data-action="choose-rules-csv">${this._t("import_rules")}</button>
          <input class="file-input" type="file" accept=".csv,text/csv" data-rules-csv>
          </div>
        <div class="table-shell">
          <table data-table-id="rules">
            <thead><tr><th></th><th>${this._t("col_id")}</th><th>${this._t("col_entity")}</th><th>${this._t("col_name")}</th><th>${this._t("col_area")}</th><th>${this._t("col_system")}</th><th>${this._t("col_condition")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_enabled")}</th><th></th></tr></thead>
            <tbody>${this._rules.length ? this._rules.map((rule) => `<tr><td><input class="row-select" type="checkbox" data-rule-select="${this._escape(rule.id)}" ${this._selectedRuleIds.has(rule.id) ? "checked" : ""}></td><td>${this._escape(rule.id)}</td><td>${this._escape(rule.entity_id)}</td><td>${this._escape(rule.name)}</td><td>${this._escape(rule.area || "")}</td><td>${this._escape(rule.system || "")}</td><td>${this._escape(rule.condition)}</td><td>${this._t(`priority_${rule.priority}`)}</td><td>${rule.enabled ? this._t("yes") : this._t("no")}</td><td><button data-edit-rule="${this._escape(rule.id)}">${this._t("edit")}</button></td></tr>`).join("") : `<tr><td colspan="10" class="empty">${this._t("no_rules")}</td></tr>`}</tbody>
          </table>
        </div>
      </section>
    `;
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
    this.shadowRoot.querySelector("[data-action='preview-suggested-rules']")?.addEventListener("click", () => this._previewSuggestedRules());
    this.shadowRoot.querySelector("[data-action='select-all-suggested-rules']")?.addEventListener("click", () => this._selectAllSuggestedRules());
    this.shadowRoot.querySelector("[data-action='deselect-all-suggested-rules']")?.addEventListener("click", () => this._deselectAllSuggestedRules());
    this.shadowRoot.querySelector("[data-action='create-selected-suggested-rules']")?.addEventListener("click", () => this._createSelectedSuggestedRules());
    this.shadowRoot.querySelector("[data-action='create-all-suggested-rules']")?.addEventListener("click", () => this._createAllSuggestedRules());
    this.shadowRoot.querySelector("[data-action='delete-selected-rules']")?.addEventListener("click", () => this._deleteSelectedRules());
    this.shadowRoot.querySelector("[data-action='export-rules']")?.addEventListener("click", () => this._exportRules());
    this.shadowRoot.querySelector("[data-action='choose-rules-csv']")?.addEventListener("click", () => this.shadowRoot.querySelector("[data-rules-csv]")?.click());
    this.shadowRoot.querySelector("[data-rules-csv]")?.addEventListener("change", (event) => this._importRules(event.target.files?.[0]));
    this.shadowRoot.querySelector("[data-action='remove-auto-generated-rules']")?.addEventListener("click", () => this._removeAutoGeneratedRules());
    this.shadowRoot.querySelectorAll("[data-new]").forEach((field) => {
      const updateDraft = () => {
        this._ruleDraft[field.dataset.new] = field.value;
      };
      field.addEventListener("input", updateDraft);
      field.addEventListener("change", updateDraft);
    });
    this.shadowRoot.querySelectorAll("[data-suggest]").forEach((field) => {
      const updateDraft = () => {
        this._suggestionDraft[field.dataset.suggest] = field.value;
        this._clearSuggestedPreview();
      };
      field.addEventListener("input", updateDraft);
      field.addEventListener("change", updateDraft);
    });
    this.shadowRoot.querySelectorAll("[data-history-range]").forEach((field) => {
      field.addEventListener("change", () => {
        if (field.dataset.historyRange === "start") this._historyStart = field.value;
        else this._historyEnd = field.value;
        this._historyExportResult = "";
      });
    });
    this.shadowRoot.querySelectorAll("[data-suggested-select]").forEach((field) => {
      field.addEventListener("change", () => {
        this._setMembership(this._selectedSuggestedRuleIds, field.dataset.suggestedSelect, field.checked);
        this._render();
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
    await this._callWS({ type: "industrial_alarm_panel/create_rule", rule: fields });
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
      system: "",
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
      system: rule.system || "",
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
        type: "industrial_alarm_panel/update_rule",
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

  async _previewSuggestedRules() {
    try {
      const result = await this._callWS({
        type: "industrial_alarm_panel/list_suggested_rules",
        ...this._suggestionPayload(),
      });
      this._suggestedRules = result?.suggested || [];
      this._selectedSuggestedRuleIds = new Set(this._suggestedRules.map((rule) => rule.id));
      this._suggestedRulesResult = this._suggestedRules.length
        ? this._t("previewing_suggested", { count: this._suggestedRules.length, entities: this._suggestedRules.length * 4 })
        : this._t("no_suggested_found");
    } catch (err) {
      this._suggestedRulesResult = err.message || String(err);
    }
    this._render();
  }

  async _createSelectedSuggestedRules() {
    await this._createSuggestedRules([...this._selectedSuggestedRuleIds]);
  }

  async _createAllSuggestedRules() {
    await this._createSuggestedRules(this._suggestedRules.map((rule) => rule.id));
  }

  _selectAllSuggestedRules() {
    this._selectedSuggestedRuleIds = new Set(this._suggestedRules.map((rule) => rule.id));
    this._render();
  }

  _deselectAllSuggestedRules() {
    this._selectedSuggestedRuleIds = new Set();
    this._render();
  }

  async _createSuggestedRules(ruleIds) {
    const count = ruleIds.length;
    if (!count) {
      this._suggestedRulesResult = this._t("select_before_create");
      this._render();
      return;
    }
    const estimatedEntities = count * 4;
    if (!window.confirm(this._t("confirm_create_suggested", { count, entities: estimatedEntities }))) return;
    try {
      const result = await this._callWS({
        type: "industrial_alarm_panel/create_suggested_rules",
        ...this._suggestionPayload(),
        rule_ids: ruleIds,
      });
      const createdCount = result?.created_count || 0;
      const skippedCount = result?.skipped_rule_ids?.length || 0;
      this._suggestedRulesResult = createdCount
        ? `${this._t("created_suggested", { count: createdCount, entities: createdCount * 4 })}${skippedCount ? this._t("skipped_suffix", { count: skippedCount }) : ""}`
        : this._t("no_new_suggested");
      this._selectedSuggestedRuleIds = new Set();
      await this._load();
    } catch (err) {
      this._suggestedRulesResult = err.message || String(err);
      this._render();
    }
  }

  async _deleteSelectedRules() {
    const ruleIds = [...this._selectedRuleIds];
    await this._deleteRules({ rule_ids: ruleIds }, ruleIds.length, this._t("label_selected_rules"));
  }

  async _exportRules() {
    try {
      const result = await this._callWS({ type: "industrial_alarm_panel/export_rules" });
      const blob = new Blob([result?.csv || ""], { type: "text/csv;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `industrial-alarm-rules-${new Date().toISOString().slice(0, 10)}.csv`;
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
        type: "industrial_alarm_panel/export_history",
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
      link.download = `industrial-alarm-history-${this._historyStart.replaceAll(":", "-")}-${this._historyEnd.replaceAll(":", "-")}.csv`;
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
        type: "industrial_alarm_panel/import_rules",
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

  async _removeAutoGeneratedRules() {
    const count = this._rules.filter((rule) => String(rule.id || "").startsWith("auto_")).length;
    await this._deleteRules({ generated_only: true }, count, this._t("label_auto_rules"));
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
        type: "industrial_alarm_panel/delete_rules",
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

  _suggestionPayload() {
    const fields = {};
    Object.entries(this._suggestionDraft).forEach(([key, value]) => {
      if (value !== "") fields[key] = Number(value);
    });
    return fields;
  }

  _clearSuggestedPreview() {
    this._suggestedRules = [];
    this._selectedSuggestedRuleIds = new Set();
    this._suggestedRulesResult = this._t("preview_again");
  }

  _setMembership(set, value, selected) {
    if (!value) return;
    if (selected) set.add(value);
    else set.delete(value);
  }

  _isEditingRulesForm() {
    const active = this.shadowRoot?.activeElement;
    if (this._tab !== "rules" || !active) return false;
    return Boolean(active.matches("[data-new], [data-suggest]"));
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
      :host { display: block; color: var(--iap-text); background: var(--iap-bg); min-height: var(--iap-min-height, 100vh); font-family: Arial, sans-serif; }
      .panel { min-height: var(--iap-min-height, 100vh); background: var(--iap-bg); color: var(--iap-text); }
      .theme-dark {
        --iap-bg: #101316; --iap-surface: #11161b; --iap-surface-alt: #14191f; --iap-header: #181d22; --iap-control: #202832; --iap-control-hover: #2a3541; --iap-text: #e6edf3; --iap-muted: #9fb1c1; --iap-heading-muted: #b8c7d4; --iap-border: #303942; --iap-border-soft: #28323c; --iap-selected-bg: #d9e2ec; --iap-selected-text: #101316; --iap-row-neutral: #252c33; --iap-row-neutral-text: #aebdcc; --iap-row-pending: #202832; --iap-row-pending-text: #dbe4ec; --iap-notice: #dbeafe; --iap-error-bg: #5b1c1c; --iap-error-text: #ffd5d5; --iap-error-border: #a83737;
      }
      .theme-light {
        --iap-bg: #f5f7fb; --iap-surface: #ffffff; --iap-surface-alt: #eef3f8; --iap-header: #ffffff; --iap-control: #ffffff; --iap-control-hover: #e8eef6; --iap-text: #1f2937; --iap-muted: #526170; --iap-heading-muted: #425466; --iap-border: #d7e0ea; --iap-border-soft: #e3e9f0; --iap-selected-bg: #1d4ed8; --iap-selected-text: #ffffff; --iap-row-neutral: #eef2f7; --iap-row-neutral-text: #526170; --iap-row-pending: #e7edf5; --iap-row-pending-text: #334155; --iap-notice: #1e40af; --iap-error-bg: #fee2e2; --iap-error-text: #7f1d1d; --iap-error-border: #fca5a5;
      }
      .topbar { display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 14px 18px; background: var(--iap-header); border-bottom: 1px solid var(--iap-border); }
      .menu-button { display: none; flex: 0 0 auto; }
      h1 { margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0; }
      .metrics { display: flex; gap: 10px; margin-top: 6px; color: var(--iap-muted); font-size: 13px; }
      .horn.on { color: #ffcf33; font-weight: 700; }
      .actions, .toolbar, .tabs, .rule-form, .bulk-actions, .bulk-summary { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
      button, select, input { background: var(--iap-control); color: var(--iap-text); border: 1px solid var(--iap-border); min-height: 34px; border-radius: 4px; padding: 0 10px; font-size: 14px; }
      input { min-width: 260px; }
      button { cursor: pointer; }
      button:hover { background: var(--iap-control-hover); }
      button:disabled { opacity: .45; cursor: default; }
      .primary { background: #2563eb; border-color: #3473ff; color: #ffffff; }
      .primary:hover { background: #1d4ed8; }
      .danger { background: #9f1d1d; border-color: #d23b3b; color: #ffffff; }
      .danger:hover { background: #831717; }
      .secondary { background: #30515d; border-color: #4b7b8c; color: #ffffff; }
      .secondary:hover { background: #3c6373; }
      .tabs { padding: 10px 18px; background: var(--iap-surface-alt); border-bottom: 1px solid var(--iap-border-soft); }
      .tabs button.selected { background: var(--iap-selected-bg); color: var(--iap-selected-text); border-color: var(--iap-selected-bg); }
      .toolbar { padding: 12px 18px; }
      .shelve-duration { display: flex; gap: 6px; align-items: center; color: var(--iap-heading-muted); font-size: 13px; }
      .history-export label { display: grid; gap: 4px; color: var(--iap-heading-muted); font-size: 12px; }
      .history-export input { min-width: 210px; }
      .history-export-result { margin-top: 0; }      
      .table-shell { overflow: auto; padding: 0 18px 18px; }
      table { width: 100%; border-collapse: collapse; background: var(--iap-surface); table-layout: auto; }
      th, td { border-bottom: 1px solid var(--iap-border-soft); padding: 8px 9px; text-align: left; font-size: 13px; white-space: nowrap; }
      th { background: var(--iap-control); color: var(--iap-heading-muted); position: sticky; top: 0; z-index: 1; }
      td:nth-child(6), td:nth-child(12) { white-space: normal; min-width: 180px; }
      tr { border-left: 6px solid #4b5563; }
      .alarm-row { background: var(--iap-surface); color: var(--iap-text); }
      .alarm-row td { border-bottom-color: rgba(16, 19, 22, .35); }
      .alarm-row button { background: rgba(16, 19, 22, .22); color: inherit; border-color: rgba(16, 19, 22, .4); }
      .alarm-row button:hover { background: rgba(16, 19, 22, .34); }
      .alarm-row.priority-critical.state-active-unack { background: #ef2b1d; color: #101316; border-left-color: #8f1711; }
      .alarm-row.priority-high.state-active-unack { background: #ff9f00; color: #101316; border-left-color: #a85b00; }
      .alarm-row.priority-medium.state-active-unack { background: #ffd800; color: #101316; border-left-color: #b69100; }
      .alarm-row.priority-low.state-active-unack { background: #58a6ff; color: #101316; border-left-color: #1d5fa8; }
      .alarm-row.priority-info.state-active-unack { background: #83d2e6; color: #101316; border-left-color: #34899f; }
      .alarm-row.priority-status.state-active-unack { background: #7ee787; color: #101316; border-left-color: #2f8a39; }
      .alarm-row.state-pending-color { background: var(--iap-row-pending); color: var(--iap-row-pending-text); border-left-color: #687585; }
      .alarm-row.state-cleared-unack { background: #d85b9d; color: #101316; border-left-color: #8e2f63; }
      .alarm-row.state-active-ack, .alarm-row.state-cleared-ack { background: #f3f4f6; color: #1f2933; border-left-color: #9ca3af; }
      .alarm-row.state-shelved, .alarm-row.state-disabled, .alarm-row.state-normal { background: var(--iap-row-neutral); color: var(--iap-row-neutral-text); border-left-color: #596675; }
      .badge { text-transform: uppercase; font-size: 12px; font-weight: 700; }
      .flash { animation: flashRow 1s step-end infinite; }
      @keyframes flashRow { 50% { filter: brightness(1.25); } }
      .empty, .error { color: var(--iap-muted); padding: 18px; }
      .error { margin: 12px 18px; color: var(--iap-error-text); background: var(--iap-error-bg); border: 1px solid var(--iap-error-border); }
      .rules, .settings { padding: 12px 18px 18px; }
      .suggested-rules { margin-bottom: 12px; padding: 10px; border: 1px solid var(--iap-border); background: var(--iap-surface); }
      .suggested-rules h2 { margin: 0 0 8px; font-size: 15px; font-weight: 700; letter-spacing: 0; color: var(--iap-text); }
      .suggested-rules-controls { display: flex; gap: 8px; align-items: end; flex-wrap: wrap; }
      .suggested-rules label { display: grid; gap: 4px; color: var(--iap-heading-muted); font-size: 12px; }
      .suggested-rules input { min-width: 90px; width: 110px; }
      .file-input { display: none; }
      .bulk-actions, .bulk-summary { margin-top: 8px; color: var(--iap-heading-muted); font-size: 13px; }
      .bulk-actions { margin-bottom: 10px; }
      .suggested-preview { margin-top: 8px; padding: 0; }
      .row-select { min-width: 0; width: 16px; height: 16px; padding: 0; }
      .notice { margin-top: 8px; color: var(--iap-notice); font-size: 13px; }
      .rule-form { margin-bottom: 12px; }
      .settings dl { display: grid; grid-template-columns: max-content minmax(120px, 1fr); gap: 10px 18px; max-width: 560px; }
      .settings dt { color: var(--iap-muted); }
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

// The dashboard card deliberately owns its rendering and data lifecycle.  The
// sidebar remains the full DCS console above; sharing that renderer here would
// re-introduce its tables, tabs and desktop interaction model.
class IndustrialAlarmPanelCard extends HTMLElement {
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
    const priorities = Array.isArray(config.priorities)
      ? config.priorities.map((value) => String(value).toLowerCase()).filter((value) => ["critical", "high", "medium", "low", "info", "status"].includes(value))
      : null;
    this._config = {
      ...config,
      title: config.title || "Industrial Alarms",
      header_icon: typeof config.header_icon === "string" && config.header_icon.trim() ? config.header_icon.trim() : "mdi:alarm-light",
      show_header_icon: config.show_header_icon !== false,
      header_icon_size: this._normalizeCssSize(config.header_icon_size, "24px"),
      title_font_size: this._normalizeCssSize(config.title_font_size, "1.15rem"),
      subtitle_font_size: this._normalizeCssSize(config.subtitle_font_size, ".85rem"),
      summary_font_size: this._normalizeCssSize(config.summary_font_size, ".78rem"),
      alarm_name_font_size: this._normalizeCssSize(config.alarm_name_font_size, "1rem"),
      alarm_meta_font_size: this._normalizeCssSize(config.alarm_meta_font_size, ".78rem"),
      priority_font_size: this._normalizeCssSize(config.priority_font_size, ".7rem"),
      action_font_size: this._normalizeCssSize(config.action_font_size, ".78rem"),
      view: views.has(requestedView) ? requestedView : "active",
      max_alarms: Math.max(0, Number.isFinite(Number(config.max_alarms)) ? Math.floor(Number(config.max_alarms)) : 5),
      show_summary: config.show_summary !== false,
      show_actions: config.show_actions !== false,
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
    this.style.setProperty("--iap-card-min-height", config.min_height || "0px");
    const sizeProperties = {
      "--iap-header-icon-size": this._config.header_icon_size,
      "--iap-title-font-size": this._config.title_font_size,
      "--iap-subtitle-font-size": this._config.subtitle_font_size,
      "--iap-summary-font-size": this._config.summary_font_size,
      "--iap-alarm-name-font-size": this._config.alarm_name_font_size,
      "--iap-alarm-meta-font-size": this._config.alarm_meta_font_size,
      "--iap-priority-font-size": this._config.priority_font_size,
      "--iap-action-font-size": this._config.action_font_size,
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
      const result = await this._hass.callWS({ type: "industrial_alarm_panel/list_alarms" });
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
    const payload = { type: `industrial_alarm_panel/${type}`, ...extra };
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
    history.pushState(null, "", "/industrial-alarms");
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
      ${this._config.hide_header ? "" : `<header><div class="heading">${this._config.show_header_icon ? `<ha-icon icon="${this._escape(this._config.header_icon)}" aria-hidden="true"></ha-icon>` : ""}<div><h2>${this._escape(this._config.title)}</h2><p>${this._t("metric_active", { count: active })} · ${this._t("metric_unack", { count: unack })}${this._sound.horn_active ? ` · ${this._t("horn_active")}` : ""}</p></div></div>${this._config.show_actions ? `<div class="header-actions"><button class="icon-button" data-action="silence" title="${this._t("silence")}" aria-label="${this._t("silence")}"><ha-icon icon="mdi:volume-off"></ha-icon></button><button class="icon-button" data-action="ack-all" title="${this._t("ack_all")}" aria-label="${this._t("ack_all")}"><ha-icon icon="mdi:check-all"></ha-icon></button></div>` : ""}</header>`}
      ${this._config.show_summary ? `<section class="summary" aria-label="Alarm summary"><span class="chip critical"><b>${count("critical")}</b> ${this._t("priority_critical")}</span><span class="chip high"><b>${count("high")}</b> ${this._t("priority_high")}</span><span class="chip unack"><b>${unack}</b> ${this._t("metric_unack", { count: "" }).trim()}</span><span class="chip"><b>💤 ${shelved}</b></span><span class="chip"><b>🚫 ${disabled}</b></span></section>` : ""}
      ${this._error ? `<div class="error" role="alert">${this._escape(this._error)}</div>` : ""}
      <section class="alarm-list">${shown.length ? shown.map((alarm) => this._alarmItem(alarm)).join("") : `<div class="empty"><ha-icon icon="mdi:check-circle-outline"></ha-icon><span>${this._t("no_alarms")}</span></div>`}</section>
      ${visible.length > shown.length ? `<button class="more" data-action="open-panel">+${visible.length - shown.length} more alarms</button>` : ""}
      ${this._config.show_open_panel ? `<footer><button data-action="open-panel">Open Industrial Alarm Panel <span aria-hidden="true">→</span></button></footer>` : ""}
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
    return `:host { display:block; min-width:0; font-family:inherit; --iap-critical:#d64545; --iap-high:#e17825; --iap-medium:#c79618; --iap-low:#4285b4; --iap-info:#477fc1; --iap-status:#718096; }
      .alarm-card { min-height:var(--iap-card-min-height, 0); overflow:visible; color:var(--primary-text-color); background:var(--ha-card-background, var(--card-background-color)); border-radius:var(--ha-card-border-radius, 12px); }
      .force-light { color-scheme:light; --primary-text-color:#202124; --secondary-text-color:#5f6368; --divider-color:#dfe1e5; --ha-card-background:#fff; }
      .force-dark { color-scheme:dark; --primary-text-color:#e8eaed; --secondary-text-color:#aab0b6; --divider-color:#45494e; --ha-card-background:#202124; }
      header { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; padding:16px 16px 10px; }
      .heading { display:flex; min-width:0; gap:12px; align-items:center; } .heading>ha-icon { width:var(--iap-header-icon-size, 24px); height:var(--iap-header-icon-size, 24px); --mdc-icon-size:var(--iap-header-icon-size, 24px); color:var(--error-color, var(--iap-critical)); flex:none; }
      h2 { margin:0; font-size:var(--iap-title-font-size, 1.15rem); line-height:1.3; font-weight:600; overflow-wrap:anywhere; } p { margin:3px 0 0; color:var(--secondary-text-color); font-size:.85rem; } header p { font-size:var(--iap-subtitle-font-size, .85rem); overflow-wrap:anywhere; }
      button { font:inherit; color:inherit; background:none; border:0; cursor:pointer; border-radius:var(--ha-card-border-radius, 12px); }
      button:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; } button:disabled { opacity:.45; cursor:default; }
      .header-actions { display:flex; gap:4px; flex:none; } .icon-button { display:grid; place-items:center; width:44px; height:44px; }
      .icon-button:hover, footer button:hover, .more:hover { background:color-mix(in srgb, var(--primary-text-color) 8%, transparent); }
      .summary { display:flex; flex-wrap:wrap; gap:7px; padding:4px 16px 12px; font-size:var(--iap-summary-font-size, .78rem); }
      .chip { display:inline-flex; gap:4px; align-items:center; padding:4px 9px; border:1px solid var(--divider-color); border-radius:999px; color:var(--secondary-text-color); font-size:inherit; }
      .chip.critical b { color:var(--iap-critical); } .chip.high b { color:var(--iap-high); } .chip.unack b { color:var(--warning-color, var(--iap-medium)); }
      .alarm-list { display:grid; gap:9px; padding:4px 12px 12px; min-width:0; }
      .alarm-item { --priority:var(--iap-status); position:relative; display:flex; min-width:0; border:1px solid var(--divider-color); border-radius:var(--ha-card-border-radius, 12px); background:color-mix(in srgb, var(--ha-card-background, var(--card-background-color)) 96%, var(--priority)); overflow:visible; }
      .priority-critical { --priority:var(--iap-critical); } .priority-high { --priority:var(--iap-high); } .priority-medium { --priority:var(--iap-medium); } .priority-low { --priority:var(--iap-low); } .priority-info { --priority:var(--iap-info); }
      .accent { width:4px; flex:none; background:var(--priority); border-radius:var(--ha-card-border-radius, 12px) 0 0 var(--ha-card-border-radius, 12px); } .alarm-content { padding:10px 12px; min-width:0; flex:1; border-radius:0 var(--ha-card-border-radius, 12px) var(--ha-card-border-radius, 12px) 0; }
      .alarm-leading, .alarm-footer { display:flex; justify-content:space-between; align-items:center; gap:10px; min-width:0; }
      .priority-badge { display:inline-flex; align-items:center; gap:6px; color:var(--priority); font-size:var(--iap-priority-font-size, .7rem); font-weight:700; letter-spacing:.04em; text-transform:uppercase; }
      .priority-dot { width:7px; height:7px; border-radius:50%; background:currentColor; } time, .alarm-tag, .alarm-context, .alarm-details { color:var(--secondary-text-color); font-size:var(--iap-alarm-meta-font-size, .78rem); }
      .alarm-name { margin:5px 0 2px; min-width:0; font-size:var(--iap-alarm-name-font-size, 1rem); font-weight:600; line-height:1.35; overflow-wrap:anywhere; } .alarm-tag { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
      .alarm-context { margin-top:3px; overflow-wrap:anywhere; } .alarm-footer { margin-top:7px; align-items:flex-end; } .alarm-details { min-width:0; overflow-wrap:anywhere; }
      .state { color:var(--primary-text-color); } .item-actions { position:relative; z-index:1; display:flex; flex:none; align-items:center; gap:3px; } .item-actions button { min-height:40px; padding:0 10px; color:var(--primary-color); font-size:var(--iap-action-font-size, .78rem); font-weight:600; text-transform:uppercase; }
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
      title: "Industrial Alarms",
      view: "active",
      max_alarms: 5,
      show_summary: true,
      show_actions: true,
      show_shelve_action: true,
      show_disable_action: true,
      show_restore_actions: true,
      show_open_panel: true,
      header_icon: "mdi:alarm-light",
      theme: "auto",
    };
  }
}

if (!customElements.get("industrial-alarm-panel")) {
  customElements.define("industrial-alarm-panel", IndustrialAlarmPanel);
}

if (!customElements.get("industrial-alarm-panel-card")) {
  customElements.define("industrial-alarm-panel-card", IndustrialAlarmPanelCard);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === "industrial-alarm-panel-card")) {
  window.customCards.push({
    type: "industrial-alarm-panel-card",
    name: "Industrial Alarm Panel",
    description: "Compact, responsive alarm summary for Home Assistant dashboards.",
    preview: true,
  });
}
