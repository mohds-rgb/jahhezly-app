import 'package:url_launcher/url_launcher.dart';

class WhatsAppAdapter {
  Future<bool> openOrderMessage({required String phoneNumber, required String message}) async {
    final normalized = phoneNumber.replaceAll(RegExp(r'[^0-9]'), '');
    final uri = Uri.https('wa.me', '/$normalized', {'text': message});
    return launchUrl(uri, mode: LaunchMode.externalApplication);
  }
}
