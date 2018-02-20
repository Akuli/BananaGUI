from bananagui import widgets, widgettree


asciitemplate = """\
{window}
`-- {bigbox}
    |-- {labelbox}
    |   |-- {label1}
    |   |-- {label2}
    |   `-- {label3}
    `-- {button}
"""
unicodetemplate = (asciitemplate
                   .replace('`-- ', '└── ')
                   .replace('|-- ', '├── ')
                   .replace('|   ', '│   '))


def test_dumping(dummywrapper, capsys):
    window = widgets.Window("Test window")
    bigbox = widgets.Box()
    window.add(bigbox)
    labelbox = widgets.Box()
    bigbox.append(labelbox)
    for i in (1, 2, 3):
        labelbox.append(widgets.Label("Label %d" % i))
    button = widgets.Button()
    bigbox.append(button)

    widgetlist = [
        ('window', window),
        ('bigbox', bigbox),
        ('labelbox', labelbox),
        ('label1', labelbox[0]),
        ('label2', labelbox[1]),
        ('label3', labelbox[2]),
        ('button', button),
    ]
    asciiformat = {
        name: widgettree._clean_repr(widget, ascii_only=True)
        for name, widget in widgetlist}
    unicodeformat = {
        name: widgettree._clean_repr(widget, ascii_only=False)
        for name, widget in widgetlist}
    asciiresult = asciitemplate.format(**asciiformat)
    unicoderesult = unicodetemplate.format(**unicodeformat)
    assert widgettree.dumps(window) == unicoderesult
    assert widgettree.dumps(window, ascii_only=True) == asciiresult
    assert capsys.readouterr() == ('', '')  # check if it leaks to stdout
    widgettree.dump(window)
    assert capsys.readouterr() == (unicoderesult, '')
