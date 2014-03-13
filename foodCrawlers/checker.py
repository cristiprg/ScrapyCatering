import unicodedata
import string


def checkAndExtract( selector, regExp ):
	selectedSet = selector.select( regExp ).extract()
	
	# We don't have to continue
	if selectedSet == []:
		return ""
		
	# We get rid of the empty spaces
	resultUnicode = selectedSet[0].replace( '\r\n', '' )
	result = unicodedata.normalize( 'NFKD', resultUnicode ).encode( 'ascii', 'ignore' )
	
	return result
