const loginsignupbtn = document.getElementById
let modal = document.getElementById("myModal");

const login_selector = document.getElementById("login-selector");
const signup_selector = document.getElementById("signup-selector");
let credentials = document.getElementById("credentials");

let loc_selector = document.getElementById("loc-selector");
const ok_btn = document.getElementById("ok-btn");

let current_loc = document.getElementById("currentloc");
let seleced_location = localStorage.getItem('selectedLocation'); 

let location_values = document.getElementsByClassName('location-values')
let services_offered = document.getElementById('services-offered')

let stars = document.getElementsByClassName('star')
const ratings = document.getElementById('ratings-number')

const ininvalidMsg = document.getElementById("invalid-msg")


function loginSign(){
  modal.style.display = "block";
}



// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

signup_selector.addEventListener('click', ()=>{
  login_selector.classList.remove('active-btn')
  login_selector.classList.add('inactive-btn')

  signup_selector.classList.remove('inactive-btn')
  signup_selector.classList.add('active-btn')

  credentials.innerHTML = `
    <form action="/signup" method="POST" enctype="multipart/form-data">
    <div class="sign-login-content">
        <input type="text" placeholder="Username" name="username" class="credential-data" required>
        <br>
        <input type="text" placeholder="Your fullnames" name="fullname" class="credential-data" required>
        <br>
        <input type="email" placeholder="Email" name="email" class="credential-data" required>
        <br>
        <input type="password" placeholder="Password" name="password" class="credential-data" required>
        <br>
        <input type="password" placeholder="Password Again" name="password-again" class="credential-data" required>
        <br>
        <button type="submit" class="credentials-btn">SIGN UP</button>
    </div>
  </form>
`

})

login_selector.addEventListener('click', ()=>{
  signup_selector.classList.remove('active-btn')
  signup_selector.classList.add('inactive-btn')

  login_selector.classList.remove('inactive-btn')
  login_selector.classList.add('active-btn')

  credentials.innerHTML = `
  <form action="/login" method="POST">
    <div class="sign-login-content">
        <input type="text" placeholder="Username" name="username" class="credential-data">
        <br>
        <input type="password" placeholder="Password" name="password" class="credential-data">
        <br>
        <button type="submit" class="credentials-btn">LOGIN</button>
    </div>
  </form>
  `
})
// const profile_pic = document.getElementById("profile-pic")

// function base64convert(x) {
//   return atob(x).split('').map(function(v) {return v.codePointAt(0)});
// };
// base64convert(profile_pic)

if (localStorage.length === 1){
  loc_selector.innerHTML = `
    <div class="flex" style="align-items: center; justify-content: center;">
      <h2>Your selected location is : <span>${seleced_location}</span></h2>
      <button class="ok-btn" id="change-btn">Change</button>
    </div>
  `
  services_offered.innerHTML = `
      <div class="service-card">
      <form action="/all-hospitals-available", method="POST" enctype="multipart/form-data">
          <input type="text" name="location" value="${seleced_location}" style="display: none" class="location-values">
          <button>
              <img src="../static/assets/hospital.png" alt="">
              <div class="heading">
                  <h2>Hospital</h2>
              </div>
              <div class="description">
                  <p>All available hospitals near you</p>
              </div>
          </button>
      </form>
    </div>

    <div class="service-card">
    <form action="/all-ambulance", method="POST" enctype="multipart/form-data">
          <input type="text" name="location" value="${seleced_location}" style="display: none" class="location-values">
          <button>
              <img src="../static/assets/ambulance.png" alt="">
              <div class="heading">
                  <h2>Ambulance</h2>
              </div>
              <div class="description">
                  <p>All available abulance near you</p>
              </div>
          </button>
      </form>

    </div>

    <div class="service-card">
    <form action="/private-doc", method="POST" enctype="multipart/form-data">
          <input type="text" name="location" value="${seleced_location}" style="display: none" class="location-values">
          <button>
              <img src="../static/assets/private-doc.png" alt="">
              <div class="heading">
                  <h2>Private Doctor</h2>
              </div>
              <div class="description">
                  <p>Insearch of a private doc? Click here!</p>
              </div>
          </button>
      </form>
    
    </div>
  `

  const change_btn = document.getElementById("change-btn")
  change_btn.addEventListener("click", () => {
    localStorage.clear();
    location.reload()
  })
}

setTimeout(() => {
  ininvalidMsg.remove()
}, 2000)

function ok(){
  ok_btn.addEventListener('click', () => {
    if (current_loc.value === ''){
      current_loc.placeholder = `Please input a location`;
      current_loc.classList.add('loc-input-warning')
      ok_btn.style.background = 'rgb(226, 33, 33)';
      setTimeout(() => {
          current_loc.placeholder = `Enter your location address`;
          ok_btn.style.background = '#0F25EB';
          current_loc.classList.remove('loc-input-warning')}, 
        2000);
    }else{
      localStorage.clear();
      localStorage.setItem('selectedLocation', current_loc.value);
      location.reload();
    }
    
  })
}


for (let i = 0; i < location_values.length; i++) {
    location_values[i].value = seleced_location;
}


function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#blah')
              .attr('src', e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
  }
}

function readURL2(input) {
  if (input.files && input.files[0]) {
      var reader2 = new FileReader();

      reader2.onload = function (e) {
          $('#blah2')
              .attr('src', e.target.result);
      };

      reader2.readAsDataURL(input.files[0]);
  }
}

// function ratingsfun(){
//   for(let i = 0; i < ratings.value; i++){
//     stars[i].src = "../static/assets/icons/star2.png";
//   }
// }
// ratingsfun()

