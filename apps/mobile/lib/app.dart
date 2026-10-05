import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'application/catalog_controller.dart';
import 'core/config/app_config.dart';
import 'core/i18n/jahhezly_localizations.dart';
import 'core/network/api_client.dart';
import 'core/network/merchant_api.dart';
import 'core/theme/jahhezly_theme.dart';
import 'data/local/local_database.dart';
import 'data/local/sync_queue_processor.dart';
import 'data/repositories/catalog_repository.dart';
import 'data/repositories/order_repository.dart';
import 'presentation/customer/cart_screen.dart';
import 'presentation/customer/catalog_screen.dart';
import 'presentation/customer/order_status_screen.dart';
import 'presentation/customer/store_selection_screen.dart';
import 'presentation/merchant/merchant_dashboard.dart';

class JahhezlyApp extends StatefulWidget {
  const JahhezlyApp({super.key});

  @override
  State<JahhezlyApp> createState() => _JahhezlyAppState();
}

class _JahhezlyAppState extends State<JahhezlyApp> with WidgetsBindingObserver {
  late final LocalDatabase _local;
  late final ApiClient _api;
  late final MerchantApi _merchantApi;
  late final CatalogController _catalog;
  late final OrderRepository _orders;
  late final SyncQueueProcessor _sync;
  String? _storeId;
  int _index = 0;
  Locale _locale = const Locale('ar');
  late final Future<void> _bootstrap;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _local = LocalDatabase();
    _api = ApiClient(baseUrl: AppConfig.fromEnvironment.apiBaseUrl);
    _merchantApi = MerchantApi(baseUrl: AppConfig.fromEnvironment.apiBaseUrl);
    _bootstrap = _bootstrapAsync();
  }

  Future<void> _bootstrapAsync() async {
    final guestSession = await _local.getOrCreateGuestSession();
    _api.guestSession = guestSession;
    _catalog = CatalogController(CatalogRepository(api: _api, local: _local));
    _orders = OrderRepository(api: _api, local: _local);
    _sync = SyncQueueProcessor(local: _local, api: _api);
    _storeId = await _local.getLastStoreId();
    await _sync.drain();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _sync.drain();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  void _toggleLocale() {
    setState(() {
      _locale = _locale.languageCode == 'ar' ? const Locale('en') : const Locale('ar');
    });
  }

  Future<void> _selectStore(String id) async {
    await _local.setLastStoreId(id);
    if (!mounted) return;
    setState(() {
      _storeId = id;
      _index = 0;
    });
  }

  void _openOrderStatus(Map<String, dynamic> order) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => OrderStatusScreen(
          repository: _orders,
          orderId: '${order['id']}',
          whatsappPhone: order['customerPhone'] as String?,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Jahhezly',
        debugShowCheckedModeBanner: false,
        theme: JahhezlyTheme.light(),
        locale: _locale,
        supportedLocales: const [Locale('ar'), Locale('en')],
        localizationsDelegates: const [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
          JahhezlyLocalizationsDelegate(),
        ],
        home: FutureBuilder<void>(
          future: _bootstrap,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Scaffold(body: Center(child: CircularProgressIndicator()));
            }
            if (snapshot.hasError) {
              return const Scaffold(body: Center(child: Text('Jahhezly could not initialize local storage.')));
            }
            return Directionality(
              textDirection: _locale.languageCode == 'ar' ? TextDirection.rtl : TextDirection.ltr,
              child: _buildShell(),
            );
          },
        ),
      );

  Widget _buildShell() {
    if (_storeId == null) {
      return StoreSelectionScreen(
        api: _api,
        onToggleLocale: _toggleLocale,
        onSelected: _selectStore,
        onMerchantLogin: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => MerchantDashboard(api: _merchantApi))),
      );
    }

    final strings = JahhezlyStrings(_locale);
    return Scaffold(
      body: _index == 0
          ? CatalogScreen(
              controller: _catalog,
              storeId: _storeId!,
              onToggleLocale: _toggleLocale,
              onChangeStore: () => setState(() => _storeId = null),
              onAdd: (line) async => _local.addToCart(
                storeId: _storeId!,
                productId: line.productId,
                name: line.name,
                unitPrice: line.unitPrice,
              ),
            )
          : CartScreen(
              local: _local,
              orders: _orders,
              storeId: _storeId!,
              onOrderSubmitted: _openOrderStatus,
            ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() => _index = value),
        destinations: [
          NavigationDestination(icon: const Icon(Icons.storefront_outlined), label: strings.catalog),
          NavigationDestination(icon: const Icon(Icons.shopping_cart_outlined), label: strings.cart),
        ],
      ),
    );
  }
}
