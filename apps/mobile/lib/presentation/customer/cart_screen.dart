import 'package:flutter/material.dart';

import '../../core/i18n/jahhezly_localizations.dart';
import '../../core/network/api_exception.dart';
import '../../data/local/local_database.dart';
import '../../data/repositories/order_repository.dart';
import '../../domain/models/cart_line.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key, required this.local, required this.orders, required this.storeId, required this.onOrderSubmitted});
  final LocalDatabase local;
  final OrderRepository orders;
  final String storeId;
  final ValueChanged<Map<String, dynamic>> onOrderSubmitted;

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  List<CartLine> lines = const [];
  bool loading = true;
  bool submitting = false;
  String? message;
  final _phone = TextEditingController();

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    _phone.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    final rows = await widget.local.getCart(widget.storeId);
    if (!mounted) return;
    setState(() {
      lines = rows.map((row) => CartLine(
        productId: row['product_id']! as String,
        name: row['name']! as String,
        quantity: row['quantity']! as int,
        unitPrice: (row['unit_price']! as num).toDouble(),
      )).toList();
      loading = false;
    });
  }

  Future<void> _setQuantity(CartLine line, int quantity) async {
    await widget.local.setCartLine(storeId: widget.storeId, productId: line.productId, name: line.name, quantity: quantity, unitPrice: line.unitPrice);
    await _load();
  }

  Future<void> _submit() async {
    if (lines.isEmpty || submitting) return;
    final strings = JahhezlyStrings.of(context);
    final phone = _phone.text.trim();
    if (phone.isEmpty) {
      setState(() => message = strings.phoneRequired);
      return;
    }
    final items = lines.map((line) => {
      'productId': line.productId,
      'quantity': line.quantity,
      'clientUnitPrice': line.unitPrice,
    }).toList();

    setState(() { submitting = true; message = null; });
    try {
      final result = await widget.orders.submit(storeId: widget.storeId, items: items, customerPhone: phone);
      if (!mounted) return;
      if (!result.queued) {
        await widget.local.clearCart(widget.storeId);
        await _load();
      }
      setState(() {
        submitting = false;
        message = result.queued ? strings.savedLocally : strings.submitted;
      });
      if (!result.queued && result.payload != null) {
        widget.onOrderSubmitted(result.payload!);
      }
    } on ApiException catch (error) {
      if (!mounted) return;
      setState(() {
        submitting = false;
        message = '${error.code}: ${error.message}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final strings = JahhezlyStrings.of(context);
    if (loading) return const Center(child: CircularProgressIndicator());
    final total = lines.fold<double>(0, (sum, line) => sum + line.lineTotal);
    return Scaffold(
      appBar: AppBar(title: Text(strings.isArabic ? 'مراجعة الطلب' : 'Review order')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (lines.isEmpty)
            Padding(padding: const EdgeInsets.symmetric(vertical: 40), child: Text(strings.emptyCart)),
          for (final line in lines)
            Card(
              child: ListTile(
                title: Text(line.name),
                subtitle: Text('${line.quantity} × ${line.unitPrice.toStringAsFixed(2)} SYP'),
                leading: IconButton(onPressed: () => _setQuantity(line, line.quantity - 1), icon: const Icon(Icons.remove_circle_outline)),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(line.quantity.toString()),
                    IconButton(onPressed: () => _setQuantity(line, line.quantity + 1), icon: const Icon(Icons.add_circle_outline)),
                  ],
                ),
              ),
            ),
          if (lines.isNotEmpty) ...[
            const SizedBox(height: 8),
            TextField(
              controller: _phone,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(labelText: strings.phone, hintText: strings.phoneHint, prefixIcon: const Icon(Icons.phone_outlined)),
            ),
            const Divider(height: 28),
            ListTile(
              title: Text(strings.estimatedTotal),
              trailing: Text('${total.toStringAsFixed(2)} SYP', style: const TextStyle(fontWeight: FontWeight.w700)),
            ),
          ],
          FilledButton(
            onPressed: lines.isEmpty || submitting ? null : _submit,
            child: Text(submitting ? (strings.isArabic ? 'جارٍ الإرسال...' : 'Submitting...') : strings.sendOrder),
          ),
          if (message != null) Padding(padding: const EdgeInsets.only(top: 16), child: SelectableText(message!)),
        ],
      ),
    );
  }
}
