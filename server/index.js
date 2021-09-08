const button = document.getElementById('button');
button.addEventListener('click', () => {
  const input = document.getElementById('files');
  putFile(input.files[0]);
})
