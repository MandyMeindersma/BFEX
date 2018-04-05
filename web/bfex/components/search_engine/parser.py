from .stack import Stack
from bfex.common.utils import TextNormalizer

# Operator precedence for parsing
precedence = {
    "AND": 2,
    "OR": 2,
    "(": 1,
    ")": 1
}

bool_values = ['AND', 'OR']
operators = ['AND', 'OR', ')', '(']

invalid_prev_terms = {
    'bool': ['AND', 'OR', '('],
    'term': [')'],
    ')': ['(', 'AND', 'OR'],
    '(': [')']
}


class QueryParser(object):
    """Manages parsing boolean query strings, and converting them to a postfix list."""

    def _normalize_query(self, query):
        """Normalizes the braces in the query to be padded with spaces. Allows easy splitting of the query."""
        query = query.replace('(', ' ( ')
        normalized = query.replace(')', ' ) ')

        return normalized

    def _validate_query(self, query):
        """Validates the order and overall construction of the query

        :exception: QueryException if the query is not a valid boolean query."""

        if query.count('(') != query.count(')'):
            raise QueryException('Parentheses dont match')

        if query[0] in ['AND', 'OR', ')']:
            raise QueryException('Invalid First Term')

        i = 1
        while i < len(query):
            if type(query[i]) == tuple:
                if query[i-1] in invalid_prev_terms['term'] or type(query[i-1]) is tuple:
                    raise QueryException('Term has invalid previous')

            if query[i] in bool_values:
                if query[i-1] in invalid_prev_terms['bool']:
                    raise QueryException('Bool has invalid previous')

            if query[i] is ')':
                if query[i-1] in invalid_prev_terms[')']:
                    raise QueryException(') has invalid previous')

            if query[i] is '(':
                if query[i-1] in invalid_prev_terms['('] or type(query[i-1]) is tuple:
                    raise QueryException('( has invalid previous')

            i += 1

    def _make_query(self, q_list):
        """Constructs a new list with valid types of query parameters.

        Valid types include PHRASE, KEYWORD, or operators

        :param q_list: Query split on spaces into a list.
        """
        good_query = []
        i = 0
        while i < len(q_list):
            if '"' in q_list[i]:
                phrase_string = q_list[i]
                if phrase_string.count('"') == 2:
                    good_query.append(('PHRASE', phrase_string))
                else:
                    i += 1
                    while '"' not in q_list[i]:
                        if q_list[i] in operators:
                            raise QueryException('Brackets or bools in phrase query')
                        phrase_string = phrase_string + " " + q_list[i]
                        i += 1
                    phrase_string = phrase_string + " " + q_list[i]
                    phrase_string = phrase_string[1:-1]
                    good_query.append(('PHRASE', phrase_string))

            elif q_list[i] in operators:
                good_query.append((q_list[i]))

            else:
                good_query.append(('KEYWORD', q_list[i]))
            i += 1
        return good_query

    def _order_of_operations(self, good_query):
        """Creates a postfix ordered list with correct order of operations, as determined by operator precedence.

        :param good_query: A validated list of tuples (keywords, phrase) or operators.
        :return: A postfix ordered list of keywords, phrases and operators, not including braces.
        :href: http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
        """
        q_stack = Stack()
        result_list = []
        for token in good_query:
            if token in bool_values:
                while (not q_stack.is_empty()) and (precedence[q_stack.peek()] >= precedence[token]):
                    result_list.append(q_stack.pop())
                q_stack.push(token)
            elif token == '(':
                q_stack.push(token)
            elif token == ')':
                top_token = q_stack.pop()
                while top_token != '(':
                    result_list.append(top_token)
                    top_token = q_stack.pop()
            elif token[0] == 'KEYWORD':
                # Do we want to apply stemming to keywords? Could give us better search results.
                stemmed_token = TextNormalizer.tokenize(token[1])[0]
                result_list.append(('KEYWORD', stemmed_token))
            else:
                stemmed_token = TextNormalizer.tokenize(token[1])
                result_list.append(('PHRASE', stemmed_token))

        while not q_stack.is_empty():
            result_list.append(q_stack.pop())
        return result_list

    def parse_query(self, query):
        """Splits query on whitespace, calls funtions to make, validate and list operations in correct order.

        :param string query: Boolean query as a string. Phrases are expected to be wrapped in double quotes.
        :return: A postfix ordered list that represents the query."""
        norm_query = self._normalize_query(query)

        q_list = norm_query.split()

        query = self._make_query(q_list)
        self._validate_query(query)
        return self._order_of_operations(query)


class QueryException(Exception):
    def __init__(self, message):
        super().__init__(message)