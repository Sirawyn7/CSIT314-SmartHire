
from flask import Blueprint, render_template, redirect, url_for, session
from core.membership_core import MembershipManager

class MembershipRoutes:
    """Handles membership payment and status routes."""

    def __init__(self, db):
        self.db = db
        self.blueprint = Blueprint("membership", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/membership/pay", view_func=self.pay_page, methods=["GET"])
        self.blueprint.add_url_rule("/membership/pay", view_func=self.pay_post, methods=["POST"])
        self.blueprint.add_url_rule("/membership/confirmation", view_func=self.confirmation_page, methods=["GET"])

    def pay_page(self):
        """Renders the membership payment page."""
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))

        user_id = session["user_id"]
        manager = MembershipManager(self.db)
        context = manager.get_membership_context(user_id)
        price = manager.get_membership_price(user_id)

        return render_template("membership/pay.html",
            membership=context,
            price=price,
            is_member=manager.is_member(user_id)
        )

    def pay_post(self):
        """Processes a pseudo-payment for the current billing period."""
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))

        user_id = session["user_id"]
        manager = MembershipManager(self.db)
        manager.process_payment(user_id)

        return redirect(url_for("membership.confirmation_page"))

    def confirmation_page(self):
        """Renders the payment confirmation page."""
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))

        user_id = session["user_id"]
        manager = MembershipManager(self.db)
        context = manager.get_membership_context(user_id)

        return render_template("membership/confirmation.html",
            membership=context
        )