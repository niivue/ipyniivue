import "./widget.css";


async function render({ model, el }) {
  let text = "Hello World and Goodbye"
  console.log(text);
  el.textContent = text
}

export default { render };
