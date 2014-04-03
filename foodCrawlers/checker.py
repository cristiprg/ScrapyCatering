import unicodedata
import string

"""
	string checkAndExtract( HtmlXPathSelector selector, string regExp )
	This function uses the regExp to extract information from the selector.
	If there is nothing to be extracted then it returns the empty string.
	Also this method converts the string from unicode to ASCII.

"""
def checkAndExtract( selector, regExp, index = 0 ):
	selectedSet = selector.select( regExp ).extract()
	
	# We don't have to continue
	if selectedSet == []:
		return ""
		
		
	if( index >= len(selectedSet) ):
		return ""	
		
	# We get rid of the empty spaces
	resultUnicode = selectedSet[index].replace( '\n', '' ).replace( '\r', '' )
	
	result = unicodeToAscii( resultUnicode )
	
	# Checks if there are only spaces in the string
	if( result.isspace() ):
		return ""
	
	return result
	
	

def unicodeToAscii( unicodeString ):
	result = unicodedata.normalize( 'NFKD', unicodeString ).encode( 'ascii', 'ignore' )
	
	if ( result.isspace() ):
		return ""
		
	return result
