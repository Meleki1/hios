# HIOS Kernel Architecture

## Status

Accepted

---

# Purpose

The Kernel is the execution core of HIOS.

It is responsible for orchestrating intelligence capabilities while remaining completely independent of business domains and implementation details.

The Kernel does **not** know about:

- OpenAI
- Anthropic
- Gemini
- LangGraph
- FastAPI
- Telegram
- Databases
- Vector stores
- Pest control
- Home Intelligence

The Kernel only understands capabilities and execution.

---

# Philosophy

The Kernel is intentionally small.

Its responsibilities are limited to:

1. Discover capabilities
2. Resolve capabilities
3. Execute pipelines
4. Manage runtime context
5. Coordinate execution

Everything else belongs outside the Kernel.

---

# Core Components

```
PipelineRunner
        │
        ▼
Runtime
        │
        ▼
CapabilityRegistry
        │
        ▼
Capability
```

---

# Runtime

The Runtime is the service provider of HIOS.

Responsibilities:

- resolve registered capabilities
- expose runtime services
- remain stateless

The Runtime never:

- executes business logic
- decides execution order
- communicates with AI models
- knows about business domains

---

# Capability Registry

The Registry maps capability types to implementations.

Example:

```
UNDERSTANDING

↓

OpenAIUnderstandingCapability
```

Responsibilities:

- register implementations
- resolve implementations
- validate registrations

The Registry never executes capabilities.

---

# Pipeline

A Pipeline defines the execution order of capabilities.

Example:

```
Knowledge

↓

Understanding

↓

Decision

↓

Execution
```

Pipelines are declarative.

They contain no business logic.

---

# Pipeline Runner

The Pipeline Runner orchestrates execution.

Responsibilities:

- create RuntimeContext
- execute each pipeline step
- transform results into requests
- stop on unrecoverable failures
- return the final result

The Pipeline Runner does not implement capability logic.

---

# Runtime Context

RuntimeContext contains execution metadata shared across the pipeline.

Examples:

- execution_id
- correlation_id
- trace metadata

RuntimeContext never contains business state.

Business state belongs inside Requests.

---

# Capability

A Capability performs one well-defined responsibility.

Every capability implements the same contract.

```
Request

↓

Capability

↓

Result
```

Capabilities:

- receive exactly one request
- produce exactly one result

Capabilities never:

- invoke other capabilities
- orchestrate pipelines
- access the registry

---

# Mapper

A Mapper transforms one capability result into the next capability request.

Example:

```
KnowledgeResult

↓

KnowledgeToUnderstandingMapper

↓

UnderstandingRequest
```

Mappers contain no business decisions.

They only transform data.

---

# Execution Flow

```
Observation

↓

Knowledge Capability

↓

Knowledge Result

↓

Knowledge → Understanding Mapper

↓

Understanding Capability

↓

Understanding Result

↓

Understanding → Decision Mapper

↓

Decision Capability

↓

Decision Result

↓

Decision → Execution Mapper

↓

Execution Capability

↓

Execution Result
```

---

# Kernel Invariants

The following rules must never be violated.

## Runtime

Runtime never executes capabilities directly.

---

## Registry

Registry never contains business logic.

---

## Pipeline

Pipeline contains execution order only.

---

## Capability

Capabilities are isolated.

Capabilities never call other capabilities.

---

## Mapper

Mappers are pure transformations.

No side effects.

---

## Domain

The Kernel must never import domain-specific implementations.

---

# Dependency Rules

```
PipelineRunner

↓

Runtime

↓

Registry

↓

Capability
```

Allowed dependencies flow downward only.

Circular dependencies are forbidden.

---

# Extension Points

HIOS supports extension through:

- new capabilities
- new pipelines
- new mappers

The Kernel itself should rarely change.

---

# Engineering Principles

- Keep the Kernel small.
- Prefer composition over inheritance.
- Capabilities are replaceable.
- Pipelines are configurable.
- Business logic belongs outside the Kernel.
- The Runtime remains implementation-agnostic.

---

# Long-term Vision

The Kernel should be capable of orchestrating any intelligence workflow without modification.

Examples:

- HOME Intelligence
- Commercial Buildings
- Insurance Assessments
- Agriculture
- Healthcare
- Manufacturing

Only capabilities change.

The Kernel remains the same.