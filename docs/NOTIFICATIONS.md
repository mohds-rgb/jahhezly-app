# Notifications

## V1 contract

Jahhezly treats order-state changes as notification-worthy events:

```text
SUBMITTED
ACCEPTED
PREPARING
READY_FOR_PICKUP
COLLECTED
```

The current client source provides an in-app status surface and a notification integration boundary. The backend remains the source of truth for order state.

## Push provider

No push provider credentials or provider-specific contracts are embedded in the repository. A future provider adapter may consume authoritative order events and deliver push notifications, but provider delivery is not claimed by this portfolio release.

## Privacy

Notification payloads must avoid unnecessary personal information. Order codes and high-level state changes are preferred over full order contents.
