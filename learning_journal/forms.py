from wtforms import Form, TextField, TextAreaField, validators

strip_filter = lambda x: x.strip() if x else None


class EntryCreateForm(Form):

    title = TextField(
        'Entry Title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter],
    )
    body = TextAreaField(
        'Entry Body',
        [validators.Length(min=1)],
        filters=[strip_filter],
    )
