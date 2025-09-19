from django import template

register = template.Library()

# List ของพยัญชนะไทยที่เรียงตามลำดับที่ถูกต้องสำหรับการทำข้อสอบ
THAI_CHOICE_CHARS = [
    'ก', 'ข', 'ค', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 
    'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 
    'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 
    'ย', 'ร', 'ล', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ'
]

@register.filter(name='int_to_char')
def int_to_char(value):
    """
    Converts an integer to its corresponding character based on its Unicode value.
    This is primarily used for generating English alphabet choices (A, B, C...).
    Example: {{ 65|int_to_char }} -> 'A'
    """
    try:
        return chr(int(value))
    except (ValueError, TypeError):
        return ''

@register.filter(name='thai_choice_char')
def thai_choice_char(index):
    """
    Converts a zero-based index (0, 1, 2...) to a Thai character choice 
    from a predefined list (ก, ข, ค...).
    This ensures correct alphabetical ordering for Thai choices.
    Example: {{ 0|thai_choice_char }} -> 'ก'
             {{ 4|thai_choice_char }} -> 'จ'
    """
    try:
        index = int(index)
        if 0 <= index < len(THAI_CHOICE_CHARS):
            return THAI_CHOICE_CHARS[index]
        return '?' # Return '?' if the index is out of the list's bounds
    except (ValueError, TypeError):
        return ''