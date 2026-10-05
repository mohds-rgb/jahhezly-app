import 'dart:async';

import 'package:http/http.dart' as http;

import '../../core/network/api_client.dart';
import '../../core/network/api_exception.dart';
import '../local/local_database.dart';

class OrderSubmissionResult {
  const OrderSubmissionResult({required this.queued, required this.payload});
  final bool queued;
  final Map<String, dynamic>? payload;
}

class OrderRepository {
  OrderRepository({required this.api, required this.local});
  final ApiClient api;
  final LocalDatabase local;

  Future<OrderSubmissionResult> submit({required String storeId, required List<Map<String, dynamic>> items, String? note, String? customerPhone}) async {
    final now = DateTime.now().toUtc();
    final idem = 'mobile-${now.microsecondsSinceEpoch}-${now.millisecondsSinceEpoch % 100000}';
    final payload = {'storeId': storeId, 'items': items, if (note != null) 'note': note, if (customerPhone != null) 'customerPhone': customerPhone};
    try {
      final response = await api.submitOrder(storeId: storeId, items: items, idempotencyKey: idem, note: note, customerPhone: customerPhone);
      return OrderSubmissionResult(queued: false, payload: response);
    } on ApiException {
      rethrow;
    } on http.ClientException {
      await local.enqueueSubmission(payload: payload, idempotencyKey: idem);
      return const OrderSubmissionResult(queued: true, payload: null);
    } on TimeoutException {
      await local.enqueueSubmission(payload: payload, idempotencyKey: idem);
      return const OrderSubmissionResult(queued: true, payload: null);
    }
  }

  }

  Future<Map<String, dynamic>> getOrder(String orderId) => api.getOrder(orderId);
}
