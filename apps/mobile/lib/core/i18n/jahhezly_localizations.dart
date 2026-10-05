import 'package:flutter/material.dart';

class JahhezlyStrings {
  const JahhezlyStrings(this.locale);
  final Locale locale;
  bool get isArabic => locale.languageCode == 'ar';

  String get appName => 'Jahhezly';
  String get chooseStore => isArabic ? 'اختر المتجر' : 'Choose a store';
  String get customerMode => isArabic ? 'تجربة العميل' : 'Customer';
  String get merchantMode => isArabic ? 'دخول المتجر' : 'Merchant login';
  String get retry => isArabic ? 'إعادة المحاولة' : 'Retry';
  String get addToCart => isArabic ? 'أضف للسلة' : 'Add to cart';
  String get cart => isArabic ? 'السلة' : 'Cart';
  String get catalog => isArabic ? 'المتجر' : 'Store';
  String get offlineCatalog => isArabic ? 'الكتالوج المحفوظ محلياً' : 'Cached catalog';
  String get staleCatalog => isArabic ? 'الأسعار المعروضة قديمة؛ سيتم التحقق منها عند الإرسال.' : 'Cached prices may be stale; final values are checked at submission.';
  String get noCatalog => isArabic ? 'لا يوجد كتالوج متاح محلياً حالياً.' : 'No catalog is available locally yet.';
  String get sendOrder => isArabic ? 'إرسال الطلب' : 'Submit order';
  String get changeStore => isArabic ? 'تغيير المتجر' : 'Change store';
  String get search => isArabic ? 'بحث في المنتجات' : 'Search products';
  String get emptyCart => isArabic ? 'السلة فارغة.' : 'Your cart is empty.';
  String get phone => isArabic ? 'رقم الهاتف للتواصل' : 'Contact phone number';
  String get phoneHint => isArabic ? '+963 9xx xxx xxx' : '+963 9xx xxx xxx';
  String get phoneRequired => isArabic ? 'أدخل رقم هاتف صالحاً للتواصل عند الاستلام.' : 'Enter a valid phone number for pickup contact.';
  String get estimatedTotal => isArabic ? 'الإجمالي التقديري' : 'Estimated total';
  String get savedLocally => isArabic ? 'محفوظ محلياً؛ بانتظار الاتصال.' : 'Saved locally; waiting for a connection.';
  String get submitted => isArabic ? 'تم إرسال الطلب إلى المتجر.' : 'Order submitted to the store.';
  String get preparing => isArabic ? 'جارٍ تجهيز الطلب' : 'Order is being prepared';
  String get ready => isArabic ? 'الطلب جاهز للاستلام' : 'Order is ready for pickup';
  String get collected => isArabic ? 'تم استلام الطلب' : 'Order collected';
  String get orderStatus => isArabic ? 'حالة الطلب' : 'Order status';

  static JahhezlyStrings of(BuildContext context) =>
      JahhezlyStrings(Localizations.localeOf(context));
}

class JahhezlyLocalizationsDelegate extends LocalizationsDelegate<JahhezlyStrings> {
  const JahhezlyLocalizationsDelegate();
  @override bool isSupported(Locale locale) => const ['ar', 'en'].contains(locale.languageCode);
  @override Future<JahhezlyStrings> load(Locale locale) async => JahhezlyStrings(locale);
  @override bool shouldReload(covariant LocalizationsDelegate<JahhezlyStrings> old) => false;
}
