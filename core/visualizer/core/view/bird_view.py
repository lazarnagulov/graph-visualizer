from typing import Tuple
import os
import sys

def render() -> Tuple[str, str]:
    """
    Returns the required head and body HTML content for the Bird view.
    :return: (bird_view_head, bird_view_body) HTML string that should be included in page.
    """
    with open(os.path.join(sys.prefix, 'templates/bird_view_head_template.html'), 'r', encoding='utf-8') as file:
        bird_view_head = file.read()
    with open(os.path.join(sys.prefix, 'templates/bird_view_body_template.html'), 'r', encoding='utf-8') as file:
        bird_view_body = file.read()

    return bird_view_head, bird_view_body
