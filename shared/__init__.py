def truncate_string(string, length): 
	if len(string) > length: 
		return '{}{}'.format(string[:length- 1 ],'...')
	return string
