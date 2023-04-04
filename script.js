let admin = document.querySelector('.admin');
let patient = document.querySelector('.patient');

admin.onClick = () =>{
    admin.classList.toggle('active');
}

patient.onClick = () =>{
    patient.classList.toggle('active'); 
}


