function mobileCheck() {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) return true;
    return false;
};

function macOsCheck() {
  if (navigator.userAgent.toUpperCase().indexOf('MAC')>=0) return true;
  return false;
}

if (window.location.href.indexOf("wybierz-grupe") > -1) {
  const groupForm = document.querySelector('main#choose form');
  const formButton = document.querySelector('div.form-field:last-child');
  
  if (!mobileCheck()) {
    let note = document.createElement('p');
    note.classList.add('note');
    if(!macOsCheck()){
      note.innerHTML = 'Aby wybrać więcej niż jedną grupę należy <span class="bold">przytrzymać</span> klawisz <span class="bold">ctrl</span> podczas wybierania.';
    } else {
      note.innerHTML = 'Aby wybrać więcej niż jedną grupę należy <span class="bold">przytrzymać</span> klawisz <span class="bold">command</span> podczas wybierania.';
    }
    groupForm.insertBefore(note, formButton);
  }
}