import unicodedata
import string

"""
	string checkAndExtract( HtmlXPathSelector selector, string regExp )
	This function uses the regExp to extract information from the selector.
	If there is nothing to be extracted then it returns the empty string.
	Also this method converts the string from unicode to ASCII.

"""
def checkAndExtract( selector, regExp ):
	selectedSet = selector.select( regExp ).extract()
	
	# We don't have to continue
	if selectedSet == []:
		return ""
		
	# We get rid of the empty spaces
	resultUnicode = selectedSet[0].replace( '\n', '' ).replace( '\r', '' )
	
	result = unicodedata.normalize( 'NFKD', resultUnicode ).encode( 'ascii', 'ignore' )
	
	# Checks if there are only spaces in the string
	if( result.isspace() ):
		return ""
	
	return result
