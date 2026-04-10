---
title: Project Approval OpenEnv
emoji: 🏢
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# Project Approval OpenEnv Environment

An OpenEnv environment where an AI agent learns to approve, reject, or request changes on project proposals.

## Action Space
- approve - Approve the project
- reject - Reject the project
- request_changes - Request changes before approval

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| project_id | int | Unique project identifier |
| title | string | Project title |
| budget | float | Project budget in USD |
| risk_level | string | low, medium, or high |
| status | string | Current status |
| completeness | float | 0.0 to 1.0 completion score |

## Baseline Scores
| Task | Decision | Reward |
|------|----------|--------|
| Easy | approve | 1.0 |
| Medium | request_changes | 1.0 |
| Hard | reject | 1.0 |
| Average | | 1.0 |

## Setup
pip install -r requirements.txt
python inference.py
