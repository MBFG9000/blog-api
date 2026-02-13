#Python modules

#Django modules
from django.core.exceptions import ValidationError

#Project modules

_RESTRICTED_DOMAINS = (
    "yahoo.com"
)

def validate_email_domain(value:str) -> None:
    """
    Validate that email address belongs to a specific domain.
    """
    domain:str = value.split("@")[-1]

    if domain in _RESTRICTED_DOMAINS:
        raise ValidationError(
            message=f"Registration using \"{domain}\" is not allowed.",
            code="invalid_domain",
        )
    
def validate_email_payload_not_in_full_name(
        email: str,
        first_name: str,
        last_name: str,) -> None:
    """
    Validate that the email address does not contain the first or last name.
    """
    email_payload: str = email.split("@")[0]
    if email_payload.lower() in (first_name + last_name).lower():
        raise ValidationError(
            {
                "email":"Email address payload should not be part of the first or last name.",
                "first_name":"First name should not contain email address payload.",
                "last_name":"Last name should not contain email address payload.",
            },
            code="invalid_email_first_or_last_name_relation"
        ) 