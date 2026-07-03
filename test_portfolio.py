from execution.portfolio import Portfolio

p = Portfolio()

print(p.buy(100))
print(p.summary(101))

print(p.sell(105))
print(p.summary(105))
