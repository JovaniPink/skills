# Protocol Boundaries

Record each protocol hop separately.

| Boundary | Questions |
| --- | --- |
| Version | Which specification and implementation versions are in use? |
| Normative source | Which versioned schema is authoritative, and which rendered or generated artifacts are only projections? |
| Discovery | Who publishes capabilities, how is the record signed or authenticated, and how are caches refreshed or revoked? |
| Binding | Do each advertised transport and protocol binding preserve operations, results, errors, and authentication? |
| Identity | Which user, service, agent, and tenant identities cross the boundary? |
| Authority | What is delegated, for how long, and how is scope enforced? Does an authorization-required state remain only a request until an external decision grants a defined scope? |
| Schema | How are inputs, outputs, extensions, and content types validated? |
| Lifecycle | How are tasks, requests, streams, artifacts, cancellation, and completion represented? |
| Failure | What happens on timeout, retry, duplication, partial delivery, or version mismatch? |
| Security | Can untrusted content influence tools, URLs, credentials, rendering, or another agent? |
| Revocation | How are credentials, capabilities, tasks, and compromised endpoints disabled? |

## Primary resources

- [A2A Protocol specification 1.0.0](https://a2a-protocol.org/v1.0.0/specification/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest)
- [Google ADK A2A documentation](https://adk-labs.github.io/adk-docs/a2a/)

Protocol support is not interoperability proof. Record the exact implementation pair and the tests that were observed.
