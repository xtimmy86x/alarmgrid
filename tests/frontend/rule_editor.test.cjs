const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { resolve } = require("node:path");
const { test } = require("node:test");
const vm = require("node:vm");

const source = readFileSync(resolve(__dirname, "../../custom_components/alarmgrid/frontend/dist/alarmgrid.js"), "utf8");

// Minimal DOM fixture: focus, ancestry and attribute selectors. Rendering is
// observed separately so a refresh cannot silently replace an active input.
class Element {
  constructor(attributes = {}, parent = null, tagName = "input") {
    this.attributes = attributes;
    this.parent = parent;
    this.tagName = tagName;
  }
  matches(selector) {
    return selector.split(",").some((part) => {
      const value = part.trim();
      if (/^[a-z]+$/.test(value)) return this.tagName === value;
      if (value.startsWith(".")) return (this.attributes.class || "").split(" ").includes(value.slice(1));
      const match = value.match(/^\[([^=\]]+)(?:=['"]([^'"]+)['"])?\]$/);
      return Boolean(match && Object.hasOwn(this.attributes, match[1]) && (match[2] === undefined || this.attributes[match[1]] === match[2]));
    });
  }
  closest(selector) {
    return this.matches(selector) ? this : this.parent?.closest(selector) || null;
  }
}

function fixture(attributes = { "data-condition-field": "entity_id" }) {
  const registry = new Map();
  const timers = [];
  const context = vm.createContext({
    HTMLElement: class {
      constructor() { this.style = { setProperty() {} }; }
      attachShadow() { this.shadowRoot = { activeElement: null }; }
    },
    customElements: { get: (name) => registry.get(name), define: (name, value) => registry.set(name, value) },
    window: { setTimeout: (callback) => { timers.push(callback); return timers.length; } },
    structuredClone,
  });
  vm.runInContext(source, context);
  const panel = new (registry.get("alarmgrid-panel"))();
  const form = new Element({ class: "rule-form" }, null, "div");
  const group = new Element({ "data-group-path": "root.0" }, form, "div");
  const isSelect = attributes["data-condition-field"] === "operator" || Object.hasOwn(attributes, "data-group-operator") || attributes["data-new"] === "priority";
  const field = new Element(attributes, group, isSelect ? "select" : "input");
  field.focus = () => { panel.shadowRoot.activeElement = field; };
  panel.shadowRoot.querySelector = (selector) => field.matches(selector) ? field : null;
  panel._tab = "rules";
  const rule = { id: "temperature", entity_id: "sensor.temperature", condition: "above", threshold: 25 };
  const alarm = { id: rule.id, lifecycle_state: "ACTIVE_UNACK" };
  panel._hass = { callWS: async () => ({ alarms: [alarm], rules: [rule], events: [], sound: {} }) };
  let renders = 0;
  panel._render = () => { renders += 1; panel.shadowRoot.activeElement = null; };
  field.focus();
  return { panel, field, rule, alarm, timers, registry, window: context.window, renders: () => renders };
}

for (const attributes of [
  { "data-condition-field": "entity_id" },
  { "data-condition-field": "operator" },
  { "data-condition-field": "value" },
  { "data-condition-field": "value_entity" },
  { "data-condition-field": "value_source" },
  { "data-condition-field": "lower" },
  { "data-condition-field": "upper" },
  { "data-condition-field": "deadband" },
  { "data-group-operator": "root.0" },
  { "data-new": "name" },
  { "data-new": "priority" },
]) {
  test(`poll preserves focused rule control ${JSON.stringify(attributes)} and still loads data`, async () => {
    const { panel, field, alarm, rule, renders } = fixture(attributes);
    await panel._load();
    assert.equal(renders(), 0);
    assert.equal(panel.shadowRoot.activeElement, field);
    assert.equal(panel._alarms[0], alarm);
    assert.equal(panel._rules[0], rule);
    assert.equal(panel._refreshing, false);
    panel.shadowRoot.activeElement = null;
    await panel._load();
    assert.equal(renders(), 1, "refresh resumes after leaving the form");
  });
}

test("websocket updates and delayed alarm colors preserve entity selection", async () => {
  const { panel, field, timers, renders } = fixture();
  panel._handleAlarmUpdateEvent({ data: {} });
  await new Promise(setImmediate);
  panel._scheduleAlarmVisualRefresh();
  timers.shift()();
  assert.equal(renders(), 0);
  assert.equal(panel.shadowRoot.activeElement, field);
});

test("failed background loads preserve the focused entity field", async () => {
  const { panel, field, renders } = fixture();
  panel._hass.callWS = async () => { throw new Error("Connection lost"); };
  await panel._load();
  assert.equal(panel._error, "Connection lost");
  assert.equal(panel.shadowRoot.activeElement, field);
  assert.equal(renders(), 0);
  assert.equal(panel._refreshing, false);
});

test("focus outside the rule form and other tabs do not block refresh", async () => {
  const { panel, renders } = fixture();
  panel.shadowRoot.activeElement = new Element({ "data-rule-select": "temperature" });
  await panel._load();
  assert.equal(renders(), 1);
  panel._tab = "active";
  await panel._load();
  assert.equal(renders(), 2);
});

test("focused form buttons allow action results to render", async () => {
  const { panel, field, renders } = fixture();
  panel.shadowRoot.activeElement = new Element({ "data-action": "update-rule" }, field.parent, "button");
  await panel._load();
  assert.equal(renders(), 1);
});

test("editing a rule focuses the entity control in the condition builder", () => {
  const { panel, field, rule, renders } = fixture();
  panel._rules = [rule];
  panel.shadowRoot.activeElement = null;
  panel._startEditRule(rule.id);
  assert.equal(renders(), 1);
  assert.equal(panel._editingRuleId, rule.id);
  assert.equal(panel.shadowRoot.activeElement, field);
  panel._cancelEditRule();
  assert.equal(panel._editingRuleId, null);
  assert.equal(renders(), 2, "explicit editor actions still render");
});

for (const [entitiesPerRule, expected] of [[1, 2], [4, 8], [undefined, 8]]) {
  test(`rule deletion estimate follows backend entity count ${entitiesPerRule}`, async () => {
    const { panel, rule, window } = fixture();
    panel._hass.callWS = async () => ({ rules: [rule], entities_per_rule: entitiesPerRule });
    await panel._load();
    let confirmation;
    panel._t = (key, values) => {
      if (key === "confirm_delete_rules") confirmation = values;
      return key;
    };
    // Stop at the confirmation, without performing a deletion.
    window.confirm = () => false;
    await panel._deleteRules({}, 2, "selected");
    assert.equal(confirmation.entities, expected);
  });
}


test("dynamic threshold survives edit, payload and advanced promotion", () => {
  const { panel, rule } = fixture();
  rule.threshold_entity = "input_number.limit";
  panel._rules = [rule];
  panel._startEditRule(rule.id);
  assert.equal(panel._ruleDraft.threshold_source, "entity");
  let payload = panel._rulePayload(panel._ruleDraft);
  assert.equal(payload.threshold_entity, "input_number.limit");
  assert.equal(payload.threshold, null);
  panel._promoteSimple();
  payload = panel._rulePayload(panel._ruleDraft);
  assert.equal(payload.condition_expression.conditions[0].value_entity, "input_number.limit");
  assert.equal(Object.hasOwn(payload.condition_expression.conditions[0], "value"), false);
  assert.equal(panel._ruleDraft.condition_expression.conditions[0].value, 25, "payload normalization must not mutate the live draft");
});

test("switching to fixed clears stale entity references and summary", () => {
  const { panel } = fixture();
  panel._ruleDraft = { entity_id: "sensor.temperature", condition: "above", threshold: 28, threshold_entity: "input_number.limit", threshold_source: "fixed" };
  let payload = panel._rulePayload(panel._ruleDraft);
  assert.equal(payload.threshold_entity, null);
  assert.equal(payload.threshold, 28);
  assert.equal(panel._draftConditionText(panel._ruleDraft).includes("input_number.limit"), false);
  const node = { type: "condition", entity_id: "sensor.temperature", operator: "above", value: 28, value_entity: "input_number.limit", value_source: "fixed" };
  panel._normalizeConditionDraft(node);
  assert.equal(Object.hasOwn(node, "value_entity"), false);
  assert.equal(node.value, 28);
});

test("unsupported comparison modes remove dynamic references", () => {
  const { panel } = fixture();
  const node = { type: "condition", entity_id: "sensor.temperature", operator: "is_on", value_entity: "input_number.limit", value_source: "entity" };
  panel._normalizeConditionDraft(node);
  assert.equal(Object.hasOwn(node, "value_entity"), false);
  const payload = panel._rulePayload({ entity_id: "sensor.temperature", condition: "is_on", threshold_source: "entity", threshold_entity: "input_number.limit" });
  assert.equal(payload.threshold_entity, null);
});

test("comparison row exposes current setpoint and escapes entity names", () => {
  const { panel } = fixture();
  panel._hass.states = { "input_number.limit": {state: "25", attributes: {friendly_name: "Limit <script>"}} };
  const markup = panel._conditionRow({ entity_id: "sensor.temperature", operator: "above", value_entity: "input_number.limit" }, "simple");
  assert(markup.includes('data-condition-field="value_source"'));
  assert(markup.includes('data-condition-field="value_entity"'));
  assert(markup.includes("Limit &lt;script&gt;"));
  assert(!markup.includes('data-condition-field="value"'));
});

test("card settings normalize invalid options and keep localized link fallback", () => {
  const { registry } = fixture();
  const card = new (registry.get("alarmgrid-card"))();
  card.setConfig({color_scheme:"neutral", flash_style:"none", open_panel_text:"  Alarm manager  "});
  assert.equal(card._config.color_scheme, "neutral");
  assert.equal(card._config.flash_style, "none");
  assert.equal(card._config.open_panel_text, "Alarm manager");
  card.setConfig({color_scheme:"bad", flash_style:"bad", open_panel_text:123});
  assert.equal(card._config.color_scheme, "default");
  assert.equal(card._config.flash_style, "panel");
  assert.equal(card._config.open_panel_text, "");
});

test("only unacknowledged card rows are marked for flashing", () => {
  const { registry } = fixture();
  const card = new (registry.get("alarmgrid-card"))();
  card.setConfig({});
  for (const state of ["ACTIVE_UNACK", "CLEARED_UNACK", "ACTIVE_ACK", "SHELVED", "DISABLED"]) {
    const html = card._alarmItem({id:"alarm", name:"Alarm", priority:"high", lifecycle_state:state});
    assert.equal(html.includes(" is-unack"), state.endsWith("_UNACK"), state);
  }
  assert(card._styles().includes("prefers-reduced-motion:reduce"));
  assert(card._styles().includes(".flash-panel .alarm-item.is-unack"));
  assert(card._styles().includes(".flash-subtle .is-unack .accent"));
});

test("visual card editor emits and restores the new preferences", () => {
  const { registry } = fixture();
  const editor = new (registry.get("alarmgrid-card-editor"))();
  editor._render = () => {};
  editor._syncDependentControls = () => {};
  let emitted;
  editor._emitConfigChanged = () => { emitted = {...editor._config}; };
  editor.setConfig({});
  editor._setStringOption("color_scheme", "neutral", "default");
  editor._setStringOption("flash_style", "none", "panel");
  editor._setStringOption("open_panel_text", "Open alarm manager");
  assert.equal(emitted.color_scheme, "neutral");
  assert.equal(emitted.flash_style, "none");
  assert.equal(emitted.open_panel_text, "Open alarm manager");
  editor._setStringOption("open_panel_text", "");
  assert.equal(Object.hasOwn(emitted, "open_panel_text"), false);
});
