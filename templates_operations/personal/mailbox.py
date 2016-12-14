


from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
import time




key=1


def mailbox_page_config(request, key):
    return render_template('personal/mailbox.html',key=key )


