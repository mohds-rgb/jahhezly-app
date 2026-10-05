import 'package:flutter/foundation.dart';

import '../data/repositories/catalog_repository.dart';
import '../domain/models/catalog_item.dart';

class CatalogController extends ChangeNotifier {
  CatalogController(this.repository);
  final CatalogRepository repository;

  List<CatalogItem> items = const [];
  bool loading = false;
  bool fromCache = false;
  Object? error;

  Future<void> load(String storeId) async {
    loading = true;
    error = null;
    notifyListeners();
    try {
      final snapshot = await repository.load(storeId);
      items = snapshot.items;
      fromCache = snapshot.fromCache;
    } catch (e) {
      error = e;
    } finally {
      loading = false;
      notifyListeners();
    }
  }
}
