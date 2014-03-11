class foodItem():
	def __init__(self):
		pass

	def __init__(self, foodName, category, ingredients, price):
		self.foodName = foodName
		self.category = category
		self.price = price
		self.ingredients = ingredients
	
	def display(self):
		print "||==<Food Item>==||"
		print "Food Name: ", self.foodName
		print "Category: ", self.category
		print "Price: ", self.price
		print "Ingredients: ", self.ingredients
		print ""
	