class CartLine {
  const CartLine({required this.productId, required this.quantity, required this.unitPrice, required this.name});

  final String productId;
  final int quantity;
  final double unitPrice;
  final String name;

  double get lineTotal => unitPrice * quantity;
}
