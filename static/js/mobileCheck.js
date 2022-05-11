function mobileCheck() {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) return true;
    return false;
};


{/* <p class="note">
            Aby wybrać więcej niż jedną grupę należy <span class="bold">przytrzymać</span> klawisz <span class="bold">ctrl</span> podczas wybierania.
        </p> */}
const groupForm = document.querySelector('main#choose form');
const formButton = document.querySelector('div.form-field:last-child');

if (!mobileCheck()) {
  let note = document.createElement('p');
  note.classList.add('note');
  note.innerHTML = 'Aby wybrać więcej niż jedną grupę należy <span class="bold">przytrzymać</span> klawisz <span class="bold">ctrl</span> podczas wybierania.';
  groupForm.insertBefore(note, formButton);
}