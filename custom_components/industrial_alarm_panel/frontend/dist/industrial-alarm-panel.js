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
    silence: "Silence",
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
    priority_all: "all",
    priority_critical: "critical",
    priority_high: "high",
    priority_medium: "medium",
    priority_low: "low",
    priority_info: "info",
    priority_status: "status",
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
    placeholder_threshold: "Threshold",
    add_rule: "Add Rule",
    edit: "Edit",
    save_rule: "Save Rule",
    cancel: "Cancel",
    editing_rule: "Editing rule {id}",
    rule_updated: "Rule {id} updated",
    delete_selected: "Delete Selected",
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
    silence: "Silenzia",
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
    priority_all: "tutte",
    priority_critical: "critica",
    priority_high: "alta",
    priority_medium: "media",
    priority_low: "bassa",
    priority_info: "info",
    priority_status: "stato",
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
    placeholder_threshold: "Soglia",
    add_rule: "Aggiungi regola",
    edit: "Modifica",
    save_rule: "Salva regola",
    cancel: "Annulla",
    editing_rule: "Modifica della regola {id}",
    rule_updated: "Regola {id} aggiornata",
    delete_selected: "Elimina selezionate",
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
  },
};

class IndustrialAlarmPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._alarms = [];
    this._history = [];
    this._rules = [];
    this._ruleDraft = {
      id: "",
      entity_id: "",
      name: "",
      condition: "above",
      threshold: "",
      priority: "medium",
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
        <td><span class="badge">${alarm.priority}</span></td>
        <td>${this._escape(alarm.area || "")}</td>
        <td>${this._escape(alarm.system || "")}</td>
        <td>${this._escape(alarm.tag || alarm.id)}</td>
        <td>${this._escape(alarm.name)}</td>
        <td>${this._escape(String(alarm.last_value ?? alarm.last_source_state ?? ""))}</td>
        <td>${this._escape(alarm.lifecycle_state)}</td>
        <td>${this._time(alarm.shelve_expiry)}</td>
        <td><button data-ack="${this._escape(alarm.id)}" ${alarm.acknowledged ? "disabled" : ""}>${this._t("ack")}</button></td>
        <td><button data-shelve="${this._escape(alarm.id)}" ${alarm.shelved || alarm.disabled ? "disabled" : ""}>${this._t("shelve")}</button></td>
        <td>${this._escape(alarm.instructions || "")}</td>
      </tr>
    `;
  }

  _historyView() {
    return `
      <section class="table-shell">
        <table data-table-id="history">
          <thead><tr><th>${this._t("col_time")}</th><th>${this._t("col_event")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_area")}</th><th>${this._t("col_tag")}</th><th>${this._t("col_alarm")}</th><th>${this._t("col_from")}</th><th>${this._t("col_to")}</th><th>${this._t("col_operator")}</th></tr></thead>
          <tbody>
            ${this._history.length ? this._history.map((event) => `
              <tr>
                <td>${this._time(event.timestamp)}</td>
                <td>${this._escape(event.event_type)}</td>
                <td>${this._escape(event.priority || "")}</td>
                <td>${this._escape(event.area || "")}</td>
                <td>${this._escape(event.tag || event.rule_id || "")}</td>
                <td>${this._escape(event.name || event.message || "")}</td>
                <td>${this._escape(event.previous_state || "")}</td>
                <td>${this._escape(event.new_state || "")}</td>
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
        </div>
        <div class="table-shell">
          <table data-table-id="rules">
            <thead><tr><th></th><th>${this._t("col_id")}</th><th>${this._t("col_entity")}</th><th>${this._t("col_name")}</th><th>${this._t("col_condition")}</th><th>${this._t("col_priority")}</th><th>${this._t("col_enabled")}</th><th></th></tr></thead>
            <tbody>${this._rules.length ? this._rules.map((rule) => `<tr><td><input class="row-select" type="checkbox" data-rule-select="${this._escape(rule.id)}" ${this._selectedRuleIds.has(rule.id) ? "checked" : ""}></td><td>${this._escape(rule.id)}</td><td>${this._escape(rule.entity_id)}</td><td>${this._escape(rule.name)}</td><td>${this._escape(rule.condition)}</td><td>${this._t(`priority_${rule.priority}`)}</td><td>${rule.enabled ? this._t("yes") : this._t("no")}</td><td><button data-edit-rule="${this._escape(rule.id)}">${this._t("edit")}</button></td></tr>`).join("") : `<tr><td colspan="8" class="empty">${this._t("no_rules")}</td></tr>`}</tbody>
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
    Object.keys(changes).forEach((key) => {
      if (changes[key] === "") delete changes[key];
    });
    if (changes.threshold !== undefined) changes.threshold = Number(changes.threshold);
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

class IndustrialAlarmPanelCard extends IndustrialAlarmPanel {
  constructor() {
    super();
    this._title = "";
    this._hideTabs = false;
    this._hideHeader = false;
    this._themeMode = "auto";
  }

  setConfig(config = {}) {
    const validTabs = new Set(["active", "unacknowledged", "history", "shelved", "disabled", "rules", "settings"]);
    this._cardConfig = config;
    this._title = config.title || "";
    this._tab = validTabs.has(config.tab) ? config.tab : "active";
    this._hideTabs = Boolean(config.hide_tabs);
    this._hideHeader = Boolean(config.hide_header);
    this._themeMode = ["auto", "light", "dark"].includes(config.theme) ? config.theme : "auto";
    this.style.setProperty("--iap-min-height", config.min_height || "0");
    if (this._rendered) this._render();
  }

  getCardSize() {
    return this._hideTabs ? 6 : 8;
  }

  static getStubConfig() {
    return {
      title: "Industrial Alarms",
      tab: "active",
      hide_tabs: false,
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
    description: "Industrial Alarm Panel alarms, history, rules, and sound controls as a Lovelace card.",
    preview: true,
  });
}