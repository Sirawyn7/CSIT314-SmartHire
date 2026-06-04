
from datetime import datetime, timedelta
import calendar
from config import MAX_RECOMMENDATIONS, MEMBERSHIP_GRACE_PERIOD_DAYS, MEMBERSHIP_PRICE_CANDIDATE, MEMBERSHIP_PRICE_EMPLOYER


class MembershipManager:
    """Handles membership status checks, billing date calculations, and payment processing."""

    def __init__(self, db):
        self.db = db

    def get_recommendation_limit(self, user_id):
        """Returns None for members (unlimited) or MAX_RECOMMENDATIONS for non-members."""
        user = self.db.users.get_by_user_id(user_id)
        return None if user["is_member"] else MAX_RECOMMENDATIONS

    def is_member(self, user_id):
        """Returns True if the user currently has an active membership."""
        user = self.db.users.get_by_user_id(user_id)
        return bool(user["is_member"])

    def get_membership_price(self, user_id):
        """Returns the membership price for the user's account type."""
        user = self.db.users.get_by_user_id(user_id)
        if user["user_type"] == "candidate":
            return MEMBERSHIP_PRICE_CANDIDATE
        return MEMBERSHIP_PRICE_EMPLOYER

    def get_billing_day(self, user_id):
        """Returns the day-of-month the user is billed on, derived from membership started_at."""
        membership = self.db.memberships.get_by_user_id(user_id)
        if not membership:
            return None
        started_at = datetime.strptime(membership["started_at"], "%Y-%m-%d %H:%M:%S")
        return started_at.day

    def get_next_due_date(self, user_id):
        """Returns the next payment due date as a datetime for the user's billing day."""
        billing_day = self.get_billing_day(user_id)
        if billing_day is None:
            return None
        today = datetime.now()
        due_date = self._resolve_billing_date(today.year, today.month, billing_day)
        if due_date < today:
            year, month = self._next_month(today.year, today.month)
            due_date = self._resolve_billing_date(year, month, billing_day)
        return due_date

    def get_grace_deadline(self, user_id):
        """Returns the last datetime a user can pay before their membership lapses."""
        due_date = self.get_next_due_date(user_id)
        if due_date is None:
            return None
        return due_date + timedelta(days=MEMBERSHIP_GRACE_PERIOD_DAYS)

    def get_current_period(self, user_id):
        """Returns the current billing period as a YYYY-MM string."""
        billing_day = self.get_billing_day(user_id)
        if billing_day is None:
            return None
        today = datetime.now()
        due_date = self._resolve_billing_date(today.year, today.month, billing_day)
        if today < due_date:
            year, month = self._prev_month(today.year, today.month)
            return f"{year}-{month:02d}"
        return f"{today.year}-{today.month:02d}"

    def is_payment_overdue(self, user_id):
        """Returns True if the current period is unpaid and the grace deadline has passed."""
        period = self.get_current_period(user_id)
        if period is None:
            return False
        payment = self.db.payments.get_by_user_and_period(user_id, period)
        if payment:
            return False
        grace_deadline = self.get_grace_deadline(user_id)
        return datetime.now() > grace_deadline

    def is_current_period_paid(self, user_id):
        """Returns True if the user has already paid for the current billing period."""
        period = self.get_current_period(user_id)
        if period is None:
            return False
        payment = self.db.payments.get_by_user_and_period(user_id, period)
        return payment is not None

    def process_payment(self, user_id):
        """
        Records a payment for the current period and ensures the user is marked as a member.
        Inserts a new membership row if the user is not currently a member (rejoining flow).
        Returns the inserted payment id.
        """
        user = self.db.users.get_by_user_id(user_id)
        if not user["is_member"]:
            self.db.memberships.insert(user_id)
            self.db.users.set_member_status(user_id, 1)

        period = self.get_current_period(user_id)
        amount = self.get_membership_price(user_id)
        payment_id = self.db.payments.insert(user_id, amount, period)
        return payment_id

    def lapse_overdue_memberships(self):
        """
        Checks all active members and sets is_member to 0 for any whose grace period
        has expired without payment. Intended to be called by the overnight scheduled job.
        """
        memberships = self.db.memberships.get_all()
        for membership in memberships:
            user_id = membership["user_id"]
            user = self.db.users.get_by_user_id(user_id)
            if not user["is_member"]:
                continue
            if self.is_payment_overdue(user_id):
                self.db.users.set_member_status(user_id, 0)

    def get_membership_context(self, user_id):
        """
        Returns a dict of membership display data for use in templates.
        Includes next due date, grace deadline, current period paid status, and price.
        Returns None if the user has no membership record.
        """
        if not self.db.memberships.get_by_user_id(user_id):
            return None
        next_due = self.get_next_due_date(user_id)
        grace_deadline = self.get_grace_deadline(user_id)
        return {
            "next_due_date": next_due.strftime("%d %B %Y"),
            "grace_deadline": grace_deadline.strftime("%d %B %Y"),
            "is_current_period_paid": self.is_current_period_paid(user_id),
            "is_payment_overdue": self.is_payment_overdue(user_id),
            "price": self.get_membership_price(user_id),
        }

    def _resolve_billing_date(self, year, month, billing_day):
        """Returns a datetime for the given year/month, clamping to the last day if needed."""
        last_day = calendar.monthrange(year, month)[1]
        day = min(billing_day, last_day)
        return datetime(year, month, day)

    def _next_month(self, year, month):
        """Returns the (year, month) tuple for the month after the given one."""
        if month == 12:
            return year + 1, 1
        return year, month + 1

    def _prev_month(self, year, month):
        """Returns the (year, month) tuple for the month before the given one."""
        if month == 1:
            return year - 1, 12
        return year, month - 1