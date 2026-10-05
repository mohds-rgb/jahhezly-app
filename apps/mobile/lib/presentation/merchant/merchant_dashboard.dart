import 'package:flutter/material.dart';

import '../../core/network/merchant_api.dart';

class MerchantDashboard extends StatefulWidget {
  const MerchantDashboard({super.key, required this.api});
  final MerchantApi api;

  @override
  State<MerchantDashboard> createState() => _MerchantDashboardState();
}

class _MerchantDashboardState extends State<MerchantDashboard> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  Map<String, dynamic>? profile;
  String? selectedStoreId;
  List<Map<String, dynamic>> orders = const [];
  bool busy = false;
  String? error;

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    setState(() { busy = true; error = null; });
    try {
      await widget.api.login(email: _email.text.trim(), password: _password.text);
      final result = await widget.api.me();
      final stores = List<Map<String, dynamic>>.from(result['memberships'] as List);
      if (!mounted) return;
      setState(() {
        profile = result;
        selectedStoreId = stores.isEmpty ? null : '${stores.first['storeId']}';
        busy = false;
      });
      if (selectedStoreId != null) await _loadOrders();
    } catch (e) {
      if (!mounted) return;
      setState(() { busy = false; error = '$e'; });
    }
  }

  Future<void> _loadOrders() async {
    final storeId = selectedStoreId;
    if (storeId == null) return;
    setState(() => busy = true);
    try {
      final result = await widget.api.orders(storeId);
      if (!mounted) return;
      setState(() { orders = result; busy = false; });
    } catch (e) {
      if (!mounted) return;
      setState(() { busy = false; error = '$e'; });
    }
  }

  Future<void> _transition(Map<String, dynamic> order) async {
    final state = '${order['state']}';
    final action = switch (state) {
      'SUBMITTED' => 'accept',
      'ACCEPTED' => 'start-preparing',
      'PREPARING' => 'ready',
      'READY_FOR_PICKUP' => 'collect',
      _ => null,
    };
    if (action == null) return;
    setState(() => busy = true);
    try {
      await widget.api.transition(orderId: '${order['id']}', action: action, version: order['version'] as int);
      await _loadOrders();
    } catch (e) {
      if (!mounted) return;
      setState(() { busy = false; error = '$e'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (profile == null) return _buildLogin();
    final stores = List<Map<String, dynamic>>.from(profile!['memberships'] as List);
    return Scaffold(
      appBar: AppBar(title: const Text('Merchant Operations')),
      body: RefreshIndicator(
        onRefresh: _loadOrders,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text('${profile!['displayName']}', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedStoreId,
              decoration: const InputDecoration(labelText: 'Store / branch'),
              items: [for (final store in stores) DropdownMenuItem(value: '${store['storeId']}', child: Text('${store['storeName']}'))],
              onChanged: (value) async { selectedStoreId = value; await _loadOrders(); },
            ),
            const SizedBox(height: 20),
            if (error != null) Card(child: ListTile(leading: const Icon(Icons.error_outline), title: Text(error!))),
            if (busy) const LinearProgressIndicator(),
            const SizedBox(height: 12),
            for (final order in orders)
              Card(
                child: ListTile(
                  title: Text('${order['publicOrderCode']}'),
                  subtitle: Text('${order['state']} · ${order['itemCount']} items · ${order['totalAmount']} ${order['currency']}'),
                  trailing: IconButton(onPressed: busy ? null : () => _transition(order), icon: const Icon(Icons.arrow_forward)),
                ),
              ),
            if (orders.isEmpty && !busy)
              const Padding(padding: EdgeInsets.symmetric(vertical: 40), child: Center(child: Text('No orders for this branch.'))),
          ],
        ),
      ),
    );
  }

  Widget _buildLogin() => Scaffold(
        appBar: AppBar(title: const Text('Merchant Login')),
        body: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text('Jahhezly Merchant', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            const Text('Server-authorized access to the stores and branches assigned to your account.'),
            const SizedBox(height: 20),
            TextField(controller: _email, keyboardType: TextInputType.emailAddress, decoration: const InputDecoration(labelText: 'Email')),
            const SizedBox(height: 12),
            TextField(controller: _password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
            const SizedBox(height: 16),
            FilledButton(onPressed: busy ? null : _login, child: Text(busy ? 'Signing in…' : 'Sign in')),
            if (error != null) Padding(padding: const EdgeInsets.only(top: 16), child: Text(error!)),
          ],
        ),
      );
}
