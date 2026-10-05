import 'dart:async';

import 'package:http/http.dart' as http;

import '../../core/network/api_client.dart';
import '../../core/network/api_exception.dart';
import '../../domain/models/catalog_item.dart';
import '../local/local_database.dart';

class CatalogSnapshot {
  const CatalogSnapshot({required this.items, required this.fromCache});
  final List<CatalogItem> items;
  final bool fromCache;
}

class CatalogRepository {
  const CatalogRepository({required this.api, required this.local});
  final ApiClient api;
  final LocalDatabase local;

  Future<CatalogSnapshot> load(String storeId) async {
    try {
      final raw = await api.getCatalog(storeId);
      final items = raw.map(CatalogItem.fromJson).toList();
      await local.replaceCatalog(storeId: storeId, items: items);
      return CatalogSnapshot(items: items, fromCache: false);
    } on ApiException catch (error) {
      if (error.code != 'SERVICE_UNAVAILABLE') rethrow;
      final items = await local.getCatalog(storeId);
      return CatalogSnapshot(items: items, fromCache: true);
    } on http.ClientException {
      final items = await local.getCatalog(storeId);
      return CatalogSnapshot(items: items, fromCache: true);
    } on TimeoutException {
      final items = await local.getCatalog(storeId);
      return CatalogSnapshot(items: items, fromCache: true);
    }
  }
}
