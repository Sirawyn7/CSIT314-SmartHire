
from config import EDUCATION_LEVELS


class SearchEngine:
    """Handles keyword, filter, fuzzy, and combined search across job and candidate data."""

    #Dict mapping so education requirements will still display lower, e.g. bachelor will show high school
    EDUCATION_RANK = {level: rank for rank, level in enumerate(EDUCATION_LEVELS)}

    def filter_search(self, items, filters):
        """Returns items matching all provided filters. Empty/None filter values are ignored."""
        results = []
        for item in items:
            if self._matches_filters(item, filters):
                results.append(item)
        return results

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