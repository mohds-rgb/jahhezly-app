import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_exception.dart';

class MerchantApi {
  MerchantApi({required this.baseUrl, http.Client? client}) : _client = client ?? http.Client();

  final String baseUrl;
  final http.Client _client;
  String? accessToken;

  Future<void> login({required String email, required String password}) async {
    final response = await _client.post(
      _uri('/v1/auth/login'),
      headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    final body = _decodeObject(response);
    accessToken = '${body['accessToken']}';
  }

  Future<Map<String, dynamic>> me() async {
    final response = await _client.get(_uri('/v1/merchant/me'), headers: _headers());
    return _decodeObject(response);
  }

  Future<List<Map<String, dynamic>>> orders(String storeId) async {
    final response = await _client.get(_uri('/v1/merchant/orders?store_id=${Uri.encodeQueryComponent(storeId)}'), headers: _headers());
    return _decodeList(response);
  }

  Future<Map<String, dynamic>> order(String orderId) async {
    final response = await _client.get(_uri('/v1/merchant/orders/$orderId'), headers: _headers());
    return _decodeObject(response);
  }

  Future<Map<String, dynamic>> transition({required String orderId, required String action, required int version}) async {
    final response = await _client.post(
      _uri('/v1/merchant/orders/$orderId/$action'),
      headers: {..._headers(), 'If-Match': '$version'},
    );
    return _decodeObject(response);
  }

  List<Map<String, dynamic>> _decodeList(http.Response response) {
    _throwIfFailed(response);
    return (jsonDecode(response.body) as List).map((item) => Map<String, dynamic>.from(item as Map)).toList();
  }

  Map<String, dynamic> _decodeObject(http.Response response) {
    _throwIfFailed(response);
    return Map<String, dynamic>.from(jsonDecode(response.body) as Map);
  }

  Map<String, String> _headers() => {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  Uri _uri(String path) {
    final base = baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl;
    return Uri.parse('$base$path');
  }

  void _throwIfFailed(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) return;
    try {
      final body = jsonDecode(response.body) as Map<String, dynamic>;
      throw ApiException(code: '${body['code'] ?? 'HTTP_ERROR'}', message: '${body['message'] ?? 'Request failed.'}');
    } catch (error) {
      if (error is ApiException) rethrow;
      throw ApiException(code: 'HTTP_${response.statusCode}', message: 'Request failed.');
    }
  }
}
