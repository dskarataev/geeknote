# -*- coding: utf-8 -*-

import tempfile
import html2text
import markdown
import tools
import out
import sys
import os
import re
import config


def ENMLtoText(contentENML):
    contentENML = contentENML.decode('utf-8')
    content = html2text.html2text(contentENML)
    return content.encode('utf-8')

def textToENML(content):
    """
    Create an ENML format of note.
    """
    if not isinstance(content, str):
        content = ""
    # try:
    content = re.sub(r'(\r|\n|\r\n)', '  \1', content) # create br tags
    content = unicode(content,"utf-8")
    contentENML = markdown.markdown(content).encode("utf-8")
    # except:
    #     out.failureMessage("Error. Content must be an UTF-8 encode.")
    #     return tools.exit()

    body =  '<?xml version="1.0" encoding="UTF-8"?>\n'
    body += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n'
    body += '<en-note>%s</en-note>' % contentENML
    return body

def edit(content=None):
    """
    Call the system editor, that types as a default in the system.
    Editing goes in markdown format, and then the markdown converts into HTML, before uploading to Evernote.
    """
    if content is None:
        content = ""

    if not isinstance(content, str):
        raise Exception("Note content must be an instanse of string, '%s' given." % type(content))

    (tmpFileHandler, tmpFileName) = tempfile.mkstemp()
    
    os.write(tmpFileHandler, ENMLtoText(content))
    os.close(tmpFileHandler)
    
    # Try to find default editor in the system.
    editor = os.environ.get("editor")
    if not (editor):
        editor = os.environ.get("EDITOR")
    if not (editor):
        # If default editor is not finded, then use nano as a default.
        if sys.platform == 'win32':
            editor = config.DEF_WIN_EDITOR
        else:
            editor = config.DEF_UNIX_EDITOR

    # Make a system call to open file for editing.
    os.system(editor + " " + tmpFileName)

    newContent =  open(tmpFileName, 'r').read()

    return newContent