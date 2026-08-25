# Tool Action Matrix

Create one row per registered tool and distinguish host policy from model-visible instructions.

| Field | Required evidence |
| --- | --- |
| Tool | Registered name, version, owner, and implementation |
| Caller | Agent identity and authenticated product principal |
| Arguments | Schema, validation, allowlists, ownership checks, and limits |
| Data | Input and output classifications and tenant boundary |
| Network | Allowed destination, redirect policy, DNS and address controls |
| Effect | Read, compute, draft, external write, destructive, financial, publication, deployment, or trust decision |
| Approval | Approver, exact bound arguments, expiration, and durable record |
| Replay | Idempotency key, duplicate handling, retry, and cancellation |
| Recovery | Rollback, compensation, partial failure, and emergency stop |
| Evidence | Request, decision, execution, and readback audit records |

## Primary resources

- [Google ADK safety and security](https://adk-labs.github.io/adk-docs/safety/)
- [Google ADK tool confirmation](https://adk-labs.github.io/adk-docs/tools-custom/confirmation/)
- [NIST concept paper on software agent identity and authority](https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents)

Experimental in-process confirmation can demonstrate interaction behavior, but it is not durable, replay-safe authorization for a production external write.
