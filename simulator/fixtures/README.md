# Week 2 tool fixtures

`week2_tools.json` contains synthetic evidence only. Version 1 stores records
keyed by `(organization_id, payment_id)`, with separate `payment`, `events`,
`ledger_entries` and `provider_status` responses. Fixtures execute no actions.

Org A and Org B intentionally share `pay-shared`, with amounts 1100 and 9900.
`pay-b-only` exists exclusively in Org B. Tests mutate temporary fixture copies
to exercise malformed payloads, empty responses and identity mismatches.

The reader must scope the record lookup before selecting or validating evidence.
Cross-tenant IDs and nonexistent IDs raise `ToolReadError` carrying the same `PAYMENT_NOT_FOUND` error.
Empty event/ledger lists are valid evidence; null payment/provider responses
raise `ToolReadError` carrying `EMPTY_RESPONSE`. Invalid shapes or inconsistent embedded identifiers
raise `ToolReadError` carrying `MALFORMED_RESPONSE`. Provider IDs other than `simulator` raise
`ToolReadError` carrying `INVALID_PROVIDER` for an existing scoped payment.

These Phase 2 errors are nonretryable and use fixed safe messages. Timeouts,
transient server errors, backoff and replay belong to the recovery phase.

The reader returns evidence on success and raises `ToolReadError(error)` for
expected failures. The gateway catches only that exception around the reader
call and preserves its `ToolError` in a failed result/trace. Unexpected defects
propagate. File-loading failures still surface at reader construction.
