let loc_selector = document.getElementById("loc-selector");
const ok_btn = document.getElementById("ok-btn");

let current_loc = document.getElementById("currentloc");
let seleced_location = localStorage.getItem('selectedLocation'); 

let location_values = document.getElementsByClassName('location-values')
let services_offered = document.getElementById('services-offered')

let stars = document.getElementsByClassName('star')
const ratings = document.getElementById('ratings-number')


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
        <form action="">
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
        <form action="">
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
  
