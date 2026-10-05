import 'package:flutter/material.dart';

import '../../core/i18n/jahhezly_localizations.dart';
import '../../core/whatsapp/whatsapp_adapter.dart';
import '../../data/repositories/order_repository.dart';

class OrderStatusScreen extends StatefulWidget {
  const OrderStatusScreen({super.key, required this.repository, required this.orderId, this.whatsappPhone});
  final OrderRepository repository;
  final String orderId;
  final String? whatsappPhone;

  @override
  State<OrderStatusScreen> createState() => _OrderStatusScreenState();
}

class _OrderStatusScreenState extends State<OrderStatusScreen> {
  Map<String, dynamic>? order;
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final result = await widget.repository.getOrder(widget.orderId);
      if (!mounted) return;
      setState(() { order = result; loading = false; error = null; });
    } catch (_) {
      if (!mounted) return;
      setState(() { loading = false; error = 'Unable to refresh order status. Last known state may be retained.'; });
    }
  }

  String _label(String state, JahhezlyStrings strings) => switch (state) {
        'SUBMITTED' => strings.isArabic ? 'تم الإرسال' : 'Submitted',
        'ACCEPTED' => strings.isArabic ? 'تم قبول الطلب' : 'Accepted',
        'PREPARING' => strings.preparing,
        'READY_FOR_PICKUP' => strings.ready,
        'COLLECTED' => strings.collected,
        'REJECTED' => strings.isArabic ? 'مرفوض' : 'Rejected',
        'CANCELLED' => strings.isArabic ? 'ملغى' : 'Cancelled',
        _ => state,
      };

  @override
  Widget build(BuildContext context) {
    final strings = JahhezlyStrings.of(context);
    if (loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    if (order == null) {
      return Scaffold(appBar: AppBar(title: Text(strings.orderStatus)), body: Center(child: Text(error ?? strings.noCatalog)));
    }
    final state = '${order!['state']}';
    final code = '${order!['publicOrderCode']}';
    final phone = order!['customerPhone'] as String? ?? widget.whatsappPhone;
    final timeline = const ['SUBMITTED', 'ACCEPTED', 'PREPARING', 'READY_FOR_PICKUP', 'COLLECTED'];
    final activeIndex = timeline.indexOf(state);

    return Scaffold(
      appBar: AppBar(title: Text(strings.orderStatus), actions: [IconButton(onPressed: _load, icon: const Icon(Icons.refresh))]),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(code, style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 8),
          Text(_label(state, strings), style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 20),
          for (var index = 0; index < timeline.length; index++)
            ListTile(
              leading: Icon(index <= activeIndex && activeIndex >= 0 ? Icons.check_circle : Icons.radio_button_unchecked),
              title: Text(_label(timeline[index], strings)),
            ),
          if (phone != null)
            OutlinedButton.icon(
              onPressed: () => WhatsAppAdapter().openOrderMessage(phoneNumber: phone, message: 'Jahhezly — order $code'),
              icon: const Icon(Icons.message_outlined),
              label: Text(strings.isArabic ? 'التواصل عبر WhatsApp' : 'Contact via WhatsApp'),
            ),
          if (error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(error!)),
        ],
      ),
    );
  }
}
