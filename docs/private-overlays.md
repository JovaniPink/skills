# Private Repo-Local Overlays

Private facts stay with the repository that owns their authority. The portable public catalog supplies reusable workflows; a private overlay supplies only the product-specific authority, topology, schema, identity, or operational contract needed by that repository.

```text
.agent-skills/skills/       # Canonical private repo-local source
.agents/skills/             # Generated Codex projection
.claude/skills/             # Generated Claude projection
```

The canonical private source is authoritative. The two client directories are projections and must be regenerated rather than hand-edited. A repository may keep these paths private even when its application code is public.

## Fictional example

Assume a fictional warehouse service named Northwind Relay. Its public workflow can use `authority-boundary-review` to ask which system owns an order and which systems are projections. Its private overlay may identify `Order Ledger A` as the current authority, name an internal reconciliation report, and state who may ratify a writer change. Those private names and contracts remain in Northwind Relay's repository; the public skill contains none of them.

## Placement test

- Public core: reusable across independent contexts, independently sourceable, safe to expose, and testable without private facts.
- Private overlay: correct execution depends on a private authority, identity, topology, contract, dataset, customer, or product.
- Neither: proprietary, unsafe, obsolete, duplicative, unsupported, or without demonstrated use.

An overlay may narrow or supply private context, but it must not weaken the public workflow's safety boundaries or silently grant tool permissions. Publication, deployment, migration, deletion, and authority ratification remain separately authorized actions.
