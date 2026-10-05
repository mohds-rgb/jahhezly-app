class AppConfig {
  const AppConfig({required this.apiBaseUrl, this.defaultStoreId});

  final String apiBaseUrl;
  final String? defaultStoreId;

  static const fromEnvironment = AppConfig(
    apiBaseUrl: String.fromEnvironment(
      'JAHHEZLY_API_BASE_URL',
      defaultValue: 'http://10.0.2.2:8000',
    ),
  );
}
