document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function prepopulateForm(email) {
  const mailRecipient = document.querySelector('#compose-recipients');
  const mailSubject = document.querySelector('#compose-subject');
  const mailBody = document.querySelector('#compose-body');
  mailRecipient.value = email.sender;
  const regex = new RegExp('^Re:.*');
  if (!regex.test(email.subject)) {
    mailSubject.value = `Re: ${email.subject}`;
  } else{
    mailSubject.value = email.subject;
  }
  mailBody.value = 
    `---------------------------
On ${email.timestamp} ${email.sender} wrote:

${email.body}
----------------------------`;
  return false;
}

function compose_email(email={}) {

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#detail-view').style.display = 'none';

  // get user input
  const mailRecipient = document.querySelector('#compose-recipients');
  const submit = document.querySelector('input[type="submit"]');
  if(email.sender) {
    prepopulateForm(email);
  } else {
    submit.disabled = true;
  }
  if (mailRecipient.value.length > 0) {
    submit.disabled = false;
  }

  mailRecipient.onkeyup = () => {
    if (mailRecipient.value.length > 0) {
        submit.disabled = false;
    }
    else {
        submit.disabled = true;
    }
  }

  document.querySelector('form').onsubmit = () => {
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    try {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: mailRecipient.value,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
      .then(
        () => load_mailbox('sent')
      )
    } catch (error){
        console.log(error)
      }
    submit.disabled = true;
    return false;
  }

  return false;
}


//toggle archived of an email
function toggleArchive(email){  
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })
  .then(
    () => load_mailbox('inbox')
  )
  return false;
}


//load single view of an email
function load_detail(email, mailbox){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'block';
  document.querySelector('#detail-view').innerHTML = '';

  //fetch the data
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {

      // show single email
      const detail = document.getElementById('detail-view');
      const ul = document.createElement('ul');
      ul.style.listStyleType = 'none';
      const sender_li = document.createElement("li");
      sender_li.innerHTML = `<b>FROM:</b>  ${email.sender}`;
      const recipients_li = document.createElement("li");
      let recipients = "";
      email.recipients.forEach( recipient => {
        recipients += `${recipient} <br/>`;
      })
      recipients_li.innerHTML = `<b>TO: </b> ${recipients}`;
      const subject_li = document.createElement("li");
      subject_li.innerHTML = `<b>Subject:</b>  ${email.subject}`;
      const timestamp_li = document.createElement("li");
      timestamp_li.innerHTML = `<b>Timestamp:</b>  ${email.timestamp}`;
      ul.appendChild(sender_li);
      ul.appendChild(recipients_li);
      ul.appendChild(subject_li);
      ul.appendChild(timestamp_li);
      detail.appendChild(ul);
      const hr = document.createElement("hr");
      if (mailbox !== 'sent'){
        const archive = document.createElement("button");
        archive.type = "button";
        archive.classList.add('btn', 'btn-outline-info');
        if (email.archived) {
          archive.textContent = 'Unarchive';
        } else {
          archive.textContent = 'Archive';
        }
        archive.addEventListener('click', () => toggleArchive(email))
        detail.appendChild(archive);
        const reply = document.createElement("button");
        reply.style.marginLeft = '10px';
        reply.type = "button";
        reply.classList.add('btn', 'btn-outline-info');
        reply.textContent = 'Reply';
        reply.addEventListener('click', () => compose_email(email))
        detail.appendChild(reply);
      }
      detail.appendChild(hr);
      const body = document.createElement("div");
      body.style.whiteSpace = 'pre-wrap';
      const body_text = document.createTextNode(email.body);
      body.appendChild(body_text);
      detail.appendChild(body);
  });
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  


  //document.querySelector('#detail-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_mailbox(mailbox) {

  // Show the details and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = '';

  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    //list emails in table
    let specs = {};
    if (mailbox !== 'sent'){
      specs = {0: 'sender', 1: 'subject', 2: 'timestamp'}
    } else {
      specs = {0: 'recipients', 1: 'subject', 2: 'timestamp'}
    }
    const emails_list = document.getElementById('emails-view');
    const table = document.createElement('table');
    table.classList.add('table');
    const tblBody = document.createElement("tbody");
    emails.forEach(email =>{
      const row = document.createElement("tr");
      row.setAttribute('id', email.id);
      //iterate over specs
      for (const value of Object.entries(specs)){
        const cell = document.createElement("td");
        const cellText = document.createTextNode(email[value[1]]);
        cell.appendChild(cellText);
        row.appendChild(cell);
        if(email.read){
          row.style.backgroundColor = "#f2f2f2";
        }
      }
      row.addEventListener('click', () => load_detail(email, mailbox));
      tblBody.appendChild(row);
    });
        
    // put the <tbody> in the <table>
    table.appendChild(tblBody);
    // appends <table> into <body>
    emails_list.appendChild(table);
});

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}