import random

from src.entities.feedback import Feedback, FeedbackType
from src.entities.user import User
from tests.mocks import user_mock, generic_entity_mock


def get_valid_feedback(description: str = None, ftype: FeedbackType = FeedbackType.POSITIVE,
                       user_from: User = user_mock.get_valid_user(), user_to: User = user_mock.get_valid_user(),
                       delivered: bool = True, **kwargs) -> Feedback:
    feedback = object.__new__(Feedback)
    if not kwargs.get("name"):
        kwargs["name"] = generic_entity_mock.random_str("Feedback")

    generic_entity_mock.fill_valid_entity(feedback)
    feedback.delivered = delivered
    feedback.user_from = user_from
    feedback.user_to = user_to
    feedback.type = ftype
    feedback.description = description
    return feedback


def get_default_feedback() -> Feedback:
    feedback = object.__new__(Feedback)
    generic_entity_mock.fill_default_entity(feedback, name="Feedback 1")
    feedback.delivered = True
    feedback.user_from = user_mock.get_default_user()
    feedback.user_to = user_mock.get_default_user()
    feedback.description = "Description 1"
    feedback.type = FeedbackType.POSITIVE
    return feedback
