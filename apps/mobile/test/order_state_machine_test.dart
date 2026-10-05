import 'package:flutter_test/flutter_test.dart';
import 'package:jahhezly_mobile/domain/order_state_machine.dart';

void main() {
  test('accepts only valid preparation transitions', () {
    expect(canTransition(OrderState.submitted, OrderState.accepted), isTrue);
    expect(canTransition(OrderState.accepted, OrderState.preparing), isTrue);
    expect(canTransition(OrderState.preparing, OrderState.readyForPickup), isTrue);
    expect(canTransition(OrderState.readyForPickup, OrderState.collected), isTrue);
  });

  test('rejects terminal-state reactivation', () {
    expect(canTransition(OrderState.collected, OrderState.preparing), isFalse);
    expect(canTransition(OrderState.rejected, OrderState.accepted), isFalse);
  });
}
