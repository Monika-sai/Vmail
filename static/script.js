const Password = document.querySelector("#password");
const Checkbox = document.querySelector("#show");
Checkbox.addEventListener('click',function(){
  const type =Password.getAttribute("type")=== "password" ? "text" : "password";
  Password.setAttribute("type",type);
});
