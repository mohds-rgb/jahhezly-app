enum LocalOrderState { queuedForSubmission, submitted, accepted, preparing, readyForPickup, collected, rejected, cancelled }

class LocalOrder {
  const LocalOrder({required this.id, required this.state, this.publicCode});

  final String id;
  final LocalOrderState state;
  final String? publicCode;
}
