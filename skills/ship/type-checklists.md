# Ship Type Checklists

Reference for `autoresearch:ship`. Each section defines the pre-ship checklist for one artifact type. The ship skill reads this file in Phase 1 to determine what to verify.

---

## 1. Library / Package

Target registries: PyPI, npm, crates.io, Maven Central, RubyGems, etc.

- [ ] `CHANGELOG.md` updated with this version's changes
- [ ] Version bumped consistently in all version-bearing files (`pyproject.toml` / `package.json` / `Cargo.toml` / `__init__.py`)
- [ ] `README.md` has install instructions and a working quickstart example
- [ ] All public functions/classes have docstrings or type annotations
- [ ] All tests pass (`pytest` / `npm test` / `cargo test`)
- [ ] No secrets or credentials in source code (API keys, tokens, passwords)
- [ ] License file present (`LICENSE` or `LICENSE.md`)
- [ ] `.gitignore` / `.npmignore` excludes build artifacts and dev configs from the published package
- [ ] Build artifact is clean (`python -m build` / `npm pack` produces expected output)
- [ ] Breaking changes documented in CHANGELOG with migration guide

---

## 2. CLI Tool

Target distribution: Homebrew, npm global, pip, shell script download, GitHub Releases binary.

- [ ] `--help` output is accurate and complete
- [ ] `--version` flag returns the current version
- [ ] All commands have been manually smoke-tested end-to-end
- [ ] `CHANGELOG.md` updated
- [ ] `README.md` includes install instructions for all supported platforms (macOS, Linux, Windows)
- [ ] Exit codes are consistent and documented (0 = success, non-zero = error)
- [ ] No hardcoded paths that only work on the developer's machine
- [ ] Binary builds (if any) compiled for all target architectures
- [ ] Shell completion scripts updated (bash, zsh, fish) if applicable
- [ ] All tests pass

---

## 3. REST API

Target deployment: cloud provider (AWS, GCP, Azure), PaaS (Railway, Render, Fly.io), self-hosted.

- [ ] All endpoints have request/response schemas documented (OpenAPI / Swagger)
- [ ] Authentication and authorization tested for all routes
- [ ] All tests pass (unit + integration)
- [ ] Environment variables documented in `.env.example` — no secrets hardcoded
- [ ] Rate limiting configured
- [ ] Health check endpoint (`/health` or equivalent) returns 200
- [ ] Database migrations are backward-compatible or migration plan documented
- [ ] Error responses return consistent JSON structure with meaningful messages
- [ ] CORS configuration reviewed and locked down to allowed origins
- [ ] API version is reflected in the base path or headers (e.g., `/v2/`)

---

## 4. Web App

Target deployment: Vercel, Netlify, AWS S3+CloudFront, GCP Cloud Run, self-hosted.

- [ ] All tests pass (unit + e2e)
- [ ] Production build completes without errors (`npm run build` / `vite build` / etc.)
- [ ] Environment variables for production are set in deploy target (not committed)
- [ ] No console errors on the main user flows (smoke-tested in browser)
- [ ] Performance: Lighthouse score ≥80 for Performance and Accessibility
- [ ] `robots.txt` and `sitemap.xml` present and correct
- [ ] CSP (Content Security Policy) headers configured
- [ ] 404 and error pages are custom and informative
- [ ] Analytics / error tracking configured (if applicable)
- [ ] All external links tested — no broken links on key pages

---

## 5. ML Model / Dataset

Target distribution: HuggingFace Hub, Kaggle, S3, model registry (MLflow, W&B).

- [ ] Model card / dataset card written (architecture, training data, intended use, limitations, evaluation results)
- [ ] Evaluation metrics documented on a held-out test set (not training data)
- [ ] License specified (model weights + training data licenses are compatible)
- [ ] Inference example provided and tested (model loads and produces expected output)
- [ ] Known failure modes and biases documented in the model card
- [ ] Model size and hardware requirements documented
- [ ] Training code and hyperparameters documented or versioned
- [ ] No PII in dataset or training artifacts
- [ ] Version / commit hash recorded in artifact metadata
- [ ] Reproducibility: random seeds and environment pinned in requirements file

---

## 6. Skill / Prompt

Target distribution: Claude plugin marketplace, skill registry, GitHub, .claude/commands/.

- [ ] Frontmatter complete: `name`, `description`, `TRIGGER`, `DO NOT TRIGGER`, `allowed-tools`
- [ ] Autonomy directive present if the skill runs in a loop
- [ ] All referenced files (e.g., `type-checklists.md`, `dimensions.md`) exist in the skill directory
- [ ] Skill tested end-to-end on at least 2 representative inputs
- [ ] Anti-patterns or guardrails documented (what the skill refuses to do)
- [ ] Output format specified (what files are written, what format)
- [ ] Edge cases table present covering ≥5 failure modes
- [ ] No hardcoded paths — all paths are relative to working directory
- [ ] `SKILL.md` passes a manual read for clarity (no ambiguous instructions)
- [ ] Added to parent `SKILL.md` command routing table (if part of a skill family)

---

## 7. Documentation Site

Target deployment: GitHub Pages, Netlify, Vercel, Read the Docs, Confluence.

- [ ] All pages render without broken links (`linkchecker` or equivalent)
- [ ] Search index is up to date
- [ ] Versioned docs reflect the current software version
- [ ] All code examples are tested and runnable
- [ ] Images have alt text (accessibility)
- [ ] Navigation structure reviewed — no orphan pages
- [ ] `404.html` is custom and helpful
- [ ] Build completes cleanly (`mkdocs build` / `docusaurus build` / `hugo` / etc.)
- [ ] Google Analytics or equivalent configured (if applicable)
- [ ] Redirects configured for any renamed/moved pages

---

## 8. Infrastructure (IaC)

Target deployment: AWS, GCP, Azure, Terraform Cloud, Pulumi Cloud, Kubernetes cluster.

- [ ] `terraform plan` / `cdk synth` / `pulumi preview` runs with zero errors
- [ ] Diff reviewed — no accidental resource deletions (`terraform show -json plan | jq '.resource_changes[] | select(.change.actions[] | contains("delete"))'`)
- [ ] All secrets injected via secret manager (not hardcoded in IaC files)
- [ ] State backend is remote and locked (not local `terraform.tfstate`)
- [ ] IAM permissions follow least-privilege principle
- [ ] All resources are tagged (environment, owner, cost-center)
- [ ] Rollback plan documented: what to do if deploy fails mid-way
- [ ] Changes tested in a non-production environment first
- [ ] Cost estimate reviewed (`infracost` or manual estimate)
- [ ] Blast radius documented: what services are affected by this change

---

## 9. Research Paper / Report

Target submission: arXiv, journal, conference, internal report, GitHub.

- [ ] Abstract accurately summarizes contributions (matches content of paper)
- [ ] All claims supported by citations or experimental results in the paper
- [ ] Reproducibility: code, data, and random seeds available (or explained why not)
- [ ] All figures have captions that can stand alone without reading the text
- [ ] Related work section covers key prior art (no obvious omissions)
- [ ] Limitations section is honest and complete
- [ ] Author list and affiliations verified
- [ ] Appendix / supplementary material referenced correctly from main text
- [ ] Spell-check and grammar check run on final draft
- [ ] arXiv / submission metadata (categories, abstract, title) reviewed before submission
