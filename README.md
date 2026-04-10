# Project Approval OpenEnv Environment

## Description
An OpenEnv environment where an AI agent learns to approve, reject, or request changes on project proposals. The agent evaluates real-world project attributes like budget, risk level, and completeness to make decisions.

## Real-World Motivation
Project approval workflows are common in organizations. This environment trains agents to make consistent, fair decisions based on project attributes.

## Action Space
The agent can take one of 3 actions:
- `approve` - Approve the project
- `reject` - Reject the project
- `request_changes` - Request changes before approval

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| project_id | int | Unique project identifier |
| title | string | Project title |
| budget | float | Project budget in USD |
| risk_level | string | low, medium, or high |
| status | string | Current status |
| completeness | float | 0.0 to 1.0 completion score |

## Tasks
| Task | Difficulty | Description |
|------|-----------|-------------|
| Basic Website | Easy | Low budget, low risk, high completeness |
| Mobile App | Medium | Medium budget, medium risk, moderate completeness |
| AI System | Hard | High budget, high risk, high completeness |

## Reward Function
- `approve` correct → 1.0
- `request_changes` correct → 1.0
- `reject` correct → 1.0
- Wrong decision → 0.5

## Baseline Scores
| Task | Decision | Reward |
|------|----------|--------|
| Easy | approve | 1.0 |
| Medium | request_changes | 1.0 |
| Hard | reject | 1.0 |
| **Average** | | **1.0** |

## Setup Instructions

### Local Setup
```bash
git clone https://github.com/abi23122003/project-approvel-open-env.git
cd project-approvel-open-env
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file:
