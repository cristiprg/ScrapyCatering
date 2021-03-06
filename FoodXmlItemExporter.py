from scrapy.contrib.exporter import XmlItemExporter
from foodCrawlers.foodItem import foodItem

class FoodXmlItemExporter(XmlItemExporter):
	def serialize_field(self, field, name, value):
		return value

	def export_item(self, item):
        #self.xg.startElement(self.item_element, {})
		for name, value in self._get_serialized_fields(item, default_value=''):
			self._export_xml_field(name, value)
        #self.xg.endElement(self.item_element)
		
	def _export_xml_field(self, name, serialized_value):
		for key, value in serialized_value.iteritems():
			#this is mandatory
			if value.foodName is None:
				raise Exception("Food name is mandatory for exporting!")
		
			self.xg.startElement(self.item_element, {})

			self.xg.startElement("foodName", {})
			self.xg.characters(value.foodName)
			self.xg.endElement("foodName")
			
			
			if value.ingredients is not None:
				self.xg.startElement("ingredients", {})
				self.xg.characters(value.ingredients)
				self.xg.endElement("ingredients")
			
			if value.price is not None:
				self.xg.startElement("price", {})
				self.xg.characters(value.price)
				self.xg.endElement("price")

			if value.category is not None:
				self.xg.startElement("category", {})
				self.xg.characters(value.category)
				self.xg.endElement("category")
			
			self.xg.endElement(self.item_element)