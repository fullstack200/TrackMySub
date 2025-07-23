from models.user import User
from models.usage import Usage

class Advisory:
    """
    Represents an advisory entity that analyzes a user's subscription usage and provides advice.
    Attributes:
        user (User): The user associated with this advisory. Must be an instance of the User class.
        usage (Usage): The usage data associated with this advisory. Must be an instance of the Usage class.
    Methods:
        generate_advice():
            Generates personalized advice for the user based on analysis and comparison.
    """
    def __init__(self, user, usage):
        self.user = user
        self.usage = usage
        
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        if isinstance(user, User):
            self._user = user
        else:
            raise ValueError("Not a valid user")
        
    @property
    def usage(self):
        return self._usage
    
    @usage.setter
    def usage(self, usage):
        if isinstance(usage, Usage):
            self._usage = usage
        else:
            raise ValueError("Invalid usage object")
        
    def generate_advice(self):
        usage = self.usage
        sub = usage.subscription

        # --- Normalize usage data to 10-point scale ---
        usage_score = min(usage.times_used_per_month, 30) / 30 * 10
        duration_score = min(usage.session_duration_hours, 5.0) / 5.0 * 10
        benefit_score = usage.benefit_rating / 5 * 10

        # --- Define category-specific weights ---
        def get_category_weights(category):
            category = category.strip().lower()
            if category in {"entertainment", "music", "video"}:
                return {"usage": 0.4, "duration": 0.3, "benefit": 0.3}, "Entertainment"
            elif category in {"technology", "cloud services", "productivity"}:
                return {"usage": 0.3, "duration": 0.4, "benefit": 0.3}, "Technology"
            elif category in {"shopping", "grocery", "membership", "delivery"}:
                return {"usage": 0.5, "duration": 0.1, "benefit": 0.4}, "Shopping/Membership"
            elif category in {"tools", "utility", "writing", "design"}:
                return {"usage": 0.3, "duration": 0.3, "benefit": 0.4}, "Utility/Tools"
            else:
                return {"usage": 0.33, "duration": 0.33, "benefit": 0.34}, "General"

        weights, category_type = get_category_weights(sub.category)

        # --- Calculate final score based on weights ---
        final_score = (
            usage_score * weights["usage"]
            + duration_score * weights["duration"]
            + benefit_score * weights["benefit"]
        )

        # --- Apply plan penalty ---
        plan_penalty_map = {"basic": 0, "standard": 1, "premium": 2}
        plan_type = sub.plan_type.strip().lower()
        plan_penalty = plan_penalty_map.get(plan_type, 0)
        final_score -= plan_penalty

        # --- Optional penalty for expensive plans ---
        if sub.subscription_price > 999:
            final_score -= 0.5

        final_score = max(0, min(final_score, 10))  # Clamp to 0–10

        # --- Generate recommendation ---
        if final_score >= 7:
            recommendation = "✅ Continue using the current plan."
        else:
            recommendation = "📉 Consider downgrading to a lower plan."

        # --- Return full detailed advice ---
        return (
            f"📄 **Subscription Advisory Report**\n"
            f"- Service: {sub.service_name} ({sub.plan_type} Plan)\n"
            f"- Category: {sub.category} ({category_type})\n"
            f"- Price: ${sub.subscription_price:.2f} per {sub.billing_frequency.lower()}\n"
            f"\n📊 **Usage Overview**\n"
            f"- Times used per month: {usage.times_used_per_month}\n"
            f"- Avg. session duration: {usage.session_duration_hours} hours\n"
            f"- Benefit rating: {usage.benefit_rating}/5\n"
            f"\n🧠 **Score Breakdown**\n"
            f"- Usage score: {usage_score:.2f}/10\n"
            f"- Duration score: {duration_score:.2f}/10\n"
            f"- Benefit score: {benefit_score:.2f}/10\n"
            f"- Plan penalty: -{plan_penalty}\n"
            f"- Final score: {final_score:.2f}/10\n"
            f"\n{recommendation}"
        )


