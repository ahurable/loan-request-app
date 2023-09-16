

var tab = 1;
    

function handleFormSteps(kind) {
    if (kind=="forward"){
        let input_id = 'form-input-wrapper-' + String(tab)
        
        document.getElementById(input_id).style.display = 'none';
        tab+=1;
        if (tab > 1) {
            document.getElementById("back-button").style.display = 'block';
        }
        if (tab == 5) {
            document.getElementById("continue-button").style.display = 'none';
            document.getElementById("submit-form").style.display='block';
        }

        input_id = 'form-input-wrapper-' + String(tab);
        document.querySelector(`body > section > div.d-lg-block.d-none.steps-holder > div > div:nth-child(${tab})`).style.color = 'black';
        document.getElementById(input_id).style.display = 'flex';
    }
    if (kind=="back"){
        console.log(kind)
        let input_id = 'form-input-wrapper-' + String(tab)
        
        document.getElementById(input_id).style.display = 'none';
        tab-=1;
        if (tab < 5) {
            document.getElementById("continue-button").style.display = 'block';
            document.getElementById("submit-form").style.display='none';
        }
        if (tab == 1) {
            document.getElementById("back-button").style.display = 'none';
        }

        input_id = 'form-input-wrapper-' + String(tab);
        document.querySelector(`body > section > div.d-lg-block.d-none.steps-holder > div > div:nth-child(${tab+1})`).style.color = 'gray';
        document.getElementById(input_id).style.display = 'flex';
    }
}


function showAnswers(thatone) {
    let aw = 'aw-'+thatone
    aw = document.getElementById(aw)
    aw.style.transition = 'all 0.2s'
    if(aw.style.height == '0px'){
        aw.style.height = '120px'
    } else {
        aw.style.height = '0px'
    }
}

function typeOfPays(selectValue) {
    var value = selectValue.value;
    switch (value) {
        case 'fish':
            document.getElementById('fish_input').style.display = 'block';
            document.getElementById('doc_input').style.display = 'none';
            // document.getElementById('card_wrapper').style.display = 'none';
            break;
        case 'document':
            document.getElementById('fish_input').style.display = 'none';
            document.getElementById('doc_input').style.display = 'block';
            // document.getElementById('card_wrapper').style.display = 'none';
            break;
        case 'card':
            document.getElementById('fish_input').style.display = 'none';
            document.getElementById('doc_input').style.display = 'none';
            // document.getElementById('card_wrapper').style.display = 'block';
            break;
        default:
            document.getElementById('fish_input').style.display = 'none';
            document.getElementById('doc_input').style.display = 'none';
            // document.getElementById('card_wrapper').style.display = 'none';
            break;
    }
}

function sendotp(phonenumber){
    fetch(`http://127.0.0.1:8000/retotp/${phonenumber}`)
}

document.querySelector('#range_input').onchange = () => {
    let poorsant = 10
    let rangeInputValue = document.querySelector('#range_input').value 
    document.querySelector('#range_value').innerHTML = rangeInputValue + "000000";
    let prophet = (parseInt(rangeInputValue) * 1000000) * (poorsant / 100)
    console.log(prophet)
    let final = prophet + (parseInt(rangeInputValue) * 1000000)
    document.querySelector('#final_value').innerHTML = String(final)
}
