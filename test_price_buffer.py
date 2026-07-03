from core.price_buffer import PriceBuffer

buffer = PriceBuffer()

for i in range(25):
    buffer.add(i)

print("Latest:", buffer.latest())
print("Size:", buffer.size())
print("Ready:", buffer.is_ready())
print("Prices:", buffer.get_prices()[-5:])
