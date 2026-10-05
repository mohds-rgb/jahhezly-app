import 'package:flutter/material.dart';

class JahhezlyTheme {
  static const navy = Color(0xFF1A2671);
  static const orange = Color(0xFFEA5521);
  static const mint = Color(0xFF69B2A5);

  static ThemeData light() => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: navy,
          primary: navy,
          secondary: orange,
          tertiary: mint,
          surface: const Color(0xFFF4F6FA),
          brightness: Brightness.light,
        ),
        scaffoldBackgroundColor: const Color(0xFFF4F6FA),
        appBarTheme: const AppBarTheme(
          backgroundColor: navy,
          foregroundColor: Colors.white,
          centerTitle: false,
        ),
        cardTheme: const CardThemeData(
          margin: EdgeInsets.only(bottom: 12),
          elevation: 0,
          surfaceTintColor: Colors.transparent,
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          filled: true,
          fillColor: Colors.white,
        ),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      );
}
