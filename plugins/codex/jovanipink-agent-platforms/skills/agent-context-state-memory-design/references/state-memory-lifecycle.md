# State and Memory Lifecycle

Use one row per material information class.

| Field | Question |
| --- | --- |
| Class | Is this instruction, request context, event history, scoped state, memory, retrieval, tool output, or artifact? |
| Subject | Which user, tenant, case, agent, or system does it concern? |
| Authority | What store or decision owner can establish or change it? |
| Provenance | Where did it come from, and can that origin be verified? |
| Writer | Which authenticated principal may create or update it? |
| Reader | Which principal may observe it, and for what purpose? |
| Time | When was it effective, observed, recorded, and last checked? |
| Retention | How long does it remain, and what rule governs deletion? |
| Conflict | What happens when sources disagree? |
| Revocation | How is it made ineligible and removed from future context? |
| Isolation | Which request, session, user, tenant, and evaluation boundaries apply? |

## Primary resources

- [Google ADK sessions and state](https://adk-labs.github.io/adk-docs/sessions/)
- [Google ADK memory](https://adk-labs.github.io/adk-docs/sessions/memory/)
- [NIST concept paper on software agent identity and authority](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)

Treat framework namespaces as mechanisms. Product authority and privacy requirements must still be defined by the owning application.
