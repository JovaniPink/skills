# Retrieval Evidence Matrix

Assess retrieval and claim support as separate stages.

| Stage | Questions |
| --- | --- |
| Source | Is the source authorized, licensed, current, versioned, and eligible for this user and purpose? |
| Ingestion | Were content, metadata, authority, time, access control, and deletion status preserved? |
| Query | Does the case represent a real need, boundary, conflict, no-answer state, or attack? |
| Retrieval | Were relevant sources found, ranked, filtered, and returned within limits? |
| Claim | Is each material claim directly or partially supported, contradicted, or unsupported? |
| Citation | Does the cited source support the nearby claim with correct date, unit, and context? |
| Safety | Can document text, metadata, or a tool result change instructions, cross a tenant boundary, or trigger a tool? |
| Recovery | Can the system abstain, ask, disclose conflict, correct a result, and revoke bad content? |

## Primary resources

- [OWASP vector and embedding weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [Google ADK safety and security](https://adk-labs.github.io/adk-docs/safety/)
- [NIST AI Resource Center](https://airc.nist.gov/)

A retrieved passage and a visible citation are evidence inputs. They are not proof that every generated claim is supported.
