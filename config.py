

#This would be stored in .env in a prod setting
SECRET_KEY = "VgYV7NbZyTjY"

#Number of listings per page for pagination
JOBS_PER_PAGE = 10

#Search
WORK_MODES = ("Remote", "On-site", "Hybrid")
EDUCATION_LEVELS = ("High School", "Bachelor", "Master", "PhD")
#Search - defines what fields keyword search compares against
JOB_KEYWORD_FIELDS = ("title", "description", "location", "required_skills")

#Fuzzy search
FUZZY_TYPO_TOLERANCE = 3
FUZZY_MIN_WORD_LENGTH = 3

#Matcher scoring weights - must sum to 1.0
SKILL_WEIGHT       = 0.40
EXPERIENCE_WEIGHT  = 0.20
EDUCATION_WEIGHT   = 0.15
WORK_MODE_WEIGHT   = 0.15
LOCATION_WEIGHT    = 0.10


#Max number of recommendations returned to non-member users
MAX_RECOMMENDATIONS = 10

#Membership
MEMBERSHIP_PRICE_CANDIDATE = 10.00
MEMBERSHIP_PRICE_EMPLOYER = 30.00
MEMBERSHIP_GRACE_PERIOD_DAYS = 7
MEMBERSHIP_CHECK_HOUR = 3 #Represents 3am, the time for membership statuses to be checked