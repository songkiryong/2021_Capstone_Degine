const button = document.getElementById('button');
button.addEventListener('click', () => {
  const input = document.getElementById('pill_file');
  putFile(input.pill_file[0]);
})
