class ApiException implements Exception {
  const ApiException({required this.code, required this.message, this.details});

  final String code;
  final String message;
  final Map<String, dynamic>? details;

  @override
  String toString() => 'ApiException($code): $message';
}
