const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const P = require('../progress.js');
const base = path.join(__dirname, '..');
function app(saved = null, failWrites = false) {
  const elements = new Map();
  const get = id => {
    if (!elements.has(id)) elements.set(id, {textContent: '', value: '', hidden: true, style: {setProperty() {}}, classList: {add() {}, remove() {}, toggle() {}}, setAttribute() {}, addEventListener() {}, querySelectorAll: () => [], scrollIntoView() {}, focus() {}});
    return elements.get(id);
  };
  let stored = saved;
  const context = vm.createContext({CourseProgress: P, console, setTimeout, clearTimeout,
    localStorage: {getItem: () => stored, setItem: (_, value) => { if (failWrites) throw new Error('quota'); stored = value; }},
    document: {getElementById: get, querySelectorAll: () => [], querySelector: get},
    window: {innerWidth: 1200, confirm: () => true}});
  vm.runInContext(fs.readFileSync(path.join(base, 'study.js'), 'utf8'), context);
  vm.runInContext(fs.readFileSync(path.join(base, 'curriculum-updates.js'), 'utf8'), context);
  vm.runInContext(fs.readFileSync(path.join(base, 'app.js'), 'utf8'), context);
  return {get, run: code => vm.runInContext(code, context), stored: () => stored};
}
test('all 16 weeks have study guidance and core learning content', () => {
  const a = app();
  assert.equal(a.run('weeks.length'), 16);
  assert.equal(a.run('weeks.every(w => w.study.prerequisite && w.study.core && w.study.stretch && w.resources.some(r => !r.optional) && w.assignment && w.failure && w.exit.length && w.deliverables.length)'), true);
});
test('legacy progress retains exact checkpoint keys and gains notes', () => {
  const a = app(JSON.stringify({activeWeek: 12, checked: {'1:resource:3': true, '12:exit:2': true}}));
  assert.equal(a.run('state.activeWeek'), 12);
  assert.equal(a.run('state.checked["1:resource:3"]'), true);
  assert.equal(a.run('state.checked["12:exit:2"]'), true);
  assert.equal(a.run('Object.keys(state.notes).length'), 0);
});
test('optional readings do not affect core completion', () => {
  const a = app(); const before = a.run('weekStats(weeks[0]).done');
  a.run('setChecked(weeks[0], "resource", 3, true)');
  assert.equal(a.run('weekStats(weeks[0]).done'), before);
});
test('next action finds gaps rather than using the number completed', () => {
  const a = app(); a.run('setChecked(weeks[0], "resource", 2, true)');
  assert.equal(a.run('CourseProgress.next(weeks,state).key'), '1:resource:0');
});
test('next action wraps back from week 16 to earlier unfinished work', () => {
  const a = app(); a.run('state.activeWeek=16; CourseProgress.tasks(weeks[15]).forEach(t => state.checked[t.key]=true)');
  assert.equal(a.run('CourseProgress.next(weeks,state).week'), 1);
});
test('fully complete course ends correctly and percentage reaches 100', () => {
  const a = app(); a.run('weeks.forEach(w => CourseProgress.tasks(w).forEach(t => state.checked[t.key]=true))');
  assert.equal(a.run('CourseProgress.next(weeks,state)'), null);
  assert.equal(a.run('courseStats().percent'), 100);
});
test('first checkpoint has visible nonzero course progress', () => {
  const a = app(); a.run('setChecked(weeks[0], "resource", 0, true)');
  assert.ok(a.run('courseStats().percent') > 0);
});
test('backup validation round-trips notes and rejects unsafe shapes', () => {
  const input = {activeWeek: 4, checked: {'4:exit:1': true}, notes: {'4': 'Next: compare two prompts'}};
  assert.deepEqual(P.validate(JSON.parse(JSON.stringify(input))), input);
  for (const bad of [null, {}, {checked: []}, {checked: {'__proto__': true, bad: true}}, {checked: {'1:exit:0': 'yes'}}, {checked: {}, notes: {'1': 'x'.repeat(20001)}}]) assert.throws(() => P.validate(bad));
});
test('corrupt stored data is not silently overwritten', () => {
  const a = app('{broken');
  assert.equal(a.run('saveState()'), false);
  assert.equal(a.stored(), '{broken');
  assert.equal(a.get('storage-warning').hidden, false);
});
test('quota failure warns instead of claiming progress was saved', () => {
  const a = app(null, true);
  assert.equal(a.run('setChecked(weeks[0], "resource", 0, true)'), false);
  assert.match(a.get('save-status').textContent, /Not saved/);
  assert.equal(a.run('state.checked["1:resource:0"]'), true);
});
test('notes survive a reload and remain week-specific', () => {
  const a = app(); a.run('state.notes[1]="Revisit schema refusals"; saveState()');
  const b = app(a.stored());
  assert.equal(b.get('week-notes').value, 'Revisit schema refusals');
  b.run('state.activeWeek=2; render()');
  assert.equal(b.get('week-notes').value, '');
});
test('invalid active week safely falls back to week one', () => {
  assert.equal(P.validate({activeWeek: 999, checked: {}}).activeWeek, 1);
});

const previousWeeks = require('./fixtures/curriculum-before-20260911.json');
const updatedIds = [2, 4, 6, 7, 9, 10, 11, 13, 14, 15, 16];
test('all original content and positional checkpoints remain intact', () => {
  const a = app(); const current = JSON.parse(a.run('JSON.stringify(weeks)'));
  for (const before of previousWeeks) {
    const after = current.find(w => w.id === before.id);
    for (const field of ['id','month','title','goal','assignment','failure']) assert.equal(after[field], before[field], `week ${before.id} ${field}`);
    for (const kind of ['deliverables','exit']) assert.deepEqual(after[kind].slice(0,before[kind].length),before[kind],`week ${before.id} ${kind} prefix`);
    before.resources.forEach((r,i) => {
      for (const field of ['title','url','focus','optional']) assert.equal(after.resources[i][field],r[field],`week ${before.id} resource ${i} ${field}`);
    });
    if (updatedIds.includes(before.id)) {
      assert.ok(after.exit.length > before.exit.length);
      assert.ok(after.deliverables.length > before.deliverables.length);
    } else {
      assert.equal(after.exit.length, before.exit.length);
      assert.equal(after.deliverables.length,before.deliverables.length);
    }
  }
});
test('fully completed legacy backup preserves checks and notes but leaves new work unfinished', () => {
  const saved = {activeWeek: 13, checked: {}, notes: {'13':'Keep my model comparison'}};
  for (const week of previousWeeks) {
    for (const [kind, items] of [['resource',week.resources],['assignment',[0]],['deliverable',week.deliverables],['exit',week.exit]]) items.forEach((_,i)=>saved.checked[`${week.id}:${kind}:${i}`]=true);
  }
  const a = app(JSON.stringify(saved));
  assert.deepEqual(JSON.parse(a.run('JSON.stringify(state)')),saved);
  assert.ok(a.run('courseStats().percent') < 100);
  assert.equal(a.run('courseStats().complete'),5);
  assert.equal(a.run('CourseProgress.next(weeks,state).key'), '13:deliverable:4');
  assert.equal(a.get('week-notes').value, saved.notes['13']);
  a.run('saveState()');
  assert.deepEqual(JSON.parse(a.stored()),saved);
});
test('new resource levels are explicit and only Required readings gate completion', () => {
  const a = app();
  assert.equal(a.run('weeks.every(w => w.resources.every(r => ["Required","Recommended","Optional"].includes(r.level) && r.optional === (r.level !== "Required")))'),true);
  a.run('weeks.forEach(w => w.resources.forEach((r,i) => {if(r.level !== "Required") state.checked[`${w.id}:resource:${i}`]=true}))');
  assert.equal(a.run('courseStats().done'),0);
});
test('progress denominator includes every appended required item exactly once', () => {
  const a = app();
  assert.equal(a.run('courseStats().total'),a.run('weeks.reduce((n,w)=>n+w.resources.filter(r=>!r.optional).length+1+w.deliverables.length+w.exit.length,0)'));
  assert.equal(a.run('new Set(weeks.flatMap(w=>CourseProgress.tasks(w).map(t=>t.key))).size'),a.run('courseStats().total'));
});
test('new checks survive saving, validation and reload', () => {
  const a = app(); a.run('state.checked["13:exit:6"]=true; state.notes[13]="Router report"; saveState()');
  const b = app(a.stored());
  assert.equal(b.run('state.checked["13:exit:6"]'),true);
  assert.equal(b.run('state.notes[13]'),'Router report');
});
test('all 16 weeks render outcomes, experiments and note prompts without stale extensions', () => {
  const a = app();
  for (let id=1;id<=16;id++) {
    a.run(`state.activeWeek=${id}; render()`);
    assert.ok(a.get('reading-outcomes').innerHTML.length);
    assert.ok(a.get('note-prompt').textContent.length);
    assert.equal(a.get('extension-build').hidden,!updatedIds.includes(id));
    assert.equal(a.get('extension-experiments').hidden,!updatedIds.includes(id));
  }
});
test('new curriculum contains the requested technical contracts', () => {
  const a = app();
  const required = {
    2:['ToolError','retryable','500','malformed','empty','unauthorized','duplicate'],
    4:['Prompt Registry','created_at','eval_dataset','eval_score','dataset_version','unsupported_claim_rate','rollback'],
    6:['BM25','Dense','Hybrid','reranker','TX_ALREADY_EXISTS','metadata'],
    7:['NDCG','Precision','Recall','MRR','cross-encoder','50','top 5'],
    9:['assemble_context','max_tokens','context_tokens','retrieved_tokens','tool_result_tokens','conversation_tokens','tokens_dropped','tokens_summarized','12,500'],
    10:['correct_tool_selection','unnecessary_tool_calls','duplicate_tool_calls','steps_to_resolution','tool_error_recovery','trajectory_success'],
    11:['LangGraph','Temporal','checkpoint','replay','idempotency','deterministic'],
    13:['cheap','normal','strong','tenant budget','latency SLO','3 percentage points','5%','100%','fail closed'],
    14:['TTFT','tokens_per_second','Semantic Cache','state','invalidation','incorrect_stale_hits'],
    15:['ReadOnlyInvestigator','refund_payment','change_payment_status','rotate_key','indirect prompt injection','replayed'],
    16:['Data Flywheel','thumbs down','human corrections','agent failures','tool failures','low-confidence','production incidents','fallback','human escalation']
  };
  for(const [id, phrases] of Object.entries(required)) {
    const text=a.run(`JSON.stringify(curriculumUpdates[${id}])`);
    for(const phrase of phrases) assert.ok(text.toLowerCase().includes(phrase.toLowerCase()),`week ${id}: ${phrase}`);
  }
  assert.equal(a.run('weeks[5].study.stretch.includes("Hybrid retrieval and the reranker experiment are required")'),true);
});
