import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_exception.dart';

class ApiClient {
  ApiClient({required this.baseUrl, http.Client? client, this.guestSession})
      : _client = client ?? http.Client();

  final String baseUrl;
  String? guestSession;
  final http.Client _client;

  Future<List<Map<String, dynamic>>> getCatalog(String storeId) async {
    final response = await _client.get(_uri('/v1/stores/$storeId/catalog'), headers: _headers());
    return _decodeList(response);
  }

  Future<List<Map<String, dynamic>>> getStores() async {
    final response = await _client.get(_uri('/v1/stores'), headers: _headers());
    return _decodeList(response);
  }

  Future<Map<String, dynamic>> getOrder(String orderId) async {
    final response = await _client.get(_uri('/v1/orders/$orderId'), headers: _headers());
    return _decodeObject(response);
  }

  Future<Map<String, dynamic>> submitOrder({
    required String storeId,
    required List<Map<String, dynamic>> items,
    required String idempotencyKey,
    String? note,
    String? customerPhone,
  }) async {
    final response = await _client.post(
      _uri('/v1/orders'),
      headers: {..._headers(), 'X-Idempotency-Key': idempotencyKey},
      body: jsonEncode({'storeId': storeId, 'items': items, if (note != null) 'note': note, if (customerPhone != null) 'customerPhone': customerPhone}),
    );
    return _decodeObject(response);
  }

  Map<String, String> _headers() => {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        if (guestSession != null) 'X-Guest-Session': guestSession!,
      };

  Uri _uri(String path) {
    final base = baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl;
    return Uri.parse('$base$path');
  }

  List<Map<String, dynamic>> _decodeList(http.Response response) {
    _throwIfFailed(response);
    final decoded = jsonDecode(response.body);
    return (decoded as List).map((item) => Map<String, dynamic>.from(item as Map)).toList();
  }

  Map<String, dynamic> _decodeObject(http.Response response) {
    _throwIfFailed(response);
    return Map<String, dynamic>.from(jsonDecode(response.body) as Map);
  }

  void _throwIfFailed(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) return;
    try {
      final body = jsonDecode(response.body) as Map<String, dynamic>;
      throw ApiException(
        code: '${body['code'] ?? 'HTTP_ERROR'}',
        message: '${body['message'] ?? 'Request failed.'}',
        details: body['details'] is Map<String, dynamic>
            ? body['details'] as Map<String, dynamic>
            : null,
      );
    } catch (error) {
      if (error is ApiException) rethrow;
      throw ApiException(code: 'HTTP_${response.statusCode}', message: 'Request failed.');
    }
  }
}
