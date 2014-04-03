import unicodedata
import string

"""
	string checkAndExtract( HtmlXPathSelector selector, string htmlParser, int index = 0 )
	This function uses the htmlParser to extract information from the selector
	which is found at position index. (0 is the implicit value ).
	If there is nothing to be extracted then it returns the empty string.
	Also this method converts the string from unicode to ASCII.

"""
def checkAndExtract( selector, regExp, index = 0 ):
	selectedSet = selector.select( regExp ).extract()
	
	# We don't have to continue
	if selectedSet == []:
		return ""
		
	# If the index requested is not a valid one we
	# return the empty string	
	if( index >= len(selectedSet) or index < 0 ):
		return ""	
		
	# We get rid of the empty spaces
	resultUnicode = selectedSet[index].replace( '\n', '' ).replace( '\r', '' )
	
	result = unicodeToAscii( resultUnicode )
	
	# Checks if there are only spaces in the string
	if( result.isspace() ):
		return ""
	
	return result
	
	
"""
	string unicodeToAscii( UnicodeString unicodeString )
	This function converts the unicodeString to an ASCII string.
	If the resulting string contains only whitespaces( no matter how many )
	the empty string is returned.

"""
def unicodeToAscii( unicodeString ):
	result = unicodedata.normalize( 'NFKD', unicodeString ).encode( 'ascii', 'ignore' )
	
	if ( result.isspace() ):
		return ""
		
	return result
