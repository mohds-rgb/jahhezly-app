import 'dart:convert';

import '../../core/network/api_client.dart';
import '../../core/network/api_exception.dart';
import 'local_database.dart';

class SyncQueueProcessor {
  const SyncQueueProcessor({required this.local, required this.api});
  final LocalDatabase local;
  final ApiClient api;

  Future<void> drain() async {
    final operations = await local.getPendingSyncOperations();
    for (final operation in operations) {
      final id = operation['id']! as int;
      final payload = jsonDecode(operation['payload_json']! as String) as Map<String, dynamic>;
      final storeId = payload['storeId'] as String;
      final items = (payload['items'] as List).map((item) => Map<String, dynamic>.from(item as Map)).toList();
      final idempotencyKey = operation['idempotency_key']! as String;
      try {
        await api.submitOrder(storeId: storeId, items: items, idempotencyKey: idempotencyKey, note: payload['note'] as String?, customerPhone: payload['customerPhone'] as String?);
        await local.markSyncCompleted(id);
      } on ApiException catch (error) {
        if (_isRetryable(error.code)) {
          await local.markSyncRetry(id, code: error.code, message: error.message);
        } else {
          await local.markSyncConflict(id, code: error.code, message: error.message);
        }
      } catch (_) {
        await local.markSyncRetry(id, code: 'NETWORK_ERROR', message: 'Network unavailable.');
      }
    }
  }

  bool _isRetryable(String code) => const {
        'SERVICE_UNAVAILABLE',
        'INTEGRATION_UNAVAILABLE',
        'RATE_LIMITED',
      }.contains(code);
}
