#!/usr/bin/env python3

## modified script from ppannuto, see github: https://github.com/ppannuto/python-titlecase

import re
import sys

SMALL = 'a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?'
PUNCT = r"""!"“#$%&'‘()*+,\-–‒—―./:;?@[\\\]_`{|}~"""

SMALL_WORDS = re.compile(r'^(%s)$' % SMALL, re.I)
INLINE_PERIOD = re.compile(r'[a-z][.][a-z]', re.I)
UC_ELSEWHERE = re.compile(r'[%s]*?[a-zA-Z]+[A-Z]+?' % PUNCT)
CAPFIRST = re.compile(r"^[%s]*?([A-Za-z])" % PUNCT)
SMALL_FIRST = re.compile(r'^([%s]*)(%s)\b' % (PUNCT, SMALL), re.I)
SMALL_LAST = re.compile(r'\b(%s)[%s]?$' % (SMALL, PUNCT), re.I)
SUBPHRASE = re.compile(r'([:.;?!\-–‒—―][ ])(%s)' % SMALL)
APOS_SECOND = re.compile(r"^[dol]{1}['‘]{1}[a-z]+(?:['s]{2})?$", re.I)
UC_INITIALS = re.compile(r"^(?:[A-Z]{1}\.{1}|[A-Z]{1}\.{1}[A-Z]{1})+$")
MAC_MC = re.compile(r"^([Mm]c|MC)(\w.+)")


class Immutable(object):
    pass

class ImmutableString(str, Immutable):
    pass

class ImmutableBytes(bytes, Immutable):
    pass


def _mark_immutable(text):
    if isinstance(text, bytes):
        return ImmutableBytes(text)
    return ImmutableString(text)


def set_small_word_list(small=SMALL):
	global SMALL_WORDS
	global SMALL_FIRST
	global SMALL_LAST
	global SUBPHRASE
	SMALL_WORDS = re.compile(r'^(%s)$' % small, re.I)
	SMALL_FIRST = re.compile(r'^([%s]*)(%s)\b' % (PUNCT, small), re.I)
	SMALL_LAST = re.compile(r'\b(%s)[%s]?$' % (small, PUNCT), re.I)
	SUBPHRASE = re.compile(r'([:.;?!][ ])(%s)' % small)


def titlecase(text, callback = None, small_first_last=True):
	"""
	Titlecases input text
	This filter changes all words to Title Caps, and attempts to be clever
	about *un*capitalizing SMALL words like a/an/the in the input.
	The list of "SMALL words" which are not capped comes from
	the New York Times Manual of Style, plus 'vs' and 'v'.
	"""

	lines = re.split('[\r\n]+', text)
	processed = []
	for line in lines:
		all_caps = line.upper() == line
		words = re.split('[\t ]', line)
		tc_line = []
		for word in words:
			if callback:
				new_word = callback(word, all_caps=all_caps)
				if new_word:
					# Address #22: If a callback has done something
					# specific, leave this string alone from now on
					tc_line.append(_mark_immutable(new_word))
					continue

			if all_caps:
				if UC_INITIALS.match(word):
					tc_line.append(word)
					continue

			if APOS_SECOND.match(word):
				if len(word[0]) == 1 and word[0] not in 'aeiouAEIOU':
					word = word[0].lower() + word[1] + word[2].upper() + word[3:]
				else:
					word = word[0].upper() + word[1] + word[2].upper() + word[3:]
				tc_line.append(word)
				continue

			match = MAC_MC.match(word)
			if match:
				tc_line.append("%s%s" % (match.group(1).capitalize(),
										 titlecase(match.group(2),callback,small_first_last)))
				continue

			if INLINE_PERIOD.search(word) or (not all_caps and UC_ELSEWHERE.match(word)):
				tc_line.append(word)
				continue
			if SMALL_WORDS.match(word):
				tc_line.append(word.lower())
				continue

			if "/" in word and "//" not in word:
				slashed = map(
					lambda t: titlecase(t,callback,False),
					word.split('/')
				)
				tc_line.append("/".join(slashed))
				continue

			if '-' in word:
				hyphenated = map(
					lambda t: titlecase(t,callback,small_first_last),
					word.split('-')
				)
				tc_line.append("-".join(hyphenated))
				continue

			if all_caps:
				word = word.lower()

			# Just a normal word that needs to be capitalized
			tc_line.append(CAPFIRST.sub(lambda m: m.group(0).upper(), word))

		if small_first_last and tc_line:
			if not isinstance(tc_line[0], Immutable):
				tc_line[0] = SMALL_FIRST.sub(lambda m: '%s%s' % (
					m.group(1),
					m.group(2).capitalize()
				), tc_line[0])

			if not isinstance(tc_line[-1], Immutable):
				tc_line[-1] = SMALL_LAST.sub(
					lambda m: m.group(0).capitalize(), tc_line[-1]
				)

		result = " ".join(tc_line)

		result = SUBPHRASE.sub(lambda m: '%s%s' % (
			m.group(1),
			m.group(2).capitalize()
		), result)

		processed.append(result)

	return "\n".join(processed)

if __name__ == "__main__":
	pass