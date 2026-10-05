import 'dart:convert';
import 'dart:math';

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

import '../../domain/models/catalog_item.dart';

class LocalDatabase {
  Database? _db;

  Future<Database> get database async => _db ??= await _open();

  Future<Database> _open() async {
    final path = join(await getDatabasesPath(), 'jahhezly.db');
    return openDatabase(path, version: 4, onCreate: (db, version) async {
      await db.execute('''CREATE TABLE catalog_items(
        id TEXT PRIMARY KEY, store_id TEXT NOT NULL, name TEXT NOT NULL, name_ar TEXT, category TEXT NOT NULL, category_ar TEXT,
        description TEXT NOT NULL, description_ar TEXT, unit_label TEXT NOT NULL,
        active INTEGER NOT NULL, available INTEGER NOT NULL, price_amount REAL NOT NULL,
        currency TEXT NOT NULL, last_synced_at TEXT NOT NULL)''');
      await db.execute('''CREATE TABLE cart_lines(
        product_id TEXT PRIMARY KEY, store_id TEXT NOT NULL, name TEXT NOT NULL, quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL)''');
      await db.execute('''CREATE TABLE sync_queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT, local_operation_id TEXT UNIQUE NOT NULL,
        idempotency_key TEXT UNIQUE NOT NULL, operation_type TEXT NOT NULL, payload_version INTEGER NOT NULL,
        payload_json TEXT NOT NULL, retry_count INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL,
        last_attempt_at TEXT, last_failure_code TEXT, last_error_message TEXT, created_at TEXT NOT NULL)''');
      await db.execute('''CREATE TABLE local_meta(
        key TEXT PRIMARY KEY, value TEXT NOT NULL)''');
      await db.insert('local_meta', {'key': 'schema_version', 'value': '3'});
    }, onUpgrade: (db, oldVersion, newVersion) async {
      if (oldVersion < 2) {
        await db.execute('ALTER TABLE sync_queue ADD COLUMN last_error_message TEXT');
        await db.insert(
          'local_meta',
          {'key': 'schema_version', 'value': '2'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
        await db.insert(
          'local_meta',
          {'key': 'last_migration', 'value': '1->2'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
      }
      if (oldVersion < 3) {
        await db.execute('ALTER TABLE catalog_items ADD COLUMN store_id TEXT');
        await db.execute('ALTER TABLE cart_lines ADD COLUMN store_id TEXT');
        await db.insert(
          'local_meta',
          {'key': 'schema_version', 'value': '3'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
        await db.insert(
          'local_meta',
          {'key': 'last_migration', 'value': oldVersion == 2 ? '2->3' : '1->3'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
      }
      if (oldVersion < 4) {
        await db.execute('ALTER TABLE catalog_items ADD COLUMN name_ar TEXT');
        await db.execute('ALTER TABLE catalog_items ADD COLUMN category_ar TEXT');
        await db.execute('ALTER TABLE catalog_items ADD COLUMN description TEXT NOT NULL DEFAULT ''');
        await db.execute('ALTER TABLE catalog_items ADD COLUMN description_ar TEXT');
        await db.insert(
          'local_meta',
          {'key': 'schema_version', 'value': '4'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
        await db.insert(
          'local_meta',
          {'key': 'last_migration', 'value': '3->4'},
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
      }
    });
  }

  Future<String?> getLastStoreId() async {
    final db = await database;
    final rows = await db.query('local_meta', where: 'key = ?', whereArgs: ['last_store_id'], limit: 1);
    return rows.isEmpty ? null : rows.first['value'] as String?;
  }

  Future<void> setLastStoreId(String storeId) async {
    final db = await database;
    await db.insert('local_meta', {'key': 'last_store_id', 'value': storeId}, conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<String?> getMeta(String key) async {
    final db = await database;
    final rows = await db.query('local_meta', where: 'key = ?', whereArgs: [key], limit: 1);
    return rows.isEmpty ? null : rows.first['value'] as String?;
  }

  Future<String> getOrCreateGuestSession() async {
    final db = await database;
    final existing = await db.query('local_meta', where: 'key = ?', whereArgs: ['guest_session'], limit: 1);
    if (existing.isNotEmpty) return existing.first['value']! as String;
    final random = Random.secure();
    final bytes = List<int>.generate(24, (_) => random.nextInt(256));
    final session = bytes.map((value) => value.toRadixString(16).padLeft(2, '0')).join();
    await db.insert('local_meta', {'key': 'guest_session', 'value': session});
    return session;
  }

  Future<void> replaceCatalog({required String storeId, required List<CatalogItem> items}) async {
    final db = await database;
    await db.transaction((txn) async {
      final batch = txn.batch();
      final syncedAt = DateTime.now().toUtc().toIso8601String();
      for (final item in items) {
        batch.insert('catalog_items', {...item.toMap(), 'store_id': storeId, 'last_synced_at': syncedAt}, conflictAlgorithm: ConflictAlgorithm.replace);
      }
      await batch.commit(noResult: true);
      await txn.insert('local_meta', {'key': 'catalog_last_synced_at', 'value': DateTime.now().toUtc().toIso8601String()}, conflictAlgorithm: ConflictAlgorithm.replace);
    });
  }

  Future<List<CatalogItem>> getCatalog(String storeId) async {
    final db = await database;
    final rows = await db.query('catalog_items', where: 'store_id = ?', whereArgs: [storeId], orderBy: 'category, name');
    return rows.map((row) => CatalogItem.fromMap(row)).toList();
  }

  Future<void> setCartLine({required String storeId, required String productId, required String name, required int quantity, required double unitPrice}) async {
    final db = await database;
    if (quantity <= 0) {
      await db.delete('cart_lines', where: 'product_id = ? AND store_id = ?', whereArgs: [productId, storeId]);
      return;
    }
    await db.insert('cart_lines', {
      'product_id': productId,
      'store_id': storeId,
      'name': name,
      'quantity': quantity,
      'unit_price': unitPrice,
    }, conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<void> addToCart({required String storeId, required String productId, required String name, required double unitPrice}) async {
    final db = await database;
    final current = await db.query('cart_lines', where: 'product_id = ? AND store_id = ?', whereArgs: [productId, storeId], limit: 1);
    final quantity = current.isEmpty ? 1 : (current.first['quantity']! as int) + 1;
    await setCartLine(storeId: storeId, productId: productId, name: name, quantity: quantity, unitPrice: unitPrice);
  }

  Future<List<Map<String, Object?>>> getCart(String storeId) async {
    final db = await database;
    return db.query('cart_lines', where: 'store_id = ?', whereArgs: [storeId], orderBy: 'name');
  }


  Future<void> clearCart(String storeId) async {
    final db = await database;
    await db.delete('cart_lines', where: 'store_id = ?', whereArgs: [storeId]);
  }

  Future<String> enqueueSubmission({required Map<String, Object?> payload, required String idempotencyKey}) async {
    final db = await database;
    final stamp = DateTime.now().toUtc();
    final suffix = Random().nextInt(1 << 31);
    final localId = 'op-${stamp.microsecondsSinceEpoch}-$suffix';
    await db.insert('sync_queue', {
      'local_operation_id': localId,
      'idempotency_key': idempotencyKey,
      'operation_type': 'CREATE_ORDER',
      'payload_version': 1,
      'payload_json': jsonEncode(payload),
      'retry_count': 0,
      'status': 'PENDING',
      'created_at': stamp.toIso8601String(),
    });
    return idempotencyKey;
  }

  Future<List<Map<String, Object?>>> getPendingSyncOperations() async {
    final db = await database;
    return db.query('sync_queue', where: 'status = ?', whereArgs: ['PENDING'], orderBy: 'created_at');
  }

  Future<void> markSyncCompleted(int id) async {
    final db = await database;
    await db.update('sync_queue', {'status': 'COMPLETED'}, where: 'id = ?', whereArgs: [id]);
  }

  Future<void> markSyncRetry(int id, {required String code, required String message}) async {
    final db = await database;
    await db.rawUpdate(
      'UPDATE sync_queue SET retry_count = retry_count + 1, last_attempt_at = ?, last_failure_code = ?, last_error_message = ? WHERE id = ?',
      [DateTime.now().toUtc().toIso8601String(), code, message, id],
    );
  }

  Future<void> markSyncConflict(int id, {required String code, required String message}) async {
    final db = await database;
    await db.update(
      'sync_queue',
      {
        'status': 'CONFLICT',
        'last_attempt_at': DateTime.now().toUtc().toIso8601String(),
        'last_failure_code': code,
        'last_error_message': message,
      },
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}
