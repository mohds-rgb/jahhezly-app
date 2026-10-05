class CatalogItem {
  const CatalogItem({
    required this.id,
    required this.name,
    this.nameAr,
    required this.description,
    this.descriptionAr,
    required this.category,
    this.categoryAr,
    required this.unitLabel,
    required this.active,
    required this.available,
    required this.priceAmount,
    required this.currency,
    required this.lastSyncedAt,
  });

  final String id;
  final String name;
  final String? nameAr;
  final String description;
  final String? descriptionAr;
  final String category;
  final String? categoryAr;
  final String unitLabel;
  final bool active;
  final bool available;
  final double priceAmount;
  final String currency;
  final DateTime lastSyncedAt;

  factory CatalogItem.fromJson(Map<String, dynamic> json) => CatalogItem(
        id: json['id'] as String,
        name: json['name'] as String,
        nameAr: json['nameAr'] as String?,
        description: (json['description'] ?? '') as String,
        descriptionAr: json['descriptionAr'] as String?,
        category: json['category'] as String,
        categoryAr: json['categoryAr'] as String?,
        unitLabel: json['unitLabel'] as String,
        active: json['active'] as bool,
        available: json['availability'] == 'AVAILABLE',
        priceAmount: double.parse('${json['price'] ?? 0}'),
        currency: (json['currency'] ?? 'SYP') as String,
        lastSyncedAt: DateTime.now().toUtc(),
      );

  Map<String, Object?> toMap() => {
        'id': id,
        'name': name,
        'name_ar': nameAr,
        'description': description,
        'description_ar': descriptionAr,
        'category': category,
        'category_ar': categoryAr,
        'unit_label': unitLabel,
        'active': active ? 1 : 0,
        'available': available ? 1 : 0,
        'price_amount': priceAmount,
        'currency': currency,
        'last_synced_at': lastSyncedAt.toIso8601String(),
      };

  factory CatalogItem.fromMap(Map<String, Object?> map) => CatalogItem(
        id: map['id']! as String,
        name: map['name']! as String,
        nameAr: map['name_ar'] as String?,
        description: (map['description'] ?? '') as String,
        descriptionAr: map['description_ar'] as String?,
        category: map['category']! as String,
        categoryAr: map['category_ar'] as String?,
        unitLabel: map['unit_label']! as String,
        active: (map['active']! as int) == 1,
        available: (map['available']! as int) == 1,
        priceAmount: (map['price_amount']! as num).toDouble(),
        currency: map['currency']! as String,
        lastSyncedAt: DateTime.parse(map['last_synced_at']! as String),
      );

  String displayName(bool arabic) => arabic ? (nameAr ?? name) : name;
  String displayCategory(bool arabic) => arabic ? (categoryAr ?? category) : category;

  bool get isStale => DateTime.now().toUtc().difference(lastSyncedAt.toUtc()) > const Duration(hours: 6);
}
