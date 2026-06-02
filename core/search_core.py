
from config import FUZZY_TYPO_TOLERANCE, FUZZY_MIN_WORD_LENGTH, EDUCATION_LEVELS
from core.synonyms_core import SYNONYMS


class SearchEngine:
    """Handles keyword, filter, fuzzy, and combined search across job and candidate data."""

    EDUCATION_RANK = {level: rank for rank, level in enumerate(EDUCATION_LEVELS)}

    def keyword_search(self, query, items, fields):
        """Returns items where query is a substring of any specified field. Case-insensitive."""
        query_lower = query.strip().lower()
        if not query_lower:
            return items
        results = []
        for item in items:
            for field in fields:
                value = item.get(field) or ""
                if query_lower in value.lower():
                    results.append(item)
                    break
        return results

    def filter_search(self, items, filters):
        """Returns items matching all provided filters. Empty/None filter values are ignored."""
        results = []
        for item in items:
            if self._matches_filters(item, filters):
                results.append(item)
        return results

    def fuzzy_search(self, query, items, fields):
        """Returns items matching query via typo tolerance or synonym expansion. Case-insensitive."""
        query_lower = query.strip().lower()
        if not query_lower:
            return []

        expanded_terms = self._expand_query(query_lower)
        results = []

        for item in items:
            if self._matches_fuzzy(expanded_terms, item, fields):
                results.append(item)

        return results

    def combined_search(self, query, items, fields, filters):
        """Runs keyword search, expands with fuzzy matches, deduplicates, then applies filters."""
        query_lower = query.strip().lower()

        if not query_lower:
            matched = items
        else:
            keyword_results = self.keyword_search(query_lower, items, fields)
            fuzzy_results = self.fuzzy_search(query_lower, items, fields)

            # Merge and deduplicate by job id — keyword results first
            seen_ids = set()
            matched = []
            for item in keyword_results + fuzzy_results:
                item_id = item.get("id")
                if item_id not in seen_ids:
                    seen_ids.add(item_id)
                    matched.append(item)

        active_filters = {k: v for k, v in filters.items() if v is not None}
        if active_filters:
            matched = self.filter_search(matched, filters)

        return matched

    def _expand_query(self, query):
        """Returns a set of terms to match against — original query plus any synonym expansions."""
        terms = {query}
        if query in SYNONYMS:
            terms.update(SYNONYMS[query])
        # Also check word-level synonyms for multi-word queries
        for word in query.split():
            if word in SYNONYMS:
                terms.update(SYNONYMS[word])
        return terms

    def _matches_fuzzy(self, expanded_terms, item, fields):
        """Returns True if any expanded term matches any field via substring or typo tolerance."""
        for field in fields:
            field_value = (item.get(field) or "").lower()
            field_words = field_value.split()
            for term in expanded_terms:
                # Substring match for synonym expansions
                if term in field_value:
                    return True
                # Typo tolerance — compare term against each word in the field
                if len(term) >= FUZZY_MIN_WORD_LENGTH:
                    for word in field_words:
                        if len(word) >= FUZZY_MIN_WORD_LENGTH:
                            if self._edit_distance(term, word) <= FUZZY_TYPO_TOLERANCE:
                                return True
        return False

    def _edit_distance(self, a, b):
        """Returns the Levenshtein edit distance between two strings."""
        rows = len(a) + 1
        cols = len(b) + 1
        matrix = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            matrix[i][0] = i
        for j in range(cols):
            matrix[0][j] = j

        for i in range(1, rows):
            for j in range(1, cols):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,       # deletion
                    matrix[i][j - 1] + 1,       # insertion
                    matrix[i - 1][j - 1] + cost # substitution
                )

        return matrix[-1][-1]

    def _matches_filters(self, item, filters):
        """Returns True if item satisfies all active filters."""
        work_mode = filters.get("work_mode")
        if work_mode:
            if item.get("work_mode") != work_mode:
                return False

        education = filters.get("education")
        if education:
            item_education = item.get("required_education")
            if item_education is None:
                return False
            selected_rank = self.EDUCATION_RANK.get(education, -1)
            required_rank = self.EDUCATION_RANK.get(item_education, -1)
            if required_rank > selected_rank:
                return False

        experience = filters.get("experience")
        if experience is not None:
            item_exp = item.get("years_experience_required")
            if item_exp is None or item_exp < experience:
                return False

        location = filters.get("location")
        if location:
            item_location = item.get("location") or ""
            if location.lower() not in item_location.lower():
                return False

        skill = filters.get("skill")
        if skill:
            item_skills = item.get("required_skills") or ""
            skill_list = [s.strip().lower() for s in item_skills.split(",")]
            if skill.lower() not in skill_list:
                return False

        return True