/* Форма записи «Диамедика»: валидация и подготовка письма без backend. */
(function () {
  'use strict';
  var form = document.getElementById('appointment-form');
  if (!form) return;
  var error = document.getElementById('form-error');
  var success = document.getElementById('form-success');
  var nameField = form.querySelector('[name="name"]');
  var phoneField = form.querySelector('[name="phone"]');
  var messageField = form.querySelector('[name="message"]');
  var consentField = form.querySelector('[name="consent"]');

  function digits(value) {
    return value.replace(/\D/g, '');
  }

  function validPhone(value) {
    var d = digits(value);
    return d.length >= 10 && d.length <= 12;
  }

  function setInvalid(field, invalid) {
    if (!field) return;
    field.setAttribute('aria-invalid', invalid ? 'true' : 'false');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (error) error.hidden = true;
    if (success) success.hidden = true;
    setInvalid(nameField, false);
    setInvalid(phoneField, false);
    setInvalid(consentField, false);

    var nameOk = nameField.value.trim().length > 1;
    var phoneOk = validPhone(phoneField.value);
    var consentOk = consentField.checked;

    setInvalid(nameField, !nameOk);
    setInvalid(phoneField, !phoneOk);
    setInvalid(consentField, !consentOk);

    if (!nameOk || !phoneOk || !consentOk) {
      if (error) error.hidden = false;
      if (!nameOk) nameField.focus();
      else if (!phoneOk) phoneField.focus();
      else consentField.focus();
      return;
    }

    var subject = 'Заявка на консультацию — Диамедика';
    var body = 'Имя: ' + nameField.value.trim() +
      '\nТелефон: ' + phoneField.value.trim() +
      '\nКомментарий: ' + (messageField && messageField.value.trim() ? messageField.value.trim() : '—');
    var mailto = 'mailto:uk.klinika@mail.ru?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);

    var link = document.createElement('a');
    link.href = mailto;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    link.remove();

    if (success) {
      success.innerHTML = 'Открываем почтовый клиент для отправки заявки. ' +
        'Если он не открылся — позвоните <a href="tel:+78432041961">+7 (843) 204-19-61</a>.';
      success.hidden = false;
    }
    form.reset();
  });
})();
