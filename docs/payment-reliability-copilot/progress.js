/* Shared by the browser and the dependency-free regression tests. */
(function (root) {
  const blank = () => ({ activeWeek: 1, checked: {}, notes: {} });
  function validate(input) {
    if (!input || typeof input !== 'object' || Array.isArray(input) ||
        !input.checked || typeof input.checked !== 'object' || Array.isArray(input.checked)) {
      throw new Error('Choose a course progress backup.');
    }
    const result = blank();
    if (Number.isInteger(Number(input.activeWeek)) && Number(input.activeWeek) >= 1 && Number(input.activeWeek) <= 16) result.activeWeek = Number(input.activeWeek);
    for (const [key, value] of Object.entries(input.checked)) {
      if (!/^(?:[1-9]|1[0-6]):(?:resource|assignment|deliverable|exit):\d{1,3}$/.test(key) || typeof value !== 'boolean') throw new Error('This backup contains invalid checkpoints.');
      result.checked[key] = value;
    }
    if (input.notes !== undefined) {
      if (!input.notes || typeof input.notes !== 'object' || Array.isArray(input.notes)) throw new Error('This backup contains invalid notes.');
      for (const [key, value] of Object.entries(input.notes)) {
        if (!/^(?:[1-9]|1[0-6])$/.test(key) || typeof value !== 'string' || value.length > 20000) throw new Error('This backup contains invalid notes.');
        result.notes[key] = value;
      }
    }
    return result;
  }
  function tasks(week) {
    return [
      ...week.resources.flatMap((r, i) => r.optional ? [] : [{ kind: 'resource', index: i, label: r.title }]),
      { kind: 'assignment', index: 0, label: 'Build and run the failure pass' },
      ...week.deliverables.map((label, index) => ({ kind: 'deliverable', index, label })),
      ...week.exit.map((label, index) => ({ kind: 'exit', index, label }))
    ].map(task => ({ ...task, key: `${week.id}:${task.kind}:${task.index}` }));
  }
  function stats(week, state) {
    const items = tasks(week);
    const done = items.filter(task => state.checked[task.key] === true).length;
    return { total: items.length, done, percent: Math.round(done / items.length * 1000) / 10 };
  }
  function next(weeks, state) {
    const ordered = [...weeks.filter(w => w.id >= state.activeWeek), ...weeks.filter(w => w.id < state.activeWeek)];
    for (const week of ordered) {
      const task = tasks(week).find(item => !state.checked[item.key]);
      if (task) return { week: week.id, ...task };
    }
    return null;
  }
  const api = { blank, validate, tasks, stats, next };
  if (typeof module !== 'undefined') module.exports = api;
  else root.CourseProgress = api;
})(globalThis);
