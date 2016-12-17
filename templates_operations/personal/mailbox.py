


from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from classes.operations.person_operations import person_operations
from classes.operations.message_operation import message_operations
import time
from flask_login import current_user, login_required
from templates_operations.user import*
from classes.look_up_tables import *




def mailbox_page_config(request):
    sender = person_operations.GetPerson(current_user, current_user.email)[0]
    key = sender
    messageStore=message_operations()
    Messages = messageStore.get_messages_by_id(key)
    peopleStore=person_operations()
    people=peopleStore.GetPersonList()
    person_with_history=messageStore.get_person_with_messaging_background(sender,key)
    if request=="GET":
        return render_template('mailbox/mailbox.html', current_user=current_user,sender=sender,
                               person_with_history=person_with_history,key=key,Messages=Messages,people=people)
    else:
        if "sendMessage" in request.form:
            receiver=request.form['Receiver']
            sender=person_operations.GetPerson(current_user,current_user.email)[0]
            message=request.form['Message']
            messageStore.send_message(sender,5,message)
        return render_template('mailbox/mailbox.html',key=key, person_with_history=person_with_history,sender=sender,current_user=current_user,Messages=Messages,people=people )




def messages_page_with_key_config(request, key):
    messageStore = message_operations()
    Messages = messageStore.get_messages()
    peopleStore = person_operations()
    people = peopleStore.GetPersonList()
    receiverPerson=peopleStore.GetPersonByObjectId(key)

    sender = person_operations.GetPerson( current_user,current_user.email)[0]
    senderPerson = peopleStore.GetPersonByObjectId(sender)
    receiver_messages=messageStore.get_messages_by_receiver_id(key)
    sent_messages=messageStore.get_messages_by_sender_id(sender)
    received_messages=messageStore.get_received_messages(sender,key)
    messageStore.set_unread_messages_read(key, sender)
    person_with_history = messageStore.get_person_with_messaging_background(sender,key)


    if request == "GET":
        Messages = messageStore.get_messages()
        return render_template('mailbox/mailbox.html', sent_messages=sent_messages,receiver_messages=receiver_messages,
                               senderPerson=senderPerson, receiverPerson=receiverPerson,person_with_history=person_with_history,
                               sender=sender,key=key,Messages=Messages, people=people)
    else:
        if "sendMessage" in request.form:
            receiver=request.form['sendMessage']
            sender=person_operations.GetPerson(current_user,current_user.email)[0]
            message=request.form['Message']
            messageStore.send_message(sender,receiver,message)
            Messages=messageStore.get_messages()
        elif "deleteMessage" in request.form:
            deleteId=request.form['deleteMessage']
            messageStore.delete_messages(deleteId)
            Messages=messageStore.get_messages()

        return render_template('mailbox/mailbox.html', sent_messages=sent_messages, receiver_messages=receiver_messages,person_with_history=person_with_history,
                               senderPerson=senderPerson,receiverPerson=receiverPerson,sender=sender, key=key, Messages=Messages, people=people)















