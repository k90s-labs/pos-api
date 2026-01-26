import re

from django.db.models import F
from .models import Member


# Utility function to generate a new unique member ID with a given prefix
def generate_member_id(prefix: str, width: int = 4) -> str:
    
    if not prefix:
        raise ValueError("prefix is required")

    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")

    existing_ids = (
        Member.objects
        .filter(member_id__startswith=prefix)
        .values_list("member_id", flat=True)
    )

    max_num = 0
    for member_id in existing_ids:
        match = pattern.match(member_id)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    next_num = max_num + 1
    return f"{prefix}{next_num:0{width}d}"