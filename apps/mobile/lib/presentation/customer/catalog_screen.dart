import 'package:flutter/material.dart';

import '../../application/catalog_controller.dart';
import '../../core/i18n/jahhezly_localizations.dart';
import '../../domain/models/cart_line.dart';

class CatalogScreen extends StatefulWidget {
  const CatalogScreen({
    super.key,
    required this.controller,
    required this.storeId,
    required this.onAdd,
    required this.onToggleLocale,
    required this.onChangeStore,
  });
  final CatalogController controller;
  final String storeId;
  final void Function(CartLine line) onAdd;
  final VoidCallback onToggleLocale;
  final VoidCallback onChangeStore;

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  final TextEditingController _search = TextEditingController();

  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_refresh);
    _search.addListener(_refresh);
    widget.controller.load(widget.storeId);
  }

  @override
  void dispose() {
    widget.controller.removeListener(_refresh);
    _search.removeListener(_refresh);
    _search.dispose();
    super.dispose();
  }

  void _refresh() {
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final strings = JahhezlyStrings.of(context);
    final query = _search.text.trim().toLowerCase();
    final items = widget.controller.items.where((item) {
      if (query.isEmpty) return true;
      return item.name.toLowerCase().contains(query) || item.category.toLowerCase().contains(query);
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: Text(strings.appName),
        actions: [
          IconButton(onPressed: widget.onChangeStore, tooltip: strings.changeStore, icon: const Icon(Icons.storefront)),
          IconButton(onPressed: widget.onToggleLocale, icon: const Icon(Icons.language)),
        ],
      ),
      body: widget.controller.loading && widget.controller.items.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: () => widget.controller.load(widget.storeId),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  TextField(
                    controller: _search,
                    decoration: InputDecoration(prefixIcon: const Icon(Icons.search), hintText: strings.search),
                  ),
                  const SizedBox(height: 12),
                  if (widget.controller.fromCache)
                    Card(
                      child: ListTile(
                        leading: const Icon(Icons.cloud_off_outlined),
                        title: Text(strings.offlineCatalog),
                        subtitle: Text(strings.staleCatalog),
                      ),
                    ),
                  for (final item in items)
                    Card(
                      child: ListTile(
                        onTap: () => _showDetails(item),
                        title: Text(item.displayName(strings.isArabic)),
                        subtitle: Text('${item.priceAmount.toStringAsFixed(2)} ${item.currency} / ${item.unitLabel}'),
                        trailing: FilledButton(
                          onPressed: item.active && item.available
                              ? () => widget.onAdd(CartLine(productId: item.id, quantity: 1, unitPrice: item.priceAmount, name: item.displayName(strings.isArabic)))
                              : null,
                          child: Text(strings.addToCart),
                        ),
                      ),
                    ),
                  if (items.isEmpty)
                    Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text(widget.controller.error != null ? strings.noCatalog : strings.search),
                    ),
                ],
              ),
            ),
    );
  }

  void _showDetails(dynamic item) {
    final strings = JahhezlyStrings.of(context);
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (context) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(item.displayName(strings.isArabic), style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
              const SizedBox(height: 8),
              Text(strings.isArabic ? (item.descriptionAr ?? item.description) : item.description),
              const SizedBox(height: 16),
              Text('${item.priceAmount.toStringAsFixed(2)} ${item.currency} / ${item.unitLabel}'),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: item.active && item.available ? () { Navigator.pop(context); widget.onAdd(CartLine(productId: item.id, quantity: 1, unitPrice: item.priceAmount, name: item.displayName(strings.isArabic))); } : null,
                child: Text(strings.addToCart),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
