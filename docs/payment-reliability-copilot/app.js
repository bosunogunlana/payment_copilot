const months = [
  { id: 1, label: 'LLMs as software', short: 'LLM foundations', weeks: '01—04' },
  { id: 2, label: 'Grounding & RAG', short: 'Grounding + RAG', weeks: '05—08' },
  { id: 3, label: 'Agentic systems', short: 'Agents + MCP', weeks: '09—12' },
  { id: 4, label: 'Production AI', short: 'Production craft', weeks: '13—16' }
];

const resource = (title, url, focus) => ({ title, url, focus });

const weeks = [
  {
    id: 1, month: 1, title: 'Models, prompting & structured output', goal: 'Treat the LLM as an unreliable software component with measurable behavior—not as a chatbot.',
    resources: [
      resource('OpenAI Developer Quickstart', 'https://developers.openai.com/api/docs/quickstart', 'Responses API + Python SDK'),
      resource('Prompt engineering guide', 'https://developers.openai.com/api/docs/guides/prompt-engineering', 'Instruction hierarchy, context, examples'),
      resource('Structured outputs', 'https://developers.openai.com/api/docs/guides/structured-outputs', 'JSON-schema constrained generation'),
      resource('Pydantic models', 'https://docs.pydantic.dev/latest/concepts/models/', 'Application-side validation')
    ],
    assignment: 'Build Payment Diagnosis Service v0. Accept a payment and its event history, then return a typed diagnosis: status, category, likely cause, recommended action, and confidence. Compare two model configurations.',
    failure: 'Create 30 labelled scenarios. Deliberately include missing events, conflicting signals, and plausible-but-wrong causes. Record validity, confidence, latency, tokens, and cost.',
    deliverables: ['app/llm/diagnose.py', 'app/models/diagnosis.py', 'evals/datasets/week1.jsonl', 'docs/learning-notes/week1.md'],
    exit: ['All responses satisfy the application schema', 'At least 30 labelled scenarios are stored', 'Explain temperature and sampling conceptually', 'Explain context-window constraints', 'Explain why structured output does not guarantee factual correctness', 'Measured cost and latency instead of guessing']
  },
  {
    id: 2, month: 1, title: 'Function calling & tool design', goal: 'Understand the core mechanism behind agents: the model requests work, your application validates and executes it.',
    resources: [
      resource('Function calling guide', 'https://developers.openai.com/api/docs/guides/function-calling', 'Tool definitions, calls, and results'),
      resource('JSON Schema', 'https://json-schema.org/learn/getting-started-step-by-step', 'Validate tool arguments at the boundary'),
      resource('OpenAI API reference', 'https://platform.openai.com/docs/api-reference/responses', 'Inspect the response/tool-call shape')
    ],
    assignment: 'Create four deterministic fixture-backed tools: get_payment, get_payment_events, get_ledger_entries, and get_provider_status. Implement the orchestration loop yourself—no agent framework.',
    failure: 'Make tools return unknown IDs, invalid providers, malformed arguments, timeouts, 500s, empty responses, and payment-not-found. Add an explicit maximum tool-step count.',
    deliverables: ['app/tools/', 'app/llm/tool_loop.py', 'simulator/fixtures/', 'evals/datasets/tool_selection.jsonl'],
    exit: ['≥90% correct first tool selection across 40 scenarios', '100% tool arguments are schema-valid', 'Authorization is performed by the application', 'A maximum tool-step count exists', 'Timeouts cannot create infinite retries', 'Draw the full tool-calling lifecycle from memory']
  },
  {
    id: 3, month: 1, title: 'Practical machine-learning foundations', goal: 'Build enough classical ML intuition to know when a deterministic or statistical model is the better tool.',
    resources: [
      resource('Google ML Crash Course', 'https://developers.google.com/machine-learning/crash-course/', 'Classification, generalization, overfitting'),
      resource('Classification metrics', 'https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall', 'Precision, recall, F1'),
      resource('scikit-learn model evaluation', 'https://scikit-learn.org/stable/modules/model_evaluation.html', 'Metric definitions + reporting')
    ],
    assignment: 'Generate roughly 1,000 payment-support messages across seven labels. Compare TF-IDF + logistic regression against an LLM structured classifier using train, validation, and test splits.',
    failure: 'Inspect the confusion matrix. Find the class where a false positive is most costly, then decide whether accuracy or recall should lead your deployment recommendation.',
    deliverables: ['experiments/classical_classifier.py', 'experiments/llm_classifier.py', 'data/payment_issues.csv', 'docs/learning-notes/classifier-comparison.md'],
    exit: ['Explain training vs inference', 'Explain train, validation, and test data', 'Explain overfitting', 'Explain precision vs recall and when F1 helps', 'Name a task where a $0 deterministic classifier wins', 'Write a deployment recommendation']
  },
  {
    id: 4, month: 1, title: 'Evaluation-driven development', goal: 'Make evals part of development so a prompt change can be judged objectively.',
    resources: [
      resource('OpenAI Evals guide', 'https://developers.openai.com/api/docs/guides/evals', 'Datasets, graders, and repeatable runs'),
      resource('How evals drive AI development', 'https://openai.com/index/evals-drive-next-chapter-of-ai/', 'Specify → Measure → Improve'),
      resource('OpenAI evaluation best practices', 'https://platform.openai.com/docs/guides/evals', 'Error analysis and representative examples')
    ],
    assignment: 'Build a reusable eval runner that reports accuracy, schema compliance, tool correctness, unsupported claims, latency, token usage, and estimated cost. Create an error taxonomy.',
    failure: 'Run at least one prompt change you expect to help that makes an eval worse. Keep the before/after report and classify why.',
    deliverables: ['evals/runner.py', 'evals/datasets/golden_set.jsonl', 'evals/reports/week4.md', 'evals/error_taxonomy.yml'],
    exit: ['Golden set contains at least 75 cases', 'Eval execution is reproducible', 'Scores are broken down by category', 'Model and prompt metadata are stored', 'A before/after comparison exists', 'You can distinguish a better score from a lucky sample']
  },
  {
    id: 5, month: 2, title: 'Embeddings & semantic retrieval', goal: 'Understand vector retrieval from first principles before reaching for a vector database.',
    resources: [
      resource('OpenAI embeddings guide', 'https://developers.openai.com/api/docs/guides/embeddings', 'Embedding inputs, dimensions, and search'),
      resource('pgvector documentation', 'https://github.com/pgvector/pgvector', 'Exact search, HNSW, and IVFFlat'),
      resource('NumPy dot product', 'https://numpy.org/doc/stable/reference/generated/numpy.dot.html', 'Build similarity with plain arrays')
    ],
    assignment: 'Create a 20-document payment knowledge corpus. Implement embed_document, embed_query, cosine_similarity, and search_similar_documents first with Python arrays, then migrate behind the same interface to PostgreSQL + pgvector.',
    failure: 'Probe queries for delayed withdrawals, broadcast-but-processing transactions, and missing callbacks. Inspect nearest neighbours manually and write down false friends.',
    deliverables: ['app/retrieval/embeddings.py', 'app/retrieval/vector_store.py', 'knowledge/', 'scripts/index_documents.py'],
    exit: ['Explain what an embedding represents', 'Implement cosine similarity', 'Explain semantic vs keyword search', 'Explain exact vs approximate nearest-neighbour search', 'Explain why embeddings are not knowledge', 'Name a case where similarity is not relevance']
  },
  {
    id: 6, month: 2, title: 'Build RAG manually', goal: 'Trace every stage from a question to a cited answer before adding a framework.',
    resources: [
      resource('OpenAI retrieval guide', 'https://developers.openai.com/api/docs/guides/retrieval', 'Search, ranking, and grounded answers'),
      resource('Retrieval-augmented generation course', 'https://www.deeplearning.ai/courses/retrieval-augmented-generation', 'Optional reinforcement for gaps'),
      resource('OpenAI citations pattern', 'https://platform.openai.com/docs/guides/retrieval', 'Return evidence with the answer')
    ],
    assignment: 'Build Payment Knowledge Assistant as a manual pipeline: query preprocessing → embedding → retrieval → context selection → prompt construction → LLM → answer + citations.',
    failure: 'Compare chunk sizes 250 / 500 / 1,000 and top-k 3 / 5 / 10. Keep the output and record whether the failure came from query understanding, retrieval, source quality, context, or generation.',
    deliverables: ['app/retrieval/chunker.py', 'app/retrieval/retriever.py', 'app/rag/pipeline.py', 'experiments/rag_chunking.md'],
    exit: ['Trace a wrong answer to a pipeline stage', 'Answer, evidence, and source are separate in the UI', 'At least three chunk sizes are compared', 'At least three top-k values are compared', 'Every answer carries source identifiers', 'You can explain why more context can reduce quality']
  },
  {
    id: 7, month: 2, title: 'Retrieval evaluation', goal: 'Evaluate the retrieval layer separately from generation so “bad answer” has a diagnosable cause.',
    resources: [
      resource('Information retrieval metrics', 'https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics', 'Precision, recall, and ranking metrics'),
      resource('OpenAI Evals guide', 'https://developers.openai.com/api/docs/guides/evals', 'Golden cases and graders'),
      resource('Ragas documentation', 'https://docs.ragas.io/en/stable/', 'Optional reference for RAG evaluation concepts')
    ],
    assignment: 'Create 50 retrieval-specific test cases with relevant document IDs and required facts. Calculate Precision@K, Recall@K, MRR, correctness, faithfulness, citation correctness, and completeness.',
    failure: 'Add unanswerable questions, conflicting documents, outdated documents, and irrelevant documents that share vocabulary. Report retrieval failure separately from generation failure.',
    deliverables: ['evals/retrieval/', 'evals/rag/', 'evals/reports/week7.md'],
    exit: ['Dataset contains 50 retrieval cases', 'Recall@5 is measured', 'Citation precision is measured', 'Unanswerable questions are represented', 'Retrieval and generation failures are separate', 'Your report includes an error taxonomy and next action']
  },
  {
    id: 8, month: 2, title: 'Production RAG & multi-tenancy', goal: 'Turn “chat with documents” into a trustworthy knowledge subsystem with identity, freshness, and deletion semantics.',
    resources: [
      resource('PostgreSQL row-level security', 'https://www.postgresql.org/docs/current/ddl-rowsecurity.html', 'Database-enforced tenant boundaries'),
      resource('pgvector metadata filtering', 'https://github.com/pgvector/pgvector', 'Filter vectors with application metadata'),
      resource('OpenAI retrieval guide', 'https://developers.openai.com/api/docs/guides/retrieval', 'Grounding and source attribution')
    ],
    assignment: 'Add organization_id, document_version, source_type, effective_date, access_level, provider, and network to every chunk. Implement tenant-aware search, re-indexing, deletion, retries, version replacement, and deduplication.',
    failure: 'Create Org A and Org B with deliberately similar documents. Attempt cross-tenant leakage, stale-version retrieval, duplicate ingestion, and retrieval after deletion.',
    deliverables: ['app/ingestion/', 'app/retrieval/filters.py', 'evals/security/tenant_retrieval.jsonl', 'docs/rag-architecture.md'],
    exit: ['Zero cross-tenant retrieval in tests', 'Deleted documents disappear from search', 'Updated documents replace stale versions', 'Generated claims identify their source', 'Ingestion failures are observable', 'Paqet Copilot v0.2 can ground an operator answer']
  },
  {
    id: 9, month: 3, title: 'Build an agent yourself', goal: 'Understand an agent without framework magic: state, decisions, validated actions, observations, and termination.',
    resources: [
      resource('OpenAI function calling guide', 'https://developers.openai.com/api/docs/guides/function-calling', 'Tools as application-owned actions'),
      resource('Reasoning best practices', 'https://developers.openai.com/api/docs/guides/reasoning-best-practices', 'Reasoning settings and response design'),
      resource('ReAct paper', 'https://arxiv.org/abs/2210.03629', 'Reasoning + acting as an observable loop')
    ],
    assignment: 'Implement a bounded agent loop for “Why is payment pay_123 still processing?” Store observable trajectories: requested tool, arguments, result, timing, and final answer. Do not depend on private chain-of-thought.',
    failure: 'Force an infinite loop, repeated tool call, timeout, incorrect tool data, conflicting tools, and no-answer scenario. Make each failure a typed observation.',
    deliverables: ['app/agents/loop.py', 'app/agents/state.py', 'evals/agent/baseline.jsonl', 'docs/learning-notes/week9.md'],
    exit: ['MAX_STEPS is enforced', 'A timeout budget exists', 'A retry budget exists', 'Tool calls are validated', 'Termination conditions are explicit', 'Agent completes ≥80% of baseline investigations']
  },
  {
    id: 10, month: 3, title: 'Incident investigation agent', goal: 'Move from a single payment diagnosis to a system-level production investigation with metrics, logs, history, and provider state.',
    resources: [
      resource('OpenTelemetry concepts', 'https://opentelemetry.io/docs/concepts/observability-primer/', 'Signals, traces, and context'),
      resource('Prometheus metric types', 'https://prometheus.io/docs/concepts/metric_types/', 'Counters, gauges, histograms'),
      resource('OpenAI function calling guide', 'https://developers.openai.com/api/docs/guides/function-calling', 'Expose only useful investigation tools')
    ],
    assignment: 'Generate time-series simulator conditions and build an investigator with query_metrics, search_logs, find_incidents, list_failed_payments, get_provider_status, and search_runbooks. Answer why USDC withdrawal success rate dropped in the last 30 minutes.',
    failure: 'Evaluate both final diagnosis and trajectory: relevant evidence inspected, unnecessary calls, premature stopping, root-cause confidence, and unsupported claims.',
    deliverables: ['simulator/scenarios/', 'app/agents/investigator.py', 'evals/agent/scenarios.jsonl'],
    exit: ['At least 30 incident scenarios exist', '≥80% correct root cause', '≥90% no unsupported root-cause claims', 'Zero infinite loops', 'Average tool calls are tracked', 'Tokens, cost, and latency per investigation are tracked']
  },
  {
    id: 11, month: 3, title: 'LangGraph & durable workflows', goal: 'Learn the framework after understanding the primitive it abstracts: stateful, long-running, resumable workflows.',
    resources: [
      resource('LangGraph overview', 'https://docs.langchain.com/oss/python/langgraph/overview', 'Graph state and durable execution'),
      resource('LangGraph persistence', 'https://docs.langchain.com/oss/python/langgraph/persistence', 'Checkpoints and resumability'),
      resource('LangGraph interrupts', 'https://docs.langchain.com/oss/python/langgraph/interrupts', 'Human-in-the-loop pause and resume')
    ],
    assignment: 'Refactor the investigator into a graph: understand_request → gather_payment_state → gather_operational_state → retrieve_knowledge → analyze → confidence_gate → answer or human_review. Add a proposed create_incident action.',
    failure: 'Kill the process halfway through an investigation, restart it, and resume from checkpoint. Attempt to replay a side effect and prove it is not duplicated.',
    deliverables: ['app/agents/graph.py', 'app/agents/checkpoints.py', 'evals/agent/recovery.jsonl', 'docs/decisions/langgraph.md'],
    exit: ['Workflow survives a process restart', 'State is persisted', 'Duplicate side effects are prevented', 'Approval pauses and resumes correctly', 'You can explain the value over the Week 9 loop', 'Recovery behavior is covered by an eval']
  },
  {
    id: 12, month: 3, title: 'MCP + Go', goal: 'Turn payment-domain capabilities into reusable AI infrastructure and connect your Go learning to a real boundary.',
    resources: [
      resource('MCP architecture overview', 'https://modelcontextprotocol.io/docs/learn/architecture', 'Hosts, clients, servers, and transports'),
      resource('MCP tools specification', 'https://modelcontextprotocol.io/specification/2025-06-18/server/tools', 'Discoverable, callable tools'),
      resource('MCP resources specification', 'https://modelcontextprotocol.io/specification/2025-06-18/server/resources', 'Read-only payment and incident resources')
    ],
    assignment: 'Build a small Paqet MCP server in Go. Expose payment://{id}, incident://{id}, and tools for get_payment, get_payment_events, search_incidents, and get_provider_status. Use simulator adapters until Paqet is ready.',
    failure: 'Test malformed requests, unknown IDs, authorization boundaries, tool timeouts, and a destructive action that requires explicit human approval.',
    deliverables: ['mcp/paqet-mcp/', 'mcp/paqet-mcp/server.go', 'mcp/paqet-mcp/README.md', 'evals/mcp/contract.jsonl'],
    exit: ['Server exposes resources and tools', 'Go tests cover request validation', 'Client receives stable errors', 'Simulator and Paqet adapters share a conceptual interface', 'Destructive operations require approval', 'MCP contract tests pass from a clean run']
  },
  {
    id: 13, month: 4, title: 'Serious evals', goal: 'Expand from a demo-sized golden set to an evaluation system that measures the whole agent environment.',
    resources: [
      resource('OpenAI Evals guide', 'https://developers.openai.com/api/docs/guides/evals', 'Deterministic graders and datasets'),
      resource('OpenAI evals best practices', 'https://platform.openai.com/docs/guides/evals', 'Human review and LLM-as-judge'),
      resource('OpenAI model evaluation guide', 'https://platform.openai.com/docs/guides/evals', 'Pairwise comparison + regression gates')
    ],
    assignment: 'Expand to 300–500 cases across payment investigation, retrieval, tool selection, insufficient information, ambiguous requests, outages, permission boundaries, prompt injection, and hallucination.',
    failure: 'Compare deterministic assertions, human scoring, LLM-as-judge, and pairwise comparison. Sample cases manually and document judge disagreement.',
    deliverables: ['evals/datasets/v1/', 'evals/graders/', 'evals/reports/week13.md', 'docs/evaluation-strategy.md'],
    exit: ['300+ cases are versioned', 'Coverage includes safety and permissions', 'At least two grading methods are compared', 'Manual samples are reviewed', 'Regression thresholds are defined', 'A model/prompt change can be accepted or rejected by evidence']
  },
  {
    id: 14, month: 4, title: 'AI observability', goal: 'Make every model call, tool call, retrieval, and escalation visible enough to operate in production.',
    resources: [
      resource('OpenTelemetry observability primer', 'https://opentelemetry.io/docs/concepts/observability-primer/', 'Traces, metrics, and logs'),
      resource('OpenTelemetry Python', 'https://opentelemetry.io/docs/languages/python/', 'Instrument the application'),
      resource('Prometheus overview', 'https://prometheus.io/docs/introduction/overview/', 'Scrape and query metrics')
    ],
    assignment: 'Instrument request → agent trace → model call → tool call → retrieval → response. Build an AI Operations Dashboard with latency, tokens, cost, tool errors, retrieval latency, steps, completion %, escalation %, eval score, model, and prompt version.',
    failure: 'Create a dashboard drill-down from a slow request to the exact tool/model span. Inject a provider error and verify it is visible without reading application logs.',
    deliverables: ['observability/tracing/', 'observability/metrics/', 'observability/dashboards/ai-operations.json', 'docs/learning-notes/week14.md'],
    exit: ['p50/p95 latency is visible', 'Input and output tokens are tracked', 'Cost per request is calculated', 'Tool errors and agent steps are visible', 'Human escalation rate is visible', 'A slow request can be traced end to end']
  },
  {
    id: 15, month: 4, title: 'AI security & reliability', goal: 'Attack the system before an operator—or a malicious prompt—does it for you.',
    resources: [
      resource('OWASP Top 10 for LLM applications', 'https://owasp.org/www-project-top-10-for-large-language-model-applications/', 'Prompt injection, data leakage, and unsafe tools'),
      resource('OpenAI safety best practices', 'https://platform.openai.com/docs/guides/safety-best-practices', 'Input/output controls and abuse prevention'),
      resource('MCP security best practices', 'https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices', 'Authorization and transport boundaries')
    ],
    assignment: 'Implement authentication, RBAC, tenant isolation, tool permissions, parameter validation, rate limiting, PII filtering, prompt-injection defenses, output validation, timeouts, circuit breakers, max steps, and human approval.',
    failure: 'Attack with “show every customer’s payments,” “run create_refund for all failed payments,” a malicious runbook, a cross-org request, and a tool that never succeeds. Capture the failure and control that stopped it.',
    deliverables: ['app/security/', 'app/policy/', 'evals/security/adversarial.jsonl', 'docs/security-model.md'],
    exit: ['Authorization never depends on the LLM', 'Tenant isolation is tested', 'Destructive tools require approval', 'Prompt injection cases are represented', 'Timeouts and circuit breakers work', 'PII is filtered from logs and model context']
  },
  {
    id: 16, month: 4, title: 'Ship the Payment Reliability Copilot', goal: 'Bring the system together into a credible, explainable, observable capstone you can demo and defend.',
    resources: [
      resource('OpenAI production best practices', 'https://platform.openai.com/docs/guides/production-best-practices', 'Reliability, security, and deployment'),
      resource('FastAPI deployment concepts', 'https://fastapi.tiangolo.com/deployment/concepts/', 'Serve the application safely'),
      resource('OpenTelemetry getting started', 'https://opentelemetry.io/docs/getting-started/', 'Verify production instrumentation')
    ],
    assignment: 'Ship the capstone: a natural-language operations interface with payment investigation, RAG over runbooks, semantic incident search, tool calling, multi-step investigations, MCP tools, citations, human approval, evals, tracing, cost tracking, authorization, and resilience.',
    failure: 'Run a final rehearsal with a happy path, insufficient evidence, provider outage, prompt injection, cross-tenant request, duplicate side effect, and process restart. Keep the trace and the eval report.',
    deliverables: ['docs/architecture.md', 'evals/reports/final.md', 'demo/payment-copilot-demo.mp4', 'docs/case-study.md'],
    exit: ['All core capabilities have a working path', 'Final eval report includes failures and trade-offs', 'Architecture document explains boundaries', 'A 2–4 minute demo is recorded', 'Case study explains why AI is appropriate', 'You can explain what changes at 100× scale']
  }
];

enrichCurriculum(weeks);
applyCurriculumUpdates(weeks);
const STORAGE_KEY = 'payment-reliability-copilot-progress-v1';
let storageProblem = false;
let state = loadState();
let toastTimer;

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return CourseProgress.validate(JSON.parse(raw));
  } catch (_) { storageProblem = true; }
  return CourseProgress.blank();
}

function saveState() {
  try {
    if (storageProblem) throw new Error('Storage needs recovery');
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    document.getElementById('save-status').textContent = 'Saved in this browser';
    return true;
  } catch (_) {
    document.getElementById('save-status').textContent = 'Not saved — export a backup';
    document.getElementById('storage-warning').hidden = false;
    return false;
  }
}
function currentWeek() { return weeks.find((week) => week.id === state.activeWeek) || weeks[0]; }
function key(week, kind, index) { return `${week.id}:${kind}:${index}`; }
function checked(week, kind, index) { return Boolean(state.checked[key(week, kind, index)]); }
function setChecked(week, kind, index, value) { state.checked[key(week, kind, index)] = value; return saveState(); }
function weekStats(week) {
  return CourseProgress.stats(week, state);
}
function courseStats() {
  const totals = weeks.reduce((acc, week) => { const s = weekStats(week); acc.total += s.total; acc.done += s.done; if (s.done === s.total) acc.complete += 1; return acc; }, { total: 0, done: 0, complete: 0 });
  return { ...totals, percent: totals.total ? Math.round((totals.done / totals.total) * 1000) / 10 : 0 };
}
function monthStats(monthId) {
  const these = weeks.filter((week) => week.month === monthId);
  const total = these.reduce((n, week) => n + weekStats(week).total, 0);
  const done = these.reduce((n, week) => n + weekStats(week).done, 0);
  return { total, done, percent: total ? Math.round((done / total) * 100) : 0 };
}
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char])); }

function renderNav() {
  const nav = document.getElementById('week-nav');
  nav.innerHTML = months.map((month) => {
    const items = weeks.filter((week) => week.month === month.id).map((week) => {
      const status = weekStats(week);
      const stateClass = status.done === status.total ? 'done' : '';
      return `<button class="week-nav-item ${week.id === state.activeWeek ? 'active' : ''} ${stateClass}" type="button" data-week="${week.id}" ${week.id === state.activeWeek ? 'aria-current="step"' : ''} aria-label="Week ${week.id}: ${escapeHtml(week.title)}, ${status.done} of ${status.total} complete"><span class="week-nav-number">${String(week.id).padStart(2, '0')}</span><span class="week-nav-title">${escapeHtml(week.title)}</span><span class="week-nav-status" aria-hidden="true"></span></button>`;
    }).join('');
    return `<div class="month-nav-label">MONTH ${String(month.id).padStart(2, '0')} · ${month.short.toUpperCase()}</div>${items}`;
  }).join('');
  nav.querySelectorAll('[data-week]').forEach((button) => button.addEventListener('click', () => { state.activeWeek = Number(button.dataset.week); saveState(); render(); if (window.innerWidth <= 820) document.getElementById('sidebar').classList.remove('open'); }));
}

function renderMonthRail() {
  document.getElementById('month-list').innerHTML = months.map((month) => {
    const stats = monthStats(month.id);
    return `<button type="button" class="month-item ${currentWeek().month === month.id ? 'active' : ''}" data-month="${month.id}" aria-label="Month ${month.id}: ${month.label}, ${stats.percent}% complete"><span class="month-num">0${month.id}</span><span class="month-name">${month.label}</span><span class="month-weeks">${month.weeks}</span><span class="month-meter"><span style="width:${stats.percent}%"></span></span></button>`;
  }).join('');
  document.querySelectorAll('.month-item').forEach((item) => { item.addEventListener('click', () => { const first = weeks.find((week) => week.month === Number(item.dataset.month)); state.activeWeek = first.id; saveState(); render(); }); });
}

function renderChecklist(week, items, kind, targetId) {
  document.getElementById(targetId).innerHTML = items.map((item, index) => {
    const done = checked(week, kind, index);
    const label = kind === 'deliverable' ? `<code class="deliverable-path">${escapeHtml(item)}</code>` : escapeHtml(item);
    return `<label class="check-row ${done ? 'done' : ''}"><input class="check-input" type="checkbox" data-kind="${kind}" data-index="${index}" ${done ? 'checked' : ''} /><span>${label}</span></label>`;
  }).join('');
}

function renderWeek() {
  const week = currentWeek();
  const stats = weekStats(week);
  const month = months.find((item) => item.id === week.month);
  document.getElementById('topbar-week').textContent = `Week ${String(week.id).padStart(2, '0')}`;
  document.getElementById('month-kicker').textContent = `MONTH ${String(week.month).padStart(2, '0')} · ${month.label.toUpperCase()}`;
  document.getElementById('week-number').textContent = `WEEK ${String(week.id).padStart(2, '0')}`;
  document.getElementById('week-title').textContent = week.title;
  document.getElementById('week-goal').textContent = week.goal;
  document.getElementById('week-focus').textContent = week.extension ? week.extension.focus : '';
  document.getElementById('week-focus').hidden = !week.extension;
  document.getElementById('reading-outcomes').innerHTML = week.readingOutcomes.map(text => `<li>${escapeHtml(text)}</li>`).join('');
  document.getElementById('note-prompt').textContent = week.notePrompt;
  renderExtension(week);
  document.getElementById('study-prerequisite').textContent = week.study.prerequisite;
  document.getElementById('study-core').textContent = week.study.core;
  document.getElementById('study-stretch').textContent = week.study.stretch;
  document.getElementById('week-notes').value = state.notes[week.id] || '';
  document.getElementById('previous-week').disabled = week.id === 1;
  document.getElementById('following-week').disabled = week.id === 16;
  document.getElementById('context-month').textContent = `${String(week.month).padStart(2, '0')} / 04`;
  document.getElementById('week-progress-bar').style.width = `${stats.percent}%`;
  document.getElementById('week-progress-label').textContent = `${stats.done} / ${stats.total}`;
  const weekState = document.getElementById('week-state');
  weekState.className = `week-state ${stats.done === stats.total ? 'complete' : stats.done > 0 ? 'in-progress' : ''}`;
  weekState.textContent = stats.done === stats.total ? 'Complete' : stats.done > 0 ? 'In progress' : 'Not started';

  document.getElementById('resource-list').innerHTML = week.resources.map((item, index) => {
    const done = checked(week, 'resource', index);
    return `<div class="resource-row ${done ? 'is-done' : ''}"><input class="resource-check" type="checkbox" data-kind="resource" data-index="${index}" aria-label="Mark ${escapeHtml(item.title)} as read" ${done ? 'checked' : ''} /><div><a class="resource-title" href="${item.url}" target="_blank" rel="noreferrer">${escapeHtml(item.title)}</a><div class="resource-focus">${escapeHtml(item.level)} · Reading outcome: ${escapeHtml(item.focus)}</div></div><a class="resource-link" href="${item.url}" target="_blank" rel="noreferrer" aria-label="Open ${escapeHtml(item.title)}">Open ↗</a></div>`;
  }).join('');
  document.getElementById('assignment-heading').textContent = week.title;
  document.getElementById('assignment-copy').textContent = week.assignment;
  document.getElementById('failure-copy').textContent = week.failure;
  const assignmentDone = checked(week, 'assignment', 0);
  const assignmentButton = document.getElementById('assignment-toggle');
  assignmentButton.classList.toggle('done', assignmentDone);
  assignmentButton.setAttribute('aria-pressed', assignmentDone ? 'true' : 'false');
  document.getElementById('assignment-toggle-label').textContent = assignmentDone ? 'Assignment complete' : 'Mark assignment complete';
  renderChecklist(week, week.deliverables, 'deliverable', 'deliverables-list');
  renderChecklist(week, week.exit, 'exit', 'exit-list');
  bindCheckInputs();
  renderNext();
}

function renderExtension(week) {
  const extension = week.extension;
  document.getElementById('extension-build').hidden = !extension;
  document.getElementById('extension-experiments').hidden = !extension;
  document.getElementById('implementation-additions').innerHTML = (extension?.implementation || []).map(text => `<p>${escapeHtml(text)}</p>`).join('');
  document.getElementById('experiment-additions').innerHTML = (extension?.experiments || []).map(text => `<p>${escapeHtml(text)}</p>`).join('');
  document.getElementById('extension-metrics').hidden = !extension?.metrics;
  document.getElementById('metrics-list').textContent = extension?.metrics?.join(' · ') || '';
  document.getElementById('extension-example').hidden = !extension?.example;
  document.getElementById('example-copy').textContent = extension?.example || '';
}

function renderNext() {
  const next = CourseProgress.next(weeks, state);
  document.getElementById('next-up-copy').textContent = next ? `Week ${next.week} · ${next.label}` : 'All core checkpoints complete. Review your capstone or explore optional readings.';
  document.getElementById('next-button').textContent = next ? 'Continue learning →' : 'Review capstone →';
  document.getElementById('next-button').onclick = () => {
    state.activeWeek = next ? next.week : 16; saveState(); render();
    const target = !next ? document.getElementById('week-title') : next.kind === 'assignment' ? document.getElementById('assignment-toggle') : document.querySelector(`[data-kind="${next.kind}"][data-index="${next.index}"]`);
    if (!next) target.setAttribute('tabindex', '-1');
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    target.focus({ preventScroll: true });
  };
  document.getElementById('study-continue').textContent = next ? 'Continue learning →' : 'Review capstone →';
  document.getElementById('study-continue').onclick = document.getElementById('next-button').onclick;
}

function bindCheckInputs() {
  document.querySelectorAll('[data-kind][data-index]').forEach((input) => input.addEventListener('change', () => {
    const saved = setChecked(currentWeek(), input.dataset.kind, Number(input.dataset.index), input.checked);
    const selector = `[data-kind="${input.dataset.kind}"][data-index="${input.dataset.index}"]`;
    render(); document.querySelector(selector).focus({ preventScroll: true });
    showToast(saved ? (input.checked ? 'Checkpoint saved' : 'Checkpoint reopened') : 'Not saved — export a backup');
  }));
  document.getElementById('assignment-toggle').onclick = () => { const week = currentWeek(); const next = !checked(week, 'assignment', 0); const saved = setChecked(week, 'assignment', 0, next); render(); document.getElementById('assignment-toggle').focus({ preventScroll: true }); showToast(saved ? 'Assignment updated' : 'Not saved — export a backup'); };
}

function renderOverview() {
  const stats = courseStats();
  document.getElementById('overall-percent').textContent = `${stats.percent}%`;
  document.getElementById('progress-ring').style.setProperty('--pct', `${stats.percent}%`);
  document.getElementById('completed-count').textContent = stats.done;
  document.getElementById('total-count').textContent = stats.total;
  document.getElementById('weeks-complete').textContent = stats.complete;
  document.getElementById('hours-left').textContent = '8–10';
}

function render() { renderNav(); renderWeek(); renderMonthRail(); renderOverview(); }
function showToast(message) { const toast = document.getElementById('toast'); toast.textContent = message; toast.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 1800); }

document.getElementById('menu-toggle').addEventListener('click', () => document.getElementById('sidebar').classList.toggle('open'));
document.getElementById('focus-checklist').addEventListener('click', () => document.getElementById('checklist-panel').scrollIntoView({ behavior: 'smooth', block: 'center' }));
document.getElementById('reset-progress').addEventListener('click', () => { if (window.confirm('Clear all checklists and notes? Export a backup first if you want to restore them.')) { state = CourseProgress.blank(); const saved = saveState(); render(); showToast(saved ? 'Progress reset' : 'Reset only in memory — storage unavailable'); } });

document.getElementById('week-notes').addEventListener('input', event => { state.notes[state.activeWeek] = event.target.value; saveState(); });
for (const [id, delta] of [['previous-week', -1], ['following-week', 1]]) {
  document.getElementById(id).onclick = () => { state.activeWeek = Math.max(1, Math.min(16, state.activeWeek + delta)); saveState(); render(); document.getElementById('week-title').scrollIntoView({block: 'center'}); };
}
document.getElementById('export-progress').onclick = () => {
  const blob = new Blob([JSON.stringify({ app: 'payment-reliability-copilot', version: 1, exportedAt: new Date().toISOString(), ...state }, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob); const link = document.createElement('a');
  link.href = url; link.download = `copilot-progress-${new Date().toISOString().slice(0,10)}.json`;
  link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
document.getElementById('import-progress').onclick = () => document.getElementById('backup-file').click();
document.getElementById('backup-file').onchange = async event => {
  const file = event.target.files[0]; if (!file) return;
  try {
    if (file.size > 1000000) throw new Error('Backup is too large (maximum 1 MB).');
    const data = JSON.parse(await file.text());
    if (data.app !== 'payment-reliability-copilot' || data.version !== 1) throw new Error('Choose a supported course backup.');
    const imported = CourseProgress.validate(data);
    if (!window.confirm('Replace this browser’s progress and notes with this backup? Export your current progress first if needed.')) return;
    // Commit storage first: a failed import must not replace current in-memory progress.
    localStorage.setItem(STORAGE_KEY, JSON.stringify(imported));
    state = imported; storageProblem = false;
    document.getElementById('storage-warning').hidden = true;
    saveState(); render(); showToast('Backup restored');
  } catch (error) { showToast(`Import failed: ${error.message}`); }
  finally { event.target.value = ''; }
};

render();
if (storageProblem) { document.getElementById('save-status').textContent = 'Progress could not be loaded'; document.getElementById('storage-warning').hidden = false; }
