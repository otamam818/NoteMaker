# Search for '# Code to insert' in the document and insert 
# whatever transformers you prefer in that section

# Relevant classes
# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
class simple_transformer:
    __transformers = dict()
    def __init__(
        self, 
        entered: str, 
        returned: str, 
        cursor_pos_increment: int = 0):
        """Replaces the entered string with the returned string"""
        simple_transformer.__transformers.update(
            {entered : [returned, cursor_pos_increment]}
        )

    def get_dict() -> dict:
        """Returns a dictionary of all added transformers"""
        return simple_transformer.__transformers

# Code to insert
# ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
TO_DO = simple_transformer(";;[]", "\n[   ]", 3)

if __name__ == "__main__":
    print(simple_transformer.get_dict())

