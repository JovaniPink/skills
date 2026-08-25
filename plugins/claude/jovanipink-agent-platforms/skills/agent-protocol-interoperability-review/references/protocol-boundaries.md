# Protocol Boundaries

Record each protocol hop separately.

| Boundary | Questions |
| --- | --- |
| Version | Which specification and implementation versions are in use? |
| Discovery | Who publishes capabilities, and how is the record authenticated and refreshed? |
| Identity | Which user, service, agent, and tenant identities cross the boundary? |
| Authority | What is delegated, for how long, and how is scope enforced? |
| Schema | How are inputs, outputs, extensions, and content types validated? |
| Lifecycle | How are tasks, requests, streams, artifacts, cancellation, and completion represented? |
| Failure | What happens on timeout, retry, duplication, partial delivery, or version mismatch? |
| Security | Can untrusted content influence tools, URLs, credentials, rendering, or another agent? |
| Revocation | How are credentials, capabilities, tasks, and compromised endpoints disabled? |

## Primary resources

- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest)
- [Google ADK A2A documentation](https://adk-labs.github.io/adk-docs/a2a/)

Protocol support is not interoperability proof. Record the exact implementation pair and the tests that were observed.
