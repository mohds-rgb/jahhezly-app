import 'package:flutter/material.dart';

import '../../core/i18n/jahhezly_localizations.dart';
import '../../core/network/api_client.dart';

class StoreSelectionScreen extends StatefulWidget {
  const StoreSelectionScreen({super.key, required this.api, required this.onSelected, required this.onToggleLocale, required this.onMerchantLogin});
  final ApiClient api;
  final ValueChanged<String> onSelected;
  final VoidCallback onToggleLocale;
  final VoidCallback onMerchantLogin;

  @override
  State<StoreSelectionScreen> createState() => _StoreSelectionScreenState();
}

class _StoreSelectionScreenState extends State<StoreSelectionScreen> {
  List<Map<String, dynamic>> stores = const [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => loading = true);
    try {
      final result = await widget.api.getStores();
      if (!mounted) return;
      setState(() { stores = result; loading = false; error = null; });
    } catch (_) {
      if (!mounted) return;
      setState(() { loading = false; error = 'Unable to load stores. Check your connection and retry.'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    final strings = JahhezlyStrings.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(strings.chooseStore),
        actions: [
          IconButton(
            tooltip: strings.isArabic ? 'English' : 'العربية',
            onPressed: widget.onToggleLocale,
            icon: const Icon(Icons.language),
          ),
          IconButton(
            tooltip: strings.merchantMode,
            onPressed: widget.onMerchantLogin,
            icon: const Icon(Icons.admin_panel_settings_outlined),
          ),
        ],
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : error != null
              ? Center(child: FilledButton.icon(onPressed: _load, icon: const Icon(Icons.refresh), label: Text(strings.retry)))
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    Center(
                      child: Image.asset('assets/brand/jahhezly-icon-square.png', width: 96, height: 96),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      strings.isArabic ? 'ابدأ بالتسوق مسبقاً' : 'Prepare your shopping before you arrive',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 20),
                    for (final store in stores)
                      Card(
                        child: ListTile(
                          title: Text('${store['name']}'),
                          subtitle: Text([store['district'], store['city']].where((v) => v != null && v.toString().isNotEmpty).join(' · ')),
                          leading: const CircleAvatar(child: Icon(Icons.storefront_outlined)),
                          onTap: () => widget.onSelected('${store['id']}'),
                          trailing: const Icon(Icons.chevron_left),
                        ),
                      ),
                  ],
                ),
    );
  }
}
