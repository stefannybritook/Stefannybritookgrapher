let latexMathField = "";
const data = document.currentScript.dataset;
const points = data.points;
const MQ = MathQuill;
let myplotdiv = document.getElementById('myplot');
MathQuill = MathQuill.getInterface(1);

let latexSpan = document.getElementById('latex-input');
let config = {
    spaceBehavesLikeTab: true,
    restrictMismatchedBrackets: true,
    supSubsRequireOperand: true,
};
latexMathField = MQ.MathField(latexSpan, config);
let submit_btn = document.getElementById('submit-btn');

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function get_plot(latex_string){
  try {
    const response = await fetch('http://127.0.0.1:8000/grapher/plot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ latex_string: latex_string }),
    });
    const data = await response.json();
    myplotdiv.innerHTML = "";
    Bokeh.embed.embed_item(data);
  } catch (error) {
    console.log(error);
  }
}

submit_btn.addEventListener('click', () => {
  get_plot(latexMathField.latex()); 
});
