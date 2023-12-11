/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/

// const RealizaDiagnostico = async () => {
const RealizaDiagnostico_salvando = () => {

  const formData = valida_formulario();
  var tamanho = 0
  for (var value of formData.values()) {
    tamanho++;
    break;
  }

  if (tamanho > 0) {
    let url = 'http://127.0.0.1:5000/paciente';
    fetch(url, {
      method: 'post',
      body: formData
    })
      .then((response) => response.json())
      .then((data) => {

        if (data.diagnostico == 1) {
          alert("Paciente classificado COM problema cardícado")
        } else {
          alert("Paciente classificado SEM problema cardícado")
        }
      })

      .catch((error) => {
        console.error('Error:', error);
      });
  }
}

/*
  --------------------------------------------------------------------------------------
  Valida formulario
  --------------------------------------------------------------------------------------
*/

const valida_formulario = () => {


  let age = document.getElementById("idade").value;
  let sex = document.getElementById("sexo").value;
  let shestpaintype = document.getElementById("chest_pain_type").value;
  let restingbp = document.getElementById("pa_repouso").value;
  let cholesterol = document.getElementById("colesterol").value;
  let fastingbs = document.getElementById("bs_jejum").value;
  let restingecg = document.getElementById("ecg_repouso").value;
  let maxhr = document.getElementById("max_hr").value;
  let exerciseangina = document.getElementById("exercicio_angina").value;
  let oldpeak = document.getElementById("oldpeak").value;
  let st_slope = document.getElementById("st_slope").value;

  const formData = new FormData();


  if (age === '' || sex === '' || shestpaintype === '' ||
    restingbp === '' || cholesterol === '' || fastingbs === '' ||
    restingecg === '' || maxhr === '' || exerciseangina === '' ||
    oldpeak === '' || st_slope === '') {
    alert("Não pode haver campos em branco");

    return formData
  }

  formData.append('age', age);
  formData.append('sex', sex);
  formData.append('shestpaintype', shestpaintype);
  formData.append('restingbp', restingbp);
  formData.append('cholesterol', cholesterol);
  formData.append('fastingbs', fastingbs);
  formData.append('restingecg', restingecg);
  formData.append('maxhr', maxhr);
  formData.append('exerciseangina', exerciseangina);
  formData.append('oldpeak', oldpeak);
  formData.append('st_slope', st_slope);

  return formData;
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/

// const RealizaDiagnostico = async () => {
const RealizaDiagnostico = () => {

  // Captura dados do furmulário

  const formData = valida_formulario();
  var tamanho = 0
  for (var value of formData.values()) {
    tamanho++;
    break;
  }

  if (tamanho > 0) {
    let url = 'http://127.0.0.1:5000/diagnostico';
    fetch(url, {
      method: 'post',
      body: formData
    })
      .then((response) => response.json())
      .then((data) => {

        if (data.diagnostico == 1) {
          alert("Paciente classificado COM problema cardícado")
        } else {
          alert("Paciente classificado SEM problema cardícado")
        }
      })

      .catch((error) => {
        console.error('Error:', error);
      });
  }
}