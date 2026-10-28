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
  return { panel, field, rule, alarm, timers, renders: () => renders };
}

for (const attributes of [
  { "data-condition-field": "entity_id" },
  { "data-condition-field": "operator" },
  { "data-condition-field": "value" },
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
