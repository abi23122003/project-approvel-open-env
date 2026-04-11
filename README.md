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

An OpenEnv environment where an AI agent learns to approve, reject, or request changes on project proposals based on budget, risk level, and completeness.

## Environment Description

This environment simulates a real-world project approval workflow. An AI agent acts as a project manager who must evaluate incoming project proposals and make decisions: approve, reject, or request changes. The agent is rewarded based on whether its decision matches the correct decision for each project.

## Action Space

| Action | Description |
|--------|-------------|
| approve | Approve the project for execution |
| reject | Reject the project outright |
| request_changes | Send back for revision before approval |

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| project_id | int | Unique project identifier |
| title | string | Project title |
| budget | int | Project budget in USD |
| risk_level | string | low, medium, or high |
| status | string | Current project status |
| completeness | float | 0.0 to 1.0 completion score |

## Tasks

| Task | Project | Correct Decision | Difficulty |
|------|---------|-----------------|------------|
| Easy | Community Library Renovation ($50,000, low risk, 90% complete) | approve | Easy |
| Medium | City Park Smart Lighting System ($120,000, medium risk, 60% complete) | request_changes | Medium |
| Hard | Nuclear Waste Processing Plant ($9,500,000, high risk, 30% complete) | reject | Hard |

## Reward Function

| Decision | Correct Match | Partial Credit | Wrong |
|----------|--------------|----------------|-------|
| Easy | 0.85 | 0.45 | 0.15 |
| Medium | 0.75 | 0.50 | 0.25 |
| Hard | 0.80 | 0.55 | 0.30 |

Scores are always strictly between 0.0 and 1.0.

## Baseline Scores

| Task | Decision | Reward |
|------|----------|--------|
| Easy | approve | 0.850 |
| Medium | request_changes | 0.250 |
| Hard | reject | 0.300 |
| Average | | 0.467 |

## Setup & Usage

```bash
pip install -r requirements.txt
python inference.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | UI Dashboard |
| /reset | POST | Start new episode |
| /step | POST | Take an action |
| /state | GET | Get current state |
| /health | GET | Health check |
