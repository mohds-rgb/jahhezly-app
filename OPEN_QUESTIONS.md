# Owner Decisions

This file records owner-provided decisions and the remaining decisions that are safe to treat as engineering defaults. Business-sensitive choices are never silently upgraded into facts.

| ID | Decision | Status | Resolution |
|---|---|---|---|
| OQ-01 | Target country/market | DECIDED | Syria; intended for stores across Syrian regions |
| OQ-02 | Currency and regional conventions | DECIDED | Syrian Pound (SYP); Arabic + English presentation |
| OQ-03 | Initial merchants | DECIDED | Paris Market; cham-center |
| OQ-04 | Branch structure | DECIDED | Paris Market: 1 branch; cham-center: 4 branches |
| OQ-05 | Customer authentication | DECIDED | Browse as guest; optional customer identity |
| OQ-06 | Staff authentication | DECIDED | Email + password + JWT |
| OQ-07 | WhatsApp mode | DECIDED | V1 user-controlled click-to-chat/share; programmable integration remains future |
| OQ-08 | Guest orders | DECIDED | Allowed |
| OQ-09 | Price changes at submission | DECIDED | Reject stale price; show current price; customer explicitly confirms again |
| OQ-10 | Substitutions | ENGINEERING DEFAULT | Not supported in V1; unavailable items produce an explicit conflict |
| OQ-11 | Order expiration | ENGINEERING DEFAULT | 24 hours after `READY_FOR_PICKUP` in the demo policy; production policy requires owner/business review |
| OQ-12 | Pickup verification | ENGINEERING DEFAULT | Store-authorized staff action using order code; no public store phone data in repository |
| OQ-13 | Customer phone storage | DECIDED | Yes, limited to order/contact needs |
| OQ-14 | Notifications | DECIDED | In-app status notifications + local notification architecture; push provider integration is future |
| OQ-15 | Data retention | ENGINEERING DEFAULT | 12 months for portfolio design; production retention remains legal/business review |
| OQ-16 | Hosting region | DECIDED | Middle East target region |
| OQ-17 | Tax/invoice | DECIDED | No tax calculation in V1 |
| OQ-18 | Brand identity | DECIDED | Owner-designed icon; portfolio visual system derived from icon palette |
| OQ-19 | Target platforms | DECIDED | Android + iOS via Flutter |
| OQ-20 | Production launch/distribution | DECIDED | Public GitHub portfolio repository; no production launch claimed |

## Remaining evidence questions

| ID | Question | Status |
|---|---|---|
| EV-01 | Date of the reported real-world trial/usage | UNKNOWN — not supplied |
| EV-02 | Supporting screenshots/logs/reports for the reported figures | UNAVAILABLE — owner reports none |

## Owner-reported validation snapshot

The owner reports the following figures from prior Jahhezly use/testing:

- 1,338 people used Jahhezly
- 6 stores used Jahhezly
- 3 orders
- 2 trials/experiments
- Overall result: successful and accepted

No screenshots, logs, images, or reports were supplied. These figures are therefore **owner-reported and not independently verified in this repository**. They are documented for traceability and should not be presented as independently measured product metrics.
