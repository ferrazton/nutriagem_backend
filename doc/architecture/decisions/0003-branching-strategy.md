# ADR 0001 - Branching Strategy

## Context

We need a predictable workflow for managing changes while maintaining stability in production.

## Decision

- Use `main` for production-ready code
- Use `dev` for active development
- Feature branches created from `dev`
- Hotfix branches created from `main`

## Workflow

1. Developers create feature branches from `dev`
2. PRs target `dev` branch
3. After testing, create PR from `dev` to `main`
4. Main branch is always deployable

## Consequences

- Clear separation between stable and development code
- Requires discipline in merging to main
- Additional step for production releases
