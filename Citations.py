'''
@author: Linh Vo
@purpose: This program parse the text of references in APA format
to separate the values of specific fields
'''

# Get citation input from user
citationText = input('Please enter a reference:\n').strip()

# Initialize variables
category = ''
author = ''
title = ''
year = ''
month = ''
publication = ''
volume = ''
issue = ''
pages = ''
publisher = ''
address = ''

# Find author

author, remainder = citationText.split('(', maxsplit=1)

# Find year and month of publication

date, remainder = remainder.split(').', maxsplit=1)

if date.isdigit():
    year = date
else:
    year, month = date.split(',')
    category = 'magazine article'

# Find title

# Get index and slice citation to get title based on ending symbol
if remainder.find('.') != -1:
    index = remainder.find('.')
elif remainder.find('!') != -1:
    index = remainder.find('!')
elif remainder.find('?') != 1:
    index = remainder.find('?')

title = remainder[: index + 1]
remainder = remainder[index + 1:]

# Find publisher, address for books and
# publication, pages, volume, issue for magazines and journals

remainderList = remainder.split(', ')

# If the last list element is not number of pages
if not remainderList[-1][0].isdigit():
    # Find publisher name and address based on colon separator
    if remainderList[1].find(':') != -1:
        address, publisher = remainder.split(':', maxsplit=1)
        category = 'book'
else:
    pages = remainderList[-1]
    volume, issue = remainderList[-2].split('(')
    issue = issue.replace(')', '')
    # Publication title includes all list elements except the last 2 elements
    publication = ', '.join(remainderList[:-2])

# If category is still empty at this point, assign it to journal article

if category == '':
    category = 'journal article'


# Print output

print(category.upper() + '---------------------------------------')
print('AUTHORS'.rjust(20) + ":", author.strip())
print('TITLE'.rjust(20) + ":", title.strip())
print('YEAR'.rjust(20) + ":", year.strip())
print('MONTH'.rjust(20) + ":", month.strip())
print('PUBLICATION TITLE'.rjust(20) + ":", publication.strip())
print('VOLUME'.rjust(20) + ":", volume.strip())
print('ISSUE'.rjust(20) + ":", issue.strip())
print('PAGES'.rjust(20) + ":", pages.strip())
print('PUBLISHER'.rjust(20) + ":", publisher.strip())
print('ADDRESS'.rjust(20) + ":", address.strip())
print('-------------------------------------------------------')
