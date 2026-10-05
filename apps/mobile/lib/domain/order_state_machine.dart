enum OrderState { draft, pendingSubmission, submitted, accepted, preparing, readyForPickup, collected, rejected, cancelled }

bool canTransition(OrderState from, OrderState to) {
  const allowed = <OrderState, Set<OrderState>>{
    OrderState.submitted: {OrderState.accepted, OrderState.rejected, OrderState.cancelled},
    OrderState.accepted: {OrderState.preparing, OrderState.cancelled},
    OrderState.preparing: {OrderState.readyForPickup, OrderState.cancelled},
    OrderState.readyForPickup: {OrderState.collected, OrderState.cancelled},
  };
  return allowed[from]?.contains(to) ?? false;
}
