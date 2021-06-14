document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // get user input
  const submit = document.querySelector('input[type="submit"]');
  const mailRecipient = document.querySelector('#compose-recipients');
  submit.disabled = true;

  mailRecipient.onkeyup = () => {
    if (mailRecipient.value.length > 0) {
        submit.disabled = false;
    }
    else {
        submit.disabled = true;
    }
  }

  document.querySelector('form').onsubmit = () => {
    const recipients = mailRecipient.value.split(',');
    const subject = document.querySelector('#compose-subject');
    const body = document.querySelector('#compose-body');

    recipients.forEach(recipient => {
      try {
        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
              recipients: recipient,
              subject: subject,
              body: body
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        })
      } catch (error){
          console.log(error)
        }
        
    })
    submit.disabled = true;
    load_mailbox('sent')
    return false;
  }

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}