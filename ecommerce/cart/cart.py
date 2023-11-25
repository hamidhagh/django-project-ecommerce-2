from home.models import ProductLine

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_line, quantity):
        product_line_id = str(product_line.id)
        if product_line_id not in self.cart:
            self.cart[product_line_id] = {'quantity': 0, 'price': str(product_line.sale_price)}
        self.cart[product_line_id]['quantity'] += quantity
        self.save()

    def remove(self, product_line):
        product_line_id = str(product_line.id)
        del self.cart[product_line_id]
        self.save()

    def remove_all(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def total_price(self):
        return sum(int(x['price']) * x['quantity'] for x in self.cart.values())
    

    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_line_ids = self.cart.keys()
        product_lines = ProductLine.objects.filter(id__in=product_line_ids)
        for product_line in product_lines:
            self.cart[str(product_line.id)]['product_line'] = product_line

        for data in self.cart.values():
            data['sale_price'] = int(data['price']) * data['quantity']
            yield data

    def save(self):
        self.session.modified = True
